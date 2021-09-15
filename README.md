# Space launch search API

# ElasticSearch Setup

```
docker pull docker.elastic.co/elasticsearch/elasticsearch:7.14.1

docker run -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" --name "elasticsearch" docker.elastic.co/elasticsearch/elasticsearch:7.14.1
```

- Start Container

```
docker start elasticsearch
```

- Stop Container

```
docker stop elasticsearch
```

# Flask Setup

```
export FLASK_APP=hello
flask run
```

# Routes

- http://127.0.0.1:5000/seed
- http://127.0.0.1:5000/search?keyword=abc
