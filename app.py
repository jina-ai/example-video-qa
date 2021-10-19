import glob
from pathlib import Path
import os
import click
from jina import Document, DocumentArray, Flow


def doc_generator(data_dir, num_docs):
    for i, fn in enumerate(glob.glob(os.path.join(data_dir, '*.vtt'))):
        if i < num_docs:
            fid = os.path.splitext(os.path.basename(fn))[0]
            doc = Document(id=fid, uri=fn)
            yield doc


def index(data_dir, num_docs):
    f = Flow.load_config('flows/index.yml')
    with f:
        resp = f.post(on='/index', inputs=doc_generator(data_dir, num_docs), request_size=4, return_results=True)
        f.post(on='/dump', parameters={'dump_path': './workspace/dump_lmdb', 'shards': 1})


def query_restful():
    f = Flow.load_config('flows/query.yml')

    with f:
        # create a psql snapshot
        f.post(on='/snapshot')
        # load data into faiss
        f.post(on='/sync', parameters={'only_delta': True})
        f.block()


@click.command()
@click.option('--mode', '-m', type=click.Choice(['index', 'query']), default='query')
@click.option('--data_dir', type=click.Path(exists=True))
@click.option("--num_docs", "-n", default=100)
def main(mode, data_dir, num_docs):
    if mode == 'index':
        index(data_dir, num_docs)
    elif mode == 'query':
        query_restful()


if __name__ == '__main__':
    main()
