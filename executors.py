from typing import Optional
import os

from jina import DocumentArray, Executor, requests

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
                vid = os.path.basename(new_match.tags['video_uri']).split('.')[0]
                new_match.uri = f'https://www.youtube.com/watch?v={vid}'
                new_match.scores['cosine'] = new_match.scores['relevance']
                new_match.tags['timestamp'] = int(new_match.tags['beg_in_seconds'])
                new_match.tags['vid'] = vid
                new_matches.append(new_match)
            doc.matches = new_matches
