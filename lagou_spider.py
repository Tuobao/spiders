"""
抓取拉勾网首页上技术栏，所有岗位信息
需改善的地方：多进程抓取，增加代理池
"""


import random
import time

import requests
import pymongo
from bs4 import BeautifulSoup


def get_r(url):
    proxy = random.choice(proxy_list)
    proxies = {'http': proxy}
    time.sleep(1)
    r = requests.get(url, headers=header, proxies=proxies)
    if r.status_code == 200:
        return r.text
    else:
        return False

# 首页解析技术类所有分类链接
def paser(r):
    soup = BeautifulSoup(r, 'html.parser')
    div_jisu = soup.find('div', {'class': 'menu_box'})
    div_jisu_dn = div_jisu.find('div', {'class': 'menu_sub dn'})
    a_fenlei = div_jisu_dn.find_all('a')

    for a in a_fenlei:
        data = {}
        data['url'] = a['href']
        data['name'] = a.string
        yield data

# 职位列表页解析职位信息
def paser_detail(r):
    soup = BeautifulSoup(r, 'html.parser')
    companys = soup.select('ul > li > div.list_item_top > div.company > div.company_name > a')
    jobNames = soup.select('ul > li > div.list_item_top > div.position > div.p_top > a > h3')
    jobAdds = soup.select('ul > li > div.list_item_top > div.position > div.p_top > a > span > em')
    needYears = soup.select('ul > li > div.list_item_top > div.position > div.p_bot > div.li_b_l')
    moneys = soup.select('ul > li > div.list_item_top > div.position > div.p_bot > div.li_b_l > span')
    for company,jobName,jobAdd,needYear,money in \
            zip(companys, jobNames, jobAdds, needYears, moneys):
        data = {}
        data['company'] = company.get_text()
        data['jobName'] = jobName.get_text()
        data['jobAdd'] = jobAdd.get_text()
        data['needYear'] = needYear.get_text().split('\n')[2]
        data['money'] = money.get_text()

        yield data

# 保存数据到mongodb
def save_data(data_list, name):
    client = pymongo.MongoClient('localhost', 27017)
    lagou = client['lagou']
    # 删除如.NET前的.  因为表名不能以.开头
    name.lstrip('.')
    table = lagou[name]
    for data in data_list:
        if table.insert_one(data):
            print('保存成功:', data['jobName'])


def main():
    r = get_r(start_url)
    category_list = list(paser(r))
    for category in category_list:
        url = category['url']
        name = category['name']
        data_list = []
        # 分页
        for i in range(1, 31):
            page_url = url + '{}/'.format(i)
            r = get_r(page_url)
            if not r:
                pass
            else:
                data_list += list(paser_detail(r))

        save_data(data_list, name)


if __name__ == '__main__':
    start_url = 'https://www.lagou.com/'
    header = {'Cookie': '_ga=GA1.2.1642047146.1523520393; user_trace_token=20180412160633-6a327a3d-3e28-11e8-b747-5254005c3644; LGUID=20180412160633-6a327e30-3e28-11e8-b747-5254005c3644; LG_LOGIN_USER_ID=8c11d28529d2e7746cc316d751619664f856684edf4b064660b1f2519a76a9f4; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; index_location_city=%E6%B7%B1%E5%9C%B3; _gid=GA1.2.1467585809.1533634830; JSESSIONID=ABAAABAAAFCAAEG936BBC7BB4F5073B2C05EF9CBC4EEA7C; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1533544924,1533545201,1533634830,1533697187; _putrc=7499BE2EB71C34F7123F89F2B170EADC; login=true; unick=%E5%90%B4%E5%AE%87%E4%BC%A6; hasDeliver=121; gate_login_token=93b73110808a0e4f87629976dc42c7585f3d98c20ae01ec0a1079d3dc9d63afb; LGSID=20180808113415-eca21cb5-9abb-11e8-b7bd-525400f775ce; SEARCH_ID=69a830c6d9184cf3bfd7cdc01bac80bf; LGRID=20180808114642-a9fe9cd6-9abd-11e8-a341-5254005c3644; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1533700001',
              'Referer': 'https://www.lagou.com/zhaopin/Java/?filterOption=3',
              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}

    proxy_list = ['180.118.73.126:9000',
                  '125.110.71.218:9000',
                  '180.118.135.26:9000',
                  '175.161.14.163:9000',
                  '211.136.127.125:80',
                  '180.118.92.228:9000',
                  '112.95.27.161:8118',
                  '180.118.73.175:9000',
                  '120.79.208.174:1080',
                  '49.81.125.63:9000',
                  '115.223.220.3:9000',
                  '115.218.218.34:9000',
                  '115.223.198.231:9000',
                  '117.90.252.100:9000',
                  '171.92.33.49:9000']

    main()


