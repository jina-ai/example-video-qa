import sys

from jina import Document, DocumentArray, Flow


def index():
    f = Flow.load_config('flows/index.yml')
    with f:
        docs = DocumentArray()
        doc = Document(
            id='mnnC37ewQI8',
            uri='./toy-data/mnnC37ewQI8.mkv')
        docs.append(doc)
        f.post(on='/index', inputs=docs, show_progress=True)


def query_restful():
    f = Flow.load_config('flows/query.yml')

    with f:
        f.block()


def main(mode):
    if mode == 'index':
        index()
    elif mode == 'query':
        query_restful()


if __name__ == '__main__':
    mode = sys.argv[1]
    main(mode)
