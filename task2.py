from bs4 import BeautifulSoup
import requests

url = 'https://www.imdb.com/chart/top/?ref_=nv_mv_250'
page = requests.get(url)

soup = BeautifulSoup(page.text, 'html.parser')


def scrap_top_list():
    main_div = soup.find('div', class_='lister')
    tbody = main_div.find('tbody', class_='lister-list')
    trs = tbody.find_all('tr')

    movie_ranks = []
    movie_name = []
    year_of_realease = []
    movie_urls = []
    movie_ratings = []

    for tr in trs:
        position = tr.find('td', class_='titleColumn').get_text().strip()
        rank = ""
        for i in position:
            if "." not in i:
                rank += i
            else:
                break
        movie_ranks.append(rank)

        title = tr.find('td', class_='titleColumn').a.get_text()
        movie_name.append(title)

        year = tr.find('td', class_='titleColumn').span.get_text()
        year_of_realease.append(year)

        ra = tr.find('td', "ratingColumn imdbRating").strong.get_text()
        movie_ratings.append(ra)

        link = tr.find('td', class_='titleColumn').a['href']
        movie_link = 'https://www.imdb.com'+link
        movie_urls.append(movie_link)

    top_movie = []
    details = {'position': '', 'name': '', 'year': '', 'rating': '', 'url': ''}
    for i in range(len(movie_name)):
        details['position'] = int(movie_ranks[i])
        details['name'] = str(movie_name[i])
        details['rating'] = float(movie_ratings[i])
        year_of_realease[i] = year_of_realease[i][1:5]
        details['year'] = year_of_realease[i]
        details['url'] = movie_urls[i]
        top_movie.append(details.copy())
        details = {'position': '', 'name': '',
                   'year': '', 'rating': '', 'url': ''}
    return top_movie


scraped = scrap_top_list()


def group_by_year(movies):
    years = []
    for i in movies:
        year = i['year']
        if year not in years:
            years.append(year)
    years.sort(reverse=False)
    movies_dict = {i: [] for i in years}
    for i in movies:
        year = i['year']
        for x in movies_dict:
            s = str(x)
            s1 = str(year)
            if s == s1:
                movies_dict[x].append(i)
    return movies_dict


a = group_by_year(scraped)
print(a)
