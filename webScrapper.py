import pandas as pd
from requests import get
from bs4 import BeautifulSoup
from time import sleep
from random import randint
from IPython.core.display import clear_output
from time import time

start_time = time()
requests = 0
movies, years, ratings, metascores, votes = [],[],[],[],[]
urls = ['https://www.imdb.com/search/title/?title_type=feature&release_date='+str(i) for i in range(2000,2020)]
for url in urls:
    response = get(url)
    sleep(randint(8,15))

    # Monitor the requests
    requests += 1
    elapsed_time = time() - start_time
    print('Request:{}; Frequency: {} requests/s'.format(requests, requests/elapsed_time))
    clear_output(wait = True)
    htmlSoup = BeautifulSoup(response.text, 'html.parser')
    movieContainers = htmlSoup.find_all('div',class_ = 'lister-item mode-advanced')

    for movieContainer in movieContainers:
        movies.append(movieContainer.h3.a.text)
        years.append(movieContainer.find('span', class_ = 'lister-item-year').text)
        if movieContainer.find('span', class_ = 'metascore favorable') is not None:
            metascores.append(int(movieContainer.find('span',class_ = 'metascore favorable').text))
        else:
            metascores.append(None)
        if movieContainer.find('div', class_='inline-block ratings-imdb-rating') is not None:
            ratings.append(float(movieContainer.find('div', class_ = 'inline-block ratings-imdb-rating').strong.text))
        else:
            ratings.append(float(0))
        if movieContainer.find('span', attrs = {'name':'nv'}) is not None:
            votes.append(int(movieContainer.find('span', attrs = {'name':'nv'})['data-value']))
        else:
            votes.append(int(0))

dataframe = pd.DataFrame({'Id':range(1,len(movies)+1),
                        'MovieName':movies,
                        'ReleaseYear':years,
                        'ImdbRating':ratings,
                        'Metascore':metascores,
                        'Votes':votes}).set_index('Id')

dataframe.to_csv('imdbTop50From2000To2019.csv')