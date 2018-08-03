import os
import re
import requests
import pprint
import json

from bs4 import BeautifulSoup


def get_r(url):
    r = requests.get(url)
    return r


def parse(r):
    soup = BeautifulSoup(r.text, 'html.parser')




    movie_list = soup.find_all('div', attrs={'class': 'item'})

    result_list = []
    for movie in movie_list:
        movdict = {}
        movdict['title'] = movie.find('span', class_='title').text

        movdict['score'] = movie.find('span', attrs={'class': 'rating_num'}).text
        movdict['quote'] = movie.find('span', attrs={'class': 'inq'}).text
        star = movie.find('div', attrs={'class': 'star'})
        movdict['comment_num'] = star.find_all('span')[-1].text
        result_list.append(movdict)
    next = soup.find('link', attrs={'rel': 'next'})
    if next:
        next_url = next['href']
        r = get_r(baseurl+next_url)
        parse(r)

    return result_list


def write_json(result):
    with open('result.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=4, ensure_ascii=False)


# print(result_list)
# pp = pprint.PrettyPrinter(indent=4)
# pp.pprint(result_list)


def main():
    # 多页查
    r = get_r(baseurl)
    parse(r)
    write_json(result_list)


if __name__ == '__main__':
    baseurl = 'https://movie.douban.com/top250'
    result_list = []
    main()
