from bs4 import BeautifulSoup
import requests
import tabelog_object

url = "https://tabelog.com/osaka/A2701/A270107/R3323/rstLst/?vs=1&sa=%E4%BA%AC%E6%A9%8B%E9%A7%85%EF%BC%88%E5%A4%A7%E9%98%AA%E5%BA%9C%EF%BC%89"

response = requests.get(url)

soup = BeautifulSoup(response.content, "lxml")

kyobashi_list = soup.find_all(class_="list-rst__rst-data")

for tenpo_data in kyobashi_list:
    tabelog_object.create_table()

    name = tenpo_data.find(class_="list-rst__rst-name-target cpy-rst-name")
    eat_type = tenpo_data.find(class_="list-rst__area-genre cpy-area-genre")
    score = tenpo_data.find(class_="c-rating__val c-rating__val--strong list-rst__rating-val")
    tenpo = tabelog_object.Tenpo(name.text, name.get("href"), eat_type.text, score.text)
    tenpo.save()

tenpos = tabelog_object.find_all()

for tenpo in tenpos:
    print(f'{tenpo["name"]}: {tenpo["score"]}')
