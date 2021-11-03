from pathlib import Path

import click
from jina import Document, DocumentArray, Flow


def index():
    f = Flow.load_config('flows/index.yml')
    with f:
        docs = DocumentArray()
        doc = Document(
            id='mnnC37ewQI8',
            uri='./toy-data/mnnC37ewQI8.mkv')
        docs.append(doc)
        f.post(on='/index', inputs=docs)


def query_restful():
    f = Flow.load_config('flows/query.yml')

    with f:
        f.block()


@click.command()
@click.option('--mode', '-m', type=click.Choice(['index', 'query']), default='query')
def main(mode):
    if mode == 'index':
        index()
    elif mode == 'query':
        query_restful()


if __name__ == '__main__':
    main()
