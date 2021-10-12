import glob
from pathlib import Path
import os
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


def index_self_data(data_dir):
    f = Flow.load_config('flows/index.yml')
    with f:
        docs = DocumentArray()
        for fn in glob.glob(os.path.join(data_dir, '*.vtt')):
            path = fn
            fid = str(os.path.splitext(os.path.split(path)[-1])[0])
            doc = Document(id=fid, uri=path)
            docs.append(doc)
        resp = f.post(on='/index', inputs=docs, return_results=True)
        f.post(on='/dump', parameters={'dump_path': './workspace/dump_lmdb', 'shards': 1})
        print(f'docs: {len(docs)}')
        for d in resp[0].docs:
            print(f'chunks: {len(d.chunks)}')
            for c in d.chunks:
                print(f'{c.id}: {c.text}')


def query():
    f = Flow.load_config('flows/query.yml',
                         override_with={
                             'protocol': 'grpc',
                             'cors': False})
    with f:
        resp = f.post(on='/search', inputs=[Document(text='is jina a one-liner?')], return_results=True)
        for d in resp[0].docs:
            for m in d.matches:
                print(f'{d.id}: {m.id}, {m.scores["relevance"]}, {m.location}, {m.text}, {m.tags}')


def query_restful():
    f = Flow.load_config('flows/query.yml')

    with f:
        f.block()


@click.command()
@click.option('--mode', '-m', type=click.Choice(['index', 'query']), default='query')
# @click.option('--top_k', '-k', default=TOP_K)
@click.option('--dataset', '-d', type=click.Choice(['toy-data', 'self-data'],case_sensitive=False),
              default='toy-data')
@click.option('--data_dir', type=click.Path(exists=True))
def main(mode, dataset, data_dir):
    if mode == 'index' and dataset == 'toy-data':
        index()
    elif mode == 'index' and dataset == 'self-data':
        index_self_data(data_dir)
    elif mode == 'query':
        query_restful()


if __name__ == '__main__':
    main()
