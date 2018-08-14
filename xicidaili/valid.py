"""
代理池ip有效性验证函数
数据库刚开始选用mongodb，后来修改为mysql，配置留作参考
启用多线程验证
"""

from pymongo import MongoClient
import pymysql
import requests
from queue import Queue
from threading import Thread

# 全局变量
ips = Queue()
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
          }

# 主程序
def main():
    '''
    # mongodb配置
    client = MongoClient('localhost', 27017)
    db = client['proxies']
    table = db['ips']

    lis = table.find()
    '''

    # mysql配置
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='1234',
                                 db='proxies',
                                 charset='utf8',
                                 cursorclass=pymysql.cursors.DictCursor)

    sql = 'select * from ips_ipmodel'
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql)
            # 获取代理池所有数据
            lis = cursor.fetchall()
        connection.commit()
    finally:
        connection.close()

    # 将数据加入队列
    global ips
    for ip in lis:
        ips.put(ip)

    # 开启多线程
    ths = []
    for _ in range(8):
        th = Thread(target=valid_ip)
        th.start()
        ths.append(th)
    # 结束所有任务前，同步一下线程
    for th in ths:
        th.join()


# 验证
def valid_ip():
    global ips
    # 队列的用法，.get()获取一条数据，然后把索引移到下一位，故达到遍历效果
    # .empty() 队列的数据被get获取完后，该返回值为True
    while not ips.empty():
        ip = ips.get()
        # 拼接requests代理参数
        proxy = {'http': ip['ip']+':'+ip['port'],
                 'https': ip['ip'] + ':' + ip['port']}
        try:
            # 超时设置为5s
            r = requests.get('http://icanhazip.com/', headers=header, proxies=proxy, timeout=5)
            # 请求正常
            if r.status_code == 200:
                print('ip正常工作:', ip['ip'])
            else:
                rm_ip(ip)
                print('删除无效ip:', ip['ip'])
        except:
            rm_ip(ip)
            print('删除超时无效ip:', ip['ip'])

# 数据库删除操作
def rm_ip(ip):
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='1234',
                                 db='proxies',
                                 charset='utf8',
                                 cursorclass=pymysql.cursors.DictCursor)

    sql = 'delete from ips_ipmodel where ip = %s'
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql, ip['ip'])
            lis = cursor.fetchall()
        connection.commit()
    finally:
        connection.close()


if __name__ == '__main__':
    main()
