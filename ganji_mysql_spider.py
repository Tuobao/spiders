"""
赶集网柴犬信息，并保存到mysql
"""

import requests
import json
import pymysql

from bs4 import BeautifulSoup


def get_r(url):
    r = requests.get(url, headers=header)
    return r.text


def parse(r):
    soup = BeautifulSoup(r, 'html.parser')
    dog_list = soup.find_all('dl', {'class': 'list-pic info-tworows '})
    for dog in dog_list:
        data = {}
        title = dog.find('a', {'class': 'list-title f14'})
        data['title'] = title.string.strip()
        data['info_url'] = title['href']
        data['price'] = dog.find('span', {'class': 'fc-org f14'}).string
        yield data


def save_mysql(data_list):
    # 创建连接
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='1234',
                                 db='ganji',
                                 charset='utf8',
                                 cursorclass=pymysql.cursors.DictCursor)
    # 新建表
    create_table = '''create table ganji.dog(
    title char(200),
    info_url char(200), 
    price char(200));
    '''
    # 插入数据
    sql = 'insert into dog(title, info_url, price) values (%s,%s,%s)'
    try:
        with connection.cursor() as cursor:
            cursor.execute(create_table)
            for data in data_list:
                cursor.execute(sql, (data['title'], data['info_url'], data['price']))
        connection.commit()
    finally:
        connection.close()


def main():
    r = get_r(start_url)
    data_list = list(parse(r))
    save_mysql(data_list)


if __name__ == '__main__':
    start_url = 'http://cd.ganji.com/chaiquan/'
    header = {'Cookie': 'statistics_clientid=me; ganji_xuuid=f7bb1757-0306-41f9-8384-351018b12003.1533456756381; ganji_uuid=4624666784109291297741; GANJISESSID=7balt4prph83jf1utm0g5648rj; xxzl_deviceid=g0kYiEHU8oRLWBdKaJVVe%2FipyzRv7aiJqfSCOdo1t2aHpP9kvOwSJQSmR7IwYvww; _gl_tracker=%7B%22ca_source%22%3A%22www.baidu.com%22%2C%22ca_name%22%3A%22-%22%2C%22ca_kw%22%3A%22-%22%2C%22ca_id%22%3A%22-%22%2C%22ca_s%22%3A%22seo_baidu%22%2C%22ca_n%22%3A%22-%22%2C%22ca_i%22%3A%22-%22%2C%22sid%22%3A58356467651%2C%22kw%22%3A%22%E5%AE%A0%E7%89%A9%E7%8B%97%22%7D; _wap__utmganji_wap_caInfo_V2=%7B%22ca_name%22%3A%22-%22%2C%22ca_source%22%3A%22-%22%2C%22ca_id%22%3A%22-%22%2C%22ca_kw%22%3A%22-%22%7D; lg=1; __utma=32156897.1906166565.1533456766.1533456766.1533456766.1; __utmc=32156897; __utmz=32156897.1533456766.1.1.utmcsr=cd.ganji.com|utmccn=(referral)|utmcmd=referral|utmcct=/; ganji_login_act=1533456850910; __utmb=32156897.5.10.1533456766; xzfzqtoken=ZRtU6V%2F9%2BKIqqWrpGpz649cVtWEe3UEhOnNkLTxgySn1lqq9F7Bt9umryMshrdHUin35brBb%2F%2FeSODvMgkQULA%3D%3D',
              'Referer': 'http://cd.ganji.com/chaiquan/',
              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}
    main()
