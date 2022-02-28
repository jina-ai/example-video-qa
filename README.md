# example-video-search
This is an example of building a video Question-Answer system using Jina.

The index data is videos with subtitle information. After indexing, you can query with questions in natural language and retrieve the related video together with the timestamp that the corresponding answer appears. 

![](.github/demo.gif)

## Prerequisites

We use the YouTube video as a toy example,

```bash
pip install -r requirements.txt
bash scripts/download_data.sh
```

### Usage

By default, we index the video file, `toy-data/mnnC37ewQI8.mkv`

```bash
python app.py index
```

Query with questions,

```bash
python app.py query
```

To run the video search frontend, first set it up locally.
You should have Node and Yarn installed on your machine.

```bash
cd frontend
yarn
```

This will install the necessary dependencies.

To run the search frontend, run

```bash
yarn dev
```

You can see the search frontend at [`http://localhost:3000/`](http://localhost:3000/).


## How it works

The index flow is as below. The sentences are extracted from the subtitle file. 
In the other pathway, the sentences of the subtitles are encoded by the `DPRTextEncoder`. 
The meta information of the sentences together with embeddings are stored in the `SimpleIndexer`.

![](.github/flow_index.png)

The query flow is as shown below. 

1. The input query is a question which is encoded into embeddings by using `DPRTextEncoder`. 
2. The embedding of the query question is used to retrieve the sentences from `SimpleIndexer`. 
3. Rank the candidate sentences and extract the exact answers from the sentences by using `DPRReaderRanker`. 
4. Get the timestamp and video uri information about the answer candidates with `Text2Frame`

![](.github/flow_query.png)

## How to index my own data?

1. download the subtitle files
```bash
youtube-dl --write-sub --embed-subs -o toy-data/zvXkQkqd2I8 https://www.youtube.com/watch\?v\=zvXkQkqd2I8
```
 > Replace `--write-sub` with `--write-auto-sub` when there is no subtitle file uploaded manually. This will use the subtitles generated automatically from YouTube.

2. run the following
```bash
python app.py index
python app.py query
```