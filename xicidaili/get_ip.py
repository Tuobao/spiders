"""
西刺代理爬虫，存mysql
设置只爬第一页，多页加翻页操作或拼接url
"""

import requests
import time

import pymysql
from pymongo import MongoClient
from bs4 import BeautifulSoup


class Spider:

    def __init__(self):
        # 一页五十个，目前用的不多，就爬一页的
        self.start_url = 'http://www.xicidaili.com/nn'
        self.data = []
        self.header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
                       'Cookie': '_free_proxy_session=BAh7B0kiD3Nlc3Npb25faWQGOgZFVEkiJWY0YjA4NGQ4M2E2ZTQ0OGM4MjFkNDI4NTVmYjYwZTNmBjsAVEkiEF9jc3JmX3Rva2VuBjsARkkiMWtQWGdQY2llM3dka3hjeTBGL3p1ZW52MTJEaWdEZHZScXA0Y3FMRUFOTWM9BjsARg%3D%3D--996dbb4b47e9ee9f66b1502a91649b6c677a6f93; Hm_lvt_0cf76c77469e965d2957f0553e6ecf59=1534130264; Hm_lpvt_0cf76c77469e965d2957f0553e6ecf59=1534132305',}

    def get_r(self, url):
        r = requests.get(url, headers=self.header)
        return r.text

    def parse(self, r):
        soup = BeautifulSoup(r, 'html.parser')
        items = soup.find_all('tr', {'class': 'odd'})

        for item in items:
            dic = {}
            tds = item.find_all('td')
            dic['ip'] = tds[1].get_text()
            dic['port'] = tds[2].get_text()
            dic['type'] = tds[5].get_text()

            self.data.append(dic)

    ''' mongodb
        def save_db(self):
            client = MongoClient('localhost', 27017)
            db = client['proxies']
            table = db['ips']
            for row in self.data:
                if table.insert(row):
                    print('ip %s 已储存'%row['ip'])
    '''

    # 保存数据
    def save_db(self):
        # mysql配置
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='1234',
                                     db='proxies',
                                     charset='utf8',
                                     cursorclass=pymysql.cursors.DictCursor)
        # 查询是否存在
        exsit_sql =  "select * from ips_ipmodel where ip = %s"
        # 插入新数据
        sql = 'insert into ips_ipmodel(ip, port, type) value (%s, %s, %s)'
        try:
            with connection.cursor() as cursor:
                for row in self.data:
                    # 查询该ip，查看是否存在，不重复添加
                    cursor.execute(exsit_sql, (row['ip'], ))
                    if cursor.fetchone():
                        print("ip已存在:", row['ip'])
                    else:
                        cursor.execute(sql, (row['ip'], row['port'], row['type']))
            connection.commit()
        finally:
            connection.close()


    def main(self):
        print("开始解析")
        t1 = time.time()
        r = self.get_r(self.start_url)
        self.parse(r)
        print('解析完毕，保存数据至数据库')
        self.save_db()
        t2 = time.time()
        print("数据保存完成，用时:", t2-t1)

if __name__ == '__main__':
    Spider().main()