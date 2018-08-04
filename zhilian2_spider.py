"""
zhilian_spider.py 请求智联职位列表网页，获得的响应没有包含职位信息
学习后发现，网页源代码并没有职位信息的静态信息
职位信息由网页加载完成后通过ajax动态加载的
"""

import requests
import json
import re


def get_r(url):
    """
    访问url获取响应
    :return: r.json
    """
    r = requests.get(url, headers=header)
    r_data = r.json()
    return r_data


def get_data(r_data):
    """
    获取响应json中所要数据
    :return:
    """
    results = r_data['data']['results']
    for result in results:
        data = {}
        data['company_name'] = result['company']['name']
        # 筛除黑名单内企业
        if data['company_name'] in blacklist:
            continue
        data['company_size'] = result['company']['size']['name']
        data['compant_url'] = result['company']['url']
        data['work_year'] = result['workingExp']['name']
        data['educating'] = result['eduLevel']['name']
        data['job_name'] = result['jobName']
        data['job_url'] = result['positionURL']

        yield data

def save_data(data):
    """
    保存所要数据
    :return:
    """
    with open('zhilian.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def main():
    """
    主程序
    """
    all_list = []
    # 多页查询，更改range，即爬相应页码
    for page in range(0,5):
        start_url = "https://fe-api.zhaopin.com/c/i/sou?start={}&pageSize=60&cityId=765&workExperience=-1&education=-1&companyType=-1&employmentType=-1&jobWelfareTag=-1&kw=python&kt=3&lastUrlQuery=%7B%22jl%22:%22765%22,%22kw%22:%22python%22,%22kt%22:%223%22%7D".format(
            60 * page)
        r_data = get_r(start_url)
        data_list = list(get_data(r_data))
        all_list += data_list
    save_data(all_list)


if __name__ == '__main__':
    # 企业黑名单，不收集黑名单内企业
    blacklist = []
    with open('blacklist.txt', 'r', encoding='utf-8') as f:
        for line in f.readlines():
            blacklist.append(line.strip())
    header = {'Cookie': 'NTKF_T2D_CLIENTID=guest3BCE29C5-A4A9-7A30-611B-9E195FC1BEF7; zg_did=%7B%22did%22%3A%20%22162b9c5eb2218b-078b816deefcf5-3a614f0b-1fa400-162b9c5eb23b4e%22%7D; dywem=95841923.y; _jzqy=1.1523070858.1523802487.1.jzqsr=baidu.-; __xsptplus30=30.1.1523882441.1523882441.1%234%7C%7C%7C%7C%7C%23%23LZaPgiCCZk7od7gppXXIhSo1_9AZeb_H%23; _jzqa=1.2093824724367997700.1523070858.1523802487.1523882445.7; _jzqx=1.1523882445.1523882445.1.jzqsr=passport%2Ezhaopin%2Ecom|jzqct=/account/register.-; zg_08c5bcee6e9a4c0594a5d34b79b9622a=%7B%22sid%22%3A%201523882447491%2C%22updated%22%3A%201523882447491%2C%22info%22%3A%201523535178534%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22%22%7D; dywea=95841923.1858752527188149500.1523070858.1523882372.1533370373.8; dywec=95841923; dywez=95841923.1533370373.8.8.dywecsr=baidu|dyweccn=(organic)|dywecmd=organic; sts_deviceid=16503ff139fa39-00cc8aab81cdc5-3a614f0b-2073600-16503ff13a0abb; sts_sg=1; sts_sid=16503ff13a528-0dd778ebdf5eab-3a614f0b-2073600-16503ff13a6c36; zp_src_url=https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3D3SLQdS5dk_hHUq6SfHMRN3MkJOe-E7FoXMrjdGzxjTV3JUO9Tb-wY58cbLpnSPpa%26wd%3D%26eqid%3Dc6533cd90000b433000000055b656001; urlfrom=121114583; urlfrom2=121114583; adfcid=www.baidu.com; adfcid2=www.baidu.com; adfbid=0; adfbid2=0; __utma=269921210.2078648467.1523070858.1523882392.1533370373.8; __utmc=269921210; __utmz=269921210.1533370373.8.8.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; ZP_OLD_FLAG=false; Hm_lvt_38ba284938d5eddca645bb5e02a02006=1533370380; LastCity=%E6%B7%B1%E5%9C%B3; LastCity%5Fid=765; dyweb=95841923.3.10.1533370373; __utmb=269921210.3.10.1533370373; ZL_REPORT_GLOBAL={%22sou%22:{%22actionIdFromSou%22:%2209922263-2337-4eb6-95fb-23fef91b2f4a-sou%22%2C%22funczone%22:%22smart_matching%22}}; GUID=8f10b2541046444cac4db01b702a7243; Hm_lpvt_38ba284938d5eddca645bb5e02a02006=1533370434; sts_evtseq=10',
              'Referer': 'https://sou.zhaopin.com/?jl=765&kw=python&kt=3',
              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}
    main()