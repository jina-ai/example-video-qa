# example-video-search
This is an example of building a video Question-Answer system using Jina.

The index data is subtitle files of YouTube videos. After indexing, you can query with questions in natural langurage and retrieve the related video together with the timestamp that the corresponding answer appears. 

![](.github/demo.gif)

## Prerequisites

```bash
pip install -r requirements.txt
```

You need to have the Postgres service running at the backend. If you just want to try it our, you can use the psql docker image,

```bash
docker run -e POSTGRES_PASSWORD=123456  -p 127.0.0.1:5432:5432/tcp postgres:13.2
```

If you want to keep your data in the psql database,

----
### On Mac OS X

1. Install Postgres

```bash
# install postgres
brew install postgresql
```

1. Start Postgres
```bash
pg_ctl -D /usr/local/var/postgres start
```

1. Config Postgres
```bash
psql postgres
```

1. Create a new role with `psql`. By default we use `postgres` as the `ROLE` with the password `123456`. If you want to change to other values, please change the `username` and `password` in the `index.yml` and `query.yml` accordingly

```sql
postgres=# \du

postgres=# CREATE ROLE postgres WITH LOGIN PASSWORD '123456';

postgres-# ALTER ROLE postgres SUPERUSER;
```

1. Stop the Postgres

```bash
pg_ctl -D /usr/local/var/postgres stop
```

----

### On Ubuntu

1. Install Postgres
```bash
sudo apt-get install postgresql postgresql-contrib
```

1. Start Postgres
```bash
systemctl start postgresql
```

1. Config Postgres
```bash
sudo -u postgres psql
```

1. Create a new role with `psql`. By default we use `postgres` as the `ROLE` with the password `123456`. If you want to change to other values, please change the `username` and `password` in the `index.yml` and `query.yml` accordingly

```sql
postgres=# \du

postgres=# CREATE ROLE postgres WITH LOGIN PASSWORD '123456';

postgres-# ALTER ROLE postgres SUPERUSER;
```

1. Stop the Postgres

```bash
systemctl stop postgresql
```


### Usage

By default, we index the subtitle file, `toy-data/zvXkQkqd2I8.vtt`.


```bash
python app.py -m index --data-dir ./toy-data
```

Query with questions,

```bash
python app.py -m query
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

The index flow is as below. The sentences are extracted from the subtitle file. The meta information of the sentences are stored in the `LMDBStorage`. In the other pathway, the sentences of the subtitles are encoded by the `DPRTextEncoder` and afterwards the result embeddings are stored in the `SimpleIndexer`.

![](.github/flow_index.png)

The query flow is as shown below. 

1. The input query is a question which is encoded into embeddings by using `DPRTextEncoder`. 
2. The embedding of the query question is used to retrieve the sentences from `SimpleIndexer`. 
3. After retrieving the indexed sentences, we use `MatchExpander` to extend the questions so that the sentences from the neighboring timestamps are considered as candidate sentences as well.
4. The candidate sentences retrieved from the above steps have no text or meta information. We retrieve the meta information from `LMDBStorage`.
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
python app.py -m index --data_dir FOLDER_OF_YOUR_VTTFILES
python app.py -m query
```
If your folder contains large amount of .vtt files, you could add -n to limit the number of file input, for example:
```bash
python app.py -m index --data_dir FOLDER_OF_YOUR_VTTFILES -n 10
```
In this way you could index the first 10 .vtt files in your folder.