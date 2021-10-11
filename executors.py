from typing import Dict, Iterable, List, Optional, Tuple
import webvtt
import os


import numpy as np
import torch

from jina import Document, DocumentArray, Executor, requests
from transformers import DPRReader, DPRReaderTokenizerFast


class SubtitleExtractor(Executor):
    @requests
    def extract(self, docs: Optional[DocumentArray], **kwargs):
        """
        Extract text from the `.vtt` files the use the heuristics to remove the duplicated text.

        :param docs:
        :param kwargs:
        :return:
        """
        if not docs:
            return
        for doc in docs:
            subtitles = self._load_subtitles(doc.uri)
            for idx, (beg, end, s) in enumerate(subtitles):
                len_tokens = len([t for t in s.split(' ')])
                if len_tokens <= 5:
                    continue
                chunk = Document(id=f'{doc.id}_{idx}', text=s)
                chunk.tags['beg_in_seconds'] = beg
                chunk.tags['end_in_seconds'] = end
                chunk.tags['vid'] = os.path.basename(doc.uri)
                chunk.location.append(int(beg * 1000))  # location in milliseconds
                chunk.location.append(int(end * 1000))  # location in milliseconds
                doc.chunks.append(chunk)

    def _load_subtitles(self, uri):
        beg = None
        is_last_cap_complete = True
        subtitles = []
        prev_parts = []
        for caption in webvtt.read(uri):
            # print(f'{repr(caption.text)}')
            cur_parts = [t for t in filter(lambda x: len(x.strip()) > 0, caption.text.split('\n'))]
            filtered_text = ' '.join(cur_parts)
            if len(cur_parts) == 1:
                if cur_parts[0] in prev_parts:
                    continue
            if len(cur_parts) > 1:
                if cur_parts[0] in prev_parts and is_last_cap_complete:
                    filtered_text = ' '.join(cur_parts[1:])
            is_cur_complete = True
            if is_last_cap_complete:
                beg = caption.start_in_seconds
            if caption.text.startswith(' \n') or caption.text.endswith('\n '):
                is_cur_complete = False
            if is_cur_complete:
                filtered_text = self.format_text(filtered_text)
                subtitles.append((beg, caption.end_in_seconds, filtered_text))
            is_last_cap_complete = is_cur_complete
            prev_parts = cur_parts
        return subtitles

    def format_text(self, text):
        return text.replace('gina', 'jina').replace('gene', 'jina')


class MatchExtender(Executor):
    def __init__(self, window_size=2, **kwargs):
        super().__init__(**kwargs)
        self._window_size = window_size

    @requests
    def extend_matches(self, docs: Optional[DocumentArray] = None, **kwargs):
        if not docs:
            return
        for doc in docs:
            expanded_m_list = []
            for m in doc.matches:
                expanded_id_list = self._extend(m.id)
                for expanded_id in expanded_id_list:
                    expanded_m_list.append(Document(id=expanded_id))
            doc.matches.extend(expanded_m_list)

    def _extend(self, m_id):
        vid, cur_m_id = m_id.split('_')
        cur_m_id = int(cur_m_id)
        results = []
        for idx in range(1, self._window_size+1):
            expanded_m_id = cur_m_id + idx
            results.append(f'{vid}_{expanded_m_id}')
            expanded_m_id = cur_m_id - idx
            # if expanded_m_id < 0:
            #     continue
            # results.append(f'{vid}_{expanded_m_id}')
        return results


def _logistic_fn(x: np.ndarray) -> List[float]:
    """Compute the logistic function"""
    return (1 / (1 + np.exp(-x))).tolist()


