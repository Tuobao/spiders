"""
douban250
requests  Queue  Beautifulsoup Thread
一级页面抓取二级页面的url至队列。
二级页面从队列中拿url解析数据。

"""
import requests
import time
from threading import Thread

from queue import Queue
from bs4 import BeautifulSoup
from pymongo import MongoClient


def run_time(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        func(*args, **kwargs)
        end = time.time()
        print('用时:', end - start)
    return wrapper



class Spider():

    def __init__(self):
        self.start_url = 'https://movie.douban.com/top250'
        self.qurl = Queue()
        self.item_num = 5 # 每页只取前五个
        self.thread_num = 5 # 线程数
        self.has_next = True
        self.data = []

    def parser_frist(self, url):
        print('解析开始')
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        items = soup.find_all('div', {'class': 'hd'})[:self.item_num]

        for item in items:
            url = item.a['href']
            # 二级页面url存入队列
            self.qurl.put(url)

        # 判断是否还有下一页
        next_bottom = soup.find('span', {'class': 'next'}).a
        if next_bottom:
            self.parser_frist(self.start_url + next_bottom['href'])
        else:
            self.has_next = False

    def parser_second(self):
        while self.has_next or not self.qurl.empty():
            url = self.qurl.get()
            r = requests.get(url)
            soup = BeautifulSoup(r.text, 'html.parser')
            dic = {}

            dic['rank'] = soup.find('span', {'class': 'top250-no'}).get_text()
            dic['title'] = soup.find('span', {'property': 'v:itemreviewed'}).get_text()
            dic['director'] = soup.find('span', {'class': 'attrs'}).a.get_text()
            # 其他数据

            self.data.append(dic)

    @run_time
    def run(self):
        ths = []

        th1 = Thread(target=self.parser_frist, args=(self.start_url, ))
        th1.start()
        ths.append(th1)

        for _ in range(self.thread_num):
            th2 = Thread(target=self.parser_second)
            th2.start()
            ths.append(th2)

        for th in ths:
            th.join()
        print('解析完毕，开始存储数据')
        # 存数据

        client = MongoClient('localhost', 27017)
        douban = client['douban']
        table = douban['top250']
        for row in self.data:
            if table.insert(row):
                print("保存 %s 数据成功" %row['title'])



if __name__ == '__main__':
    Spider().run()