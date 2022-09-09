from bs4 import BeautifulSoup
import requests
import json


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


scrap = scrap_top_list()


def scrap_movie_detail(movie_url):
    page = requests.get(movie_url)
    soup = BeautifulSoup(page.text, 'html.parser')

    # scrap movie name
    name = soup.find('h1', class_="sc-b73cd867-0 fbOhB").get_text()

    # runtime scrap
    run = soup.find('div', class_="sc-f65f65be-0 ktSkVi")
    print(run.get_text())
    time = run.find_all('ul')
    li = []
    runtime1 = 0
    for i in time:
        li.append(i.get_text())
    for i in li:
        if len(i) == 6:
            s = ""
            for j in i:
                if j.isdigit():
                    s += j
                else:
                    s += ""
            runtime1 = int(s[0])*60+(int(s[2])+int(s[1])*10)
    # scrap  bio
    bio = soup.find("span", attrs={"data-testid": "plot-xs_to_m"}).text

    # scrap director name
    d_name = []
    director_name = soup.find(
        'div', class_="ipc-metadata-list-item__content-container")
    x = director_name.find_all("li", class_="ipc-inline-list__item")
    for i in x:
        d_name.append(i.a.get_text())

    # in this div i get country and laungauge details
    country = soup.find(
        "li", attrs={"data-testid": "title-details-origin"}).find("a").text
    language = []
    language_name = soup.find(
        "li", attrs={"data-testid": "title-details-languages"})
    x = language_name.find_all("li", class_="ipc-inline-list__item")
    for i in x:
        language.append(i.a.get_text())

    # scrap poster image url
    poster_image_url = soup.find("img", class_="ipc-image")["src"]

    # scrap genre
    li1 = []
    gen = soup.find('div', attrs={"data-testid": "genres"}).a.text
    li1.append(gen)

    # scrap contery name
    con = soup.find('li', attrs={"data-testid": "title-details-origin"}).a.text

    detail["country"] = con
    detail["genre"] = li1
    detail["name"] = name
    detail["Director"] = d_name
    detail["Language"] = language
    detail['bio'] = bio
    detail["runtime"] = runtime1
    detail["Poster_image_url"] = poster_image_url

    return detail


detail = {'name': "", "Director": "", "country": '', "Language": "",
          "Poster_image_url": "", "runtime": "", 'genre': ""}

print("loading.....................")
url = scrap[0]['url']
p = (scrap_movie_detail(url))

with open("task4.json", "w") as t4:
    json.dump(p, t4, indent=6)
