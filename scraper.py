from bs4 import BeautifulSoup
import requests

url = "https://newspicks.com"

response = requests.get(url)

soup = BeautifulSoup(response.content, "lxml")

# news_title = soup.find_all(class_="news-title")
div = soup.find("div", class_="css-kcs4le")
a = div.find_all("a")

# すべてのリンクを取得
for href in a:
    print(f'{url}{href.get("href")}')
    url_a = url + href.get("href")

    response_a = requests.get(url_a)

    soup_a = BeautifulSoup(response_a.content, "lxml")
    main = soup_a.find("main")

    a_readmore = main.find("a")
    print(a_readmore.get("href"))

    url_b = a_readmore.get("href")

    response_b = requests.get(url_b)

    soup_b = BeautifulSoup(response_b.content, "lxml")
    article = soup_b.find("div", class_="body-columns")
    print(article)




def test():
    html = '''
    <div class="news-title">
        test
        <div class="news-review">タイトル1</div>
    </div>
    '''
    soupd = BeautifulSoup(html, "lxml")

    print(soupd.find(class_="news-title").children)
