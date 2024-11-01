import feedparser
import pprint

url = "https://rss.itmedia.co.jp/rss/2.0/itmedia_all.xml"

f = feedparser.parse(url)

articles = []
for article in f['entries'][0:10]:
    articles.append({
        'title': article['title'],
        'link': article['link'],
        'summary': article['summary']
    })

print(articles)