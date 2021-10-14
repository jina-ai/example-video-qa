import glob
from pathlib import Path
import os
import click
from jina import Document, DocumentArray, Flow


def doc_generator(data_dir, num_docs):
    f = Flow.load_config('flows/index.yml')
    with f:
        docs = DocumentArray()
        for i, fn in enumerate(glob.glob(os.path.join(data_dir, '*.vtt'))):
            if i < num_docs:
                fid = os.path.splitext(os.path.basename(fn))[0]
                doc = Document(id=fid, uri=fn)
                docs.append(doc)
        resp = f.post(on='/index', inputs=docs, return_results=True)
        f.post(on='/dump', parameters={'dump_path': './workspace/dump_lmdb', 'shards': 1})


def index(dataset,data_dir, num_docs):
    f = Flow.load_config('flows/index.yml')
    with f:
        if dataset == 'toy-data':
            path = str((Path(__file__).parent / 'toy-data' ).absolute())
            doc_generator(path,num_docs)
        elif dataset == 'self-data':
            doc_generator(data_dir,num_docs)


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
@click.option('--dataset', '-d', type=click.Choice(['toy-data', 'self-data'],case_sensitive=False),
              default='toy-data')
@click.option('--data_dir', type=click.Path(exists=True))
@click.option("--num_docs", "-n", default=100)
def main(mode, dataset, data_dir, num_docs):
    if mode == 'index':
        index(dataset,data_dir, num_docs)
    elif mode == 'query':
        query_restful()


if __name__ == '__main__':
    main()