class DPRReaderRanker(Executor):
    """
    This executor first extracts answers (answers spans) from all the matches,
    ranks them according to their relevance score, and then replaces the original
    matches with these extracted answers.

    This executor uses the DPR Reader model to re-rank documents based on
    cross-attention between the question (main document text) and the answer
    passages (text of the matches + their titles, if specified).
    """

    def __init__(
            self,
            pretrained_model_name_or_path: str = 'facebook/dpr-reader-single-nq-base',
            base_tokenizer_model: Optional[str] = None,
            title_tag_key: Optional[str] = None,
            num_spans_per_match: int = 2,
            max_length: Optional[int] = None,
            traversal_paths: Iterable[str] = ('r',),
            batch_size: int = 32,
            device: str = 'cpu',
            *args,
            **kwargs,
    ):
        """
        :param pretrained_model_name_or_path: Can be either:
            - the model id of a pretrained model hosted inside a model repo
              on huggingface.co.
            - A path to a directory containing model weights, saved using
              the transformers model's `save_pretrained()` method
        :param base_tokenizer_model: Base tokenizer model. The possible values are
            the same as for the `pretrained_model_name_or_path` parameters. If not
            provided, the `pretrained_model_name_or_path` parameter value will be used
        :param title_tag_key: The key of the tag that contains document title in the
            match documents. Specify it if you want the text of the matches to be combined
            with their titles (to mirror the method used in training of the original model)
        :param num_spans_per_match: Number of spans to extract per match
        :param max_length: Max length argument for the tokenizer
        :param traversal_paths: Default traversal paths for processing documents,
            used if the traversal path is not passed as a parameter with the request.
        :param batch_size: Default batch size for processing documents, used if the
            batch size is not passed as a parameter with the request.
        :param device: The device (cpu or gpu) that the model should be on.
        """
        super().__init__(*args, **kwargs)
        self.title_tag_key = title_tag_key
        self.device = device
        self.max_length = max_length
        self.num_spans_per_match = num_spans_per_match

        if not base_tokenizer_model:
            base_tokenizer_model = pretrained_model_name_or_path

        self.tokenizer = DPRReaderTokenizerFast.from_pretrained(base_tokenizer_model)
        self.model = DPRReader.from_pretrained(pretrained_model_name_or_path)

        self.model = self.model.to(torch.device(self.device)).eval()

        self.traversal_paths = traversal_paths
        self.batch_size = batch_size

    @requests
    def rank(
            self, docs: Optional[DocumentArray] = None, parameters: Dict = {}, **kwargs
    ) -> DocumentArray:
        """
        Extracts answers from existing matches, (re)ranks them, and replaces the current
        matches with extracted answers.

        For each match `num_spans_per_match` of answers will be extracted, which
        means that the new matches of the document will have a length of previous
        number of matches times `num_spans_per_match`.

        The new matches will be have a score called `relevance_score` saved under
        their scores. They will also have a tag `span_score`, which refers to their
        span score, which is used to rank answers that come from the same match.

        If you specified `title_tag_key` at initialization, the tag `title` will
        also be added to the new matches, and will equal the title of the match from
        which they were extracted.

        :param docs: Documents whose matches to re-rank (specifically, the matches of
            the documents on the traversal paths will be re-ranked). The document's
            `text` attribute is taken as the question, and the `text` attribute
            of the matches as the context. If you specified `title_tag_key` at
            initialization, the matches must also have a title (under this tag).
        :param parameters: dictionary to define the `traversal_paths` and the
            `batch_size`. For example
            `parameters={'traversal_paths': ['r'], 'batch_size': 10}`
        """

        if not docs:
            return None

        traversal_paths = parameters.get('traversal_paths', self.traversal_paths)
        batch_size = parameters.get('batch_size', self.batch_size)

        for doc in docs.traverse_flat(traversal_paths):
            if not getattr(doc, 'text'):
                continue

            new_matches = []

            doc_arr = DocumentArray([doc])
            match_batches_generator = doc_arr.batch(
                traversal_paths=['m'],
                batch_size=batch_size,
                require_attr='text',
            )
            for matches in match_batches_generator:
                question, contexts, titles = self._prepare_inputs(doc_arr[0].text, matches)
                with torch.inference_mode():
                    new_matches += self._get_new_matches(question, contexts, titles)

            # Make sure answers are sorted by relevance scores
            new_matches.sort(
                key=lambda x: (
                    x.scores['relevance_score'].value,
                    x.scores['span_score'].value,
                ),
                reverse=True,
            )

            # Replace previous matches with actual answers
            doc_arr[0].matches = new_matches

    def _prepare_inputs(
            self, question: str, matches: DocumentArray
    ) -> Tuple[str, List[str], Optional[List[str]]]:
        contexts = matches.get_attributes('text', 'tags__beg_in_seconds', 'tags__end_in_seconds', 'tags__vid')

        titles = None
        if self.title_tag_key:
            titles = matches.get_attributes(f'tags__{self.title_tag_key}')

            if len(titles) != len(matches) or None in titles:
                raise ValueError(
                    f'All matches are required to have the {self.title_tag_key}'
                    ' tag, but found some matches without it.'
                )

        return question, contexts, titles

    def _get_new_matches(
            self, question: str, contexts: List[Tuple[str]], titles: Optional[List[str]]
    ) -> List[Document]:
        texts, beg_in_seconds, end_in_seconds, vid_list = contexts
        encoded_inputs = self.tokenizer(
            questions=[question] * len(texts),
            titles=titles,
            texts=texts,
            padding='longest',
            return_tensors='pt',
        ).to(self.device)
        outputs = self.model(**encoded_inputs)

        # For each context, extract num_spans_per_match best spans
        best_spans = self.tokenizer.decode_best_spans(
            encoded_inputs,
            outputs,
            num_spans=self.num_spans_per_match * len(contexts),
            num_spans_per_passage=self.num_spans_per_match,
        )

        new_matches = []
        for idx, span in enumerate(best_spans):
            new_match = Document(text=span.text)
            new_match.scores['relevance_score'] = _logistic_fn(
                span.relevance_score.cpu()
            )
            new_match.scores['span_score'] = _logistic_fn(span.span_score.cpu())
            new_match.tags['beg_in_seconds'] = beg_in_seconds[span.doc_id]
            new_match.tags['end_in_seconds'] = end_in_seconds[span.doc_id]
            new_match.tags['original_text'] = texts[span.doc_id]
            new_match.tags['vid'] = vid_list[span.doc_id]
            if titles:
                new_match.tags['title'] = titles[span.doc_id]
            new_matches.append(new_match)

        return new_matches


class Text2Frame(Executor):
    @requests
    def convert(self, docs: Optional[DocumentArray]=None, **kwargs):
        if not docs:
            return
        for doc in docs:
            new_matches = []
            for m in doc.matches:
                new_match = m
                new_match.location.append(int(new_match.tags['beg_in_seconds'] * 1000))
                new_match.location.append(int(new_match.tags['end_in_seconds'] * 1000))
                vid = new_match.tags['vid'].split('.')[0]
                new_match.uri = f'https://www.youtube.com/watch?v={vid}'
                new_match.tags['timestamp'] = int(new_match.tags['beg_in_seconds'])
                new_match.scores['cosine'] = new_match.scores['relevance']
                new_matches.append(new_match)
            doc.matches = new_matches
