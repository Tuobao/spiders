import requests
import json

from bs4 import BeautifulSoup


class Stackof():
    """
    爬虫，获取stackoverflow关键词python下的最新一页数据，并非search，是
    stackoverflow里有的标签，url会不同
    """
    def __init__(self):
        self.result_list = []
        self.base_url = 'https://stackoverflow.com'
        self.start_url = 'https://stackoverflow.com/questions/tagged/python'

    def get_r(self, url):
        r = requests.get(url).text
        return r

    def parse(self, text):
        soup = BeautifulSoup(text, 'html.parser')
        question_list = soup.find_all('div', {'class': 'question-summary'})

        for question in question_list:
            result = {}
            result['title'] = question.h3.a.string
            result['detail_url'] = self.base_url + question.h3.a['href']
            # 这里添加需要的属性即可

            self.result_list.append(result)

    def write_json(self):
        with open('stack.json', 'w', encoding='utf-8') as f:
            json.dump(self.result_list, f, ensure_ascii=False, indent=4)
            print('已导出至stack.json')

    def start(self):
        r = self.get_r(self.start_url)
        self.parse(r)
        self.write_json()


stack = Stackof()
stack.start()
