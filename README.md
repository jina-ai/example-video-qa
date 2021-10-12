# example-video-search
This is an example of building a video Question-Answer system using Jina.

The index data is subtitle files of YouTube videos. After indexing, you can query with questions in natural langurage and retrieve the related video together with the timestamp that the corresponding answer appears. 

![](.github/demo.gif)

## Prerequisites

```bash
pip install -r requirements.txt
```

### Usage

By default, we index the subtitle file, `toy-data/zvXkQkqd2I8.vtt`

```bash
python app.py -m index
```

Query with questions,

```bash
python app.py -m query
```

To start the video UI, run the following codes and open `http://localhost:3000/video/` in your browser.

```bash
git clone https://github.com/jina-ai/jina-ui.git
cd jina-ui
git checkout showcase-video-search
yarn install
yarn jinajs build
yarn showcases dev
```

## How it works

The index flow is as below. The sentences are extracted from the subtitle file. The meta information of the sentences are stored in the `LMDBStorage`. In the other pathway, the sentences of the subtitles are encoded by the `DPRTextEncoder` and afterwards the result embeddings are stored in the `SimpleIndexer`.

![](.github/flow_index.png)

The query flow is as shown below. 

1. The input query is a question which is encoded into embeddings by using `DPRTextEncoder`. 
2. The embedding of the query question is used to retrieve the sentences from `SimpleIndexer`. 
3. After retrieving the indexed sentences, we use `MatchExpander` to extend the questions so that the sentences from the neighboring timestamps are considered as candidate sentences as well.
4. Rank the candidate sentences and extract the exact answers from the sentences by using `DPRReaderRanker`. 
5. Get the timestamp and video uri information about the answer candidates with `Text2Frame`

![](.github/flow_query.png)

## How to index my own data? [W.I.P.]

1. download the subtitle files
```bash
youtube-dl --write-auto-sub --skip-download https://www.youtube.com/watch\?v\=zvXkQkqd2I8 -o data/zvXkQkqd2I8
```

2. run the following
```bash
python app.py -m index -d data
python app.py -m query
```