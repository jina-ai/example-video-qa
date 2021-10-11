from pathlib import Path
from executors import SubtitleExtractor, MatchExtender, DPRReaderRanker

from jina import Document, DocumentArray


def test_subtitle_extractor():
    data_fn = Path(__file__).parents[1] / 'toy-data' / 'zvXkQkqd2I8.vtt'
    exec = SubtitleExtractor()
    docs = DocumentArray([Document(uri=str(data_fn.absolute()))])
    exec.extract(docs)
    assert len(docs[0].chunks) == 231


def test_subtitle_extractor_case1():
    data_fn = Path(__file__).parent / 'toy-data' / 'data1.vtt'
    exec = SubtitleExtractor()
    docs = DocumentArray([Document(uri=str(data_fn.absolute()))])
    exec.extract(docs)
    for c in docs[0].chunks:
        print(f'{c.location}: {c.text}')
    assert len(docs[0].chunks) == 3


def test_subtitle_extractor_case2():
    data_fn = Path(__file__).parent / 'toy-data' / 'data2.vtt'
    exec = SubtitleExtractor()
    docs = DocumentArray([Document(uri=str(data_fn.absolute()))])
    exec.extract(docs)
    for c in docs[0].chunks:
        print(f'{c.location}: {c.text}')
    assert len(docs[0].chunks) == 13


def test_question_generator_case1():
    csv_fn = Path(__file__).parent / 'toy-data' / 'answer2.csv'
    text_list = []
    from itertools import islice

    def window(seq, n=2):
        "Returns a sliding window (of width n) over data from the iterable"
        "   s -> (s0,s1,...s[n-1]), (s1,s2,...,sn), ...                   "
        it = iter(seq)
        result = tuple(islice(it, n))
        if len(result) == n:
            yield ' '.join(result)
        for elem in it:
            result = result[1:] + (elem,)
            yield ' '.join(result)

    with open(csv_fn, 'r') as f:
        for l in f:
            beg, end, text = l.strip('\n').split(',')
            text_list.append(text)

    answer_list = DocumentArray()
    for window_size in range(1, 5):
        for s in window(text_list, window_size):
            doc = Document(text=s)
            answer_list.append(doc)

    q_generator = QuestionGenerator(num_questions=3)
    q_generator.doc2query(docs=answer_list)
    for d in answer_list:
        for c in d.chunks:
            print(f'{d.text}: ({c.weight}) {c.text}')


def test_match_extender():
    exec = MatchExtender(window_size=4)
    docs = DocumentArray()
    doc = Document(id='doc_1')
    doc.matches.append(Document(id='zvXkQkqd2I8_91', text='to searching a typical jina app project'))
    docs.append(doc)
    exec.extend_matches(docs=docs)
    for d in docs:
        assert len(d.matches) == 5
        for m in d.matches:
            print(f'{m.id}')


def test_dpr_ranker():
    exec = DPRReaderRanker(batch_size=2)
    docs = DocumentArray()
    doc = Document(id='doc_1', text='what is apple?')
    m_list = [
        'as a framework jina is designed to be',
        'apple is designed to be distributed on the cloud.',
        'apple is an easier way to develop neural search on the cloud.',
    ]
    for idx, m_text in enumerate(m_list):
        m = Document(text=m_text, id=f'zvXkQkqd2I8_{idx}')
        m.tags['beg_in_seconds'] = idx * 0.1
        m.tags['end_in_seconds'] = idx * 0.1
        doc.matches.append(m)
    docs.append(doc)
    exec.rank(docs=docs)
    for d in docs:
        for m in d.matches:
            print(
                f'{m.id}({m.scores["relevance_score"].value}, {m.scores["span_score"].value}): {m.text}, {m.tags}')
