"""
智联招聘，深圳python岗爬虫
"""
import requests
import json

from bs4 import BeautifulSoup

class ZhiLian():
    def __init__(self):
        self.start_url = 'https://sou.zhaopin.com'
        self.company_base_url = 'https://company.zhaopin.com'
        self.blacklist = []
        self.header = {'Referer': 'https://www.zhaopin.com/',
                       'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) \
                       AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
                       'Host': 'sou.zhaopin.com'}

        with open('cookie.txt', 'r') as f:
            self.header['cookie'] = f.read()

    def get_r(self, url):
        r = requests.get(url, headers=self.header)
        return r.text

    def parse(self, r):
        soup = BeautifulSoup(r, 'html.parser')
        job_list = soup.find_all('div', {'class': 'listItemBox clearfix'})
        for job in job_list:
            yield {
                'job_name': job.a.span.string
            }

    def parse_company(self):
        pass

    def write_json(self, result):
        with open('zhilian.json', 'w', encoding='utf-8')as f:
            json.dump(result, f, ensure_ascii=False, indent=4)

    def start(self):
        r = self.get_r(self.start_url)
        result = list(self.parse(r))
        self.write_json(result)


zhilian = ZhiLian()
zhilian.start()
