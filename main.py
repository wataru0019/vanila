from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import feedparser
import pprint

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

url = "https://rss.itmedia.co.jp/rss/2.0/itmedia_all.xml"

f = feedparser.parse(url)

articles = []
for article in f['entries'][0:10]:
    articles.append({
        'title': article['title'],
        'link': article['link'],
        'summary': article['summary']
    })

@app.get("/")
def read_root():
    data = articles
    return data

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}