"""
代理池运行主程序
开启两个进程
一个运行获取西刺代理的爬虫
一个运行验证代理是否有效
"""

from multiprocessing import Process
from xicidaili import get_ip, valid
import time
import pymysql

# 是否调用爬虫函数的前置判断函数
# 获取数据库中ip数量，小于一定值才调用爬虫补充代理池
def process_get():
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
            # ips_ipmodel（代理池表）表中数据数量
            count = cursor.execute(sql)
        connection.commit()
    finally:
        connection.close()
    # 若数据数量小于20个则调用爬虫
    if count < 20:
        get_ip.Spider().main()

# 调用验证函数
def process_valid():
    valid.main()

# 主程序
def main():
    while True:
        print('自动获取与检测ip本轮开始')
        ps = []

        # 爬虫进程
        p1 = Process(target=process_get)
        p1.start()
        ps.append(p1)
        time.sleep(1)
        # 验证进程
        p2 = Process(target=process_valid)
        p2.start()
        ps.append(p2)

        # 同步进程，因为爬虫很快，验证进程较慢，确保每次循环都按照先判断调用爬虫，再验证
        for p in ps:
            p.join()
        print('自动获取与检测ip本轮结束')
        time.sleep(10)

if __name__ == '__main__':
    main()