from fastapi import FastAPI, Form, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os

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

@app.get("/")
def read_root():
    data = articles
    return data

class RSSRequest(BaseModel):
    url: str

@app.post("/rss")
def read_rss(rss_url: RSSRequest):
    f = feedparser.parse(rss_url.url)
    
    articles = []
    for article in f['entries'][0:10]:
        articles.append({
            'title': article['title'],
            'link': article['link'],
            'summary': article['summary']
        })

    return articles
    
# def read_rss(url: str = Form(...)):
# # https://rss.itmedia.co.jp/rss/2.0/itmedia_all.xml
#     rss_url = url

#     f = feedparser.parse(url)

#     articles = []
#     for article in f['entries'][0:10]:
#         articles.append({
#             'title': article['title'],
#             'link': article['link'],
#             'summary': article['summary']
#         })
#     print(url)
#     return articles

@app.post("/fileupload")
async def file_upload(file: UploadFile = Form(...)):
    contents = await file.read()
    file_location = f"./{file.filename}"
    with open(file_location, "wb") as f:
        f.write(contents)
    return {"filename": file.filename, "content-type": file.content_type}