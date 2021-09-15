from flask import Flask, jsonify, request
from elasticsearch import helpers
import requests

from utils import connect_elasticsearch, create_index

app = Flask(__name__)

# Connect to the Elasticsearch 
es = connect_elasticsearch()

# Seed Data route
@app.route("/seed", methods=["GET"])
def seed_data():
    try:
        res = requests.get("https://api.spaceflightnewsapi.net/v3/articles")

        create_index(es, index_name="articles")

        for d in res.json():
            es.index(index="articles", body=d, id=d['id'])

    except Exception as ex:
        print(str(ex))
    finally:
        return jsonify(res.json())

# Search Keyword route
@app.route("/search", methods=["GET"])
def search():
    keyword = request.args.get('keyword')
    if keyword:
        query = {
            "query": {
                "multi_match": {
                    "query": str(keyword),
                    "fields": ["summary", "title", "newsSite"]
                }
            }
        }
    else:
        query = {
            "query": {
                "match_all": {}
            }
        }
    found = es.search(index="articles", body=query)
    result = []
    for article in found["hits"]["hits"]:
        result.append(article['_source'])
    return jsonify(count=found["hits"]["total"]["value"], data=result)

# Default
@app.route("/")
def hello_world():
    return "<p>Hello, World!</p><p><a href='/search'>Search</a></p>"