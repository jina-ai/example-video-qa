from pathlib import Path

import click
from jina import Document, DocumentArray, Flow


def index():
    f = Flow.load_config('flows/index.yml')
    with f:
        docs = DocumentArray()
        doc = Document(
            id='zvXkQkqd2I8',
            uri=str((Path(__file__).parent / 'toy-data' / 'zvXkQkqd2I8.vtt').absolute()))
        docs.append(doc)
        resp = f.post(on='/index', inputs=docs, return_results=True)
        f.post(on='/dump', parameters={'dump_path': './workspace/dump_lmdb', 'shards': 1})
        print(f'docs: {len(docs)}')
        for d in resp[0].docs:
            print(f'chunks: {len(d.chunks)}')
            for c in d.chunks:
                print(f'{c.id}: {c.text}')

def query():
    f = Flow.load_config('flows/query.yml')
    with f:
        resp = f.post(on='/search', inputs=[Document(text='is jina a one-liner?')], return_results=True)
        for d in resp[0].docs:
            for m in d.matches:
                print(f'{d.id}: {m.id}, {m.scores["relevance"]}, {m.location}, {m.text}, {m.tags}')


def query_restful():
    f = Flow.load_config('flows/query.yml',
                         override_with={
                             'protocol': 'http',
                             'cors': True,
                             'port_expose': '45678'})

    with f:
        f.block()


@click.command()
@click.option('--mode', '-m', type=click.Choice(['index', 'query', 'query_restful']), default='query')
def main(mode):
    if mode == 'index':
        index()
    elif mode == 'query':
        query()
    elif mode == 'query_restful':
        query_restful()


if __name__ == '__main__':
    main()
