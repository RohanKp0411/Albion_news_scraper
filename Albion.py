import requests
from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np


url = "https://albiononline.com/en/news"


def get_soup(url):
    results = requests.get(url)
    soup = BeautifulSoup(results.text, "html.parser")
    return soup


soup = get_soup(url)

titles = []
dates = []


news_div = soup.find_all("a", class_=lambda x: x and x.startswith("news-item"))

for container in news_div:

    # Extracting the titles of the news
    name = container.h3.text
    titles.append(name)

    # Extracting the date, time and year the news was posted
    date = container.find("span", class_="news-item__date").text
    dates.append(date)


news = pd.DataFrame(
    {
        "News_Name": titles,
        "Date_Year": dates,
    }
)

news.to_csv("Albion News.csv")
