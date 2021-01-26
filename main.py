import requests
from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

headers = {"Accept-Language": "en-US, en;q=0.5" }
url = "https://www.imdb.com/search/title/?groups=top_1000&ref_=adv_prv"

def get_me_soup(url, headers):
    results = requests.get(url, headers=headers)
    soup = BeautifulSoup(results.text, "html.parser")
    return soup

soup = get_me_soup((url,headers))

titles = []
years = []
time = []
imdb_ratings = []
metascores = []
votes = []
us_gross = []

movie_div = soup.find_all('div', class_='lister-item mode-advanced')

for container in movie_div:
    name = container.h3.a.text
    titles.append(name)

    year = container.h3.find('span', class_='lister-item-year').text
    years.append(year)

    runtime = container.find('span', class_='runtime').text if container.p.find('span', class_='runtime') else ''
    time.append(runtime)

    imdb = float(container.strong.text)
    imdb_ratings.append(imdb)

    m_score = container.find('span', class_='metascore').text if container.find('span', class_='metascore') else '-'
    metascores.append(m_score)

    nv = container.find_all('span', attrs={'name': 'nv'})

    vote = nv[0].text
    votes.append(vote)

    grosses = nv[1].text if len(nv) > 1 else '-'
    us_gross.append(grosses)

movies = pd.DataFrame({
    'movie': titles,
    'year': years,
    'timeMin': time,
    'imdb': imdb_ratings,
    'metascore': metascores,
    'votes': votes,
    'us_grossMillions': us_gross
})

# print(movies.isna())


movies.to_csv('movies.csv')
