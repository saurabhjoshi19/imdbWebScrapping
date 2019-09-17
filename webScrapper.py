import pandas as pd
from multiprocessing import Pool
from requests import get
from bs4 import BeautifulSoup

def webScrapper(url):
    movies, years, ratings, metascores, votes = [],[],[],[],[]
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
    return (movies, years, ratings, metascores, votes)

if __name__ == '__main__':
    filename = 'imdbTop50From2000To2019.csv'
    urls = ['https://www.imdb.com/search/title/?title_type=feature&release_date='+str(i) for i in range(2000,2020)]
    movies, years, ratings, metascores, votes = [],[],[],[],[]
    pool = Pool(10)
    result = pool.map(webScrapper, urls)
    pool.terminate()
    pool.join()
    for (moviesPerUrl, yearsPerUrl, ratingsPerUrl, metascoresPerUrl, votesPerUrl) in result:
        movies.extend(moviesPerUrl)
        years.extend(yearsPerUrl)
        ratings.extend(ratingsPerUrl)
        metascores.extend(metascoresPerUrl)
        votes.extend(votesPerUrl)
    dataframe = pd.DataFrame({'Id':range(1,len(movies)+1),
                            'MovieName':movies,
                            'ReleaseYear':years,
                            'ImdbRating':ratings,
                            'Metascore':metascores,
                            'Votes':votes}).set_index('Id')
    dataframe.to_csv(filename)