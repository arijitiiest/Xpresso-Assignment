from elasticsearch import Elasticsearch, RequestsHttpConnection


def connect_elasticsearch():
    _es = None
    _es = Elasticsearch(hosts=[{"host": "host.docker.internal", "port": 9200}], connection_class=RequestsHttpConnection, 
            max_retries=30, retry_on_timeout=True, request_timeout=30)
    if _es.ping():
        print("ElasticSearch Connected...")
    else:
        print("ElasticSearch Connection Failed!!!")
    return _es


def create_index(es_object, index_name="articles"):
    created = False

    #index settings
    settings = {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0
        },
        "mappings": {
            "_doc": {
                "dynamic": "strict",
                "properties": {
                    "id": {"type": "integer"},
                    "title": {"type": "text"},
                    "url": {"type": "text"},
                    "imageUrl": {"type": "text"},
                    "newsSite": {"type": "text"},
                    "summary": {"type": "text"},
                    "publishedAt": {"type": "text"},
                    "updatedAt": {"type": "text"},
                    "featured": {"type": "text"},
                    "launches": {"type": "text"},
                    "events": {"type": "text"},
                }
            }
        }
    }

    try:
        if es_object.indices.exists(index_name):
            es_object.indices.delete(index=index_name, ignore=[400, 404])

        es_object.indices.create(index=index_name, ignore=400, body=settings)
        print('Created Index')
        created = True
    except Exception as ex:
        print(str(ex))
    finally:
        return created

