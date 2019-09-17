import pandas as pd
from requests import get
from bs4 import BeautifulSoup

def webScrapper(url):
    response = get(url)
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

if __name__ == '__main__':
    movies, years, ratings, metascores, votes = [],[],[],[],[]
    urls = ['https://www.imdb.com/search/title/?title_type=feature&release_date='+str(i) for i in range(2000,2004)]
    for url in urls:
        webScrapper(url)
    dataframe = pd.DataFrame({'Id':range(1,len(movies)+1),
                            'MovieName':movies,
                            'ReleaseYear':years,
                            'ImdbRating':ratings,
                            'Metascore':metascores,
                            'Votes':votes}).set_index('Id')
    
    filename = 'imdbtest'
    dataframe.to_csv(filename)