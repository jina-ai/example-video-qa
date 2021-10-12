# example-video-search
This is an example of building a video Question-Answer system using Jina.

## Prerequisites

```bash
pip install -r requirements.txt
```

### Usage

Index the the subtitle file, `toy-data/zvXkQkqd2I8.vtt`

```bash
python app.py -m index
```


Query with questions,

```bash
python app.py -m query
```

## How it works

The index flow is as below. The sentences are extracted from the subtitle file. The meta information of the sentences are stored in the `LMDBStorage`. The vectors of the sentences are stored in the `SimpleIndexer`.

![](.github/flow_index.png)

The query flow is as below

![](.github/flow_query.png)
