import requests
from bs4 import BeautifulSoup
import re
import os

header = {'Referer': 'http://www.mmjpg.com',
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) \
          AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}

def GetSetAmount():
    homepage = 'http://www.mmjpg.com'
    r_homepage = requests.get(homepage, headers=header)
    if r_homepage.status_code == 200:
        print('主页正常访问!')
    print('encoding', r_homepage.encoding)
    print('appencoding', r_homepage.encoding)

    r_homepage.encoding = r_homepage.apparent_encoding
    html_homepage = r_homepage.text
    suop_homepage = BeautifulSoup(html_homepage, 'html.parser')

    LatestImg_url = suop_homepage.img.attrs['src']

    print('网站当前有: ', LatestImg_url[-8: -4], '个图集')
    SetAmount = LatestImg_url[-8: -4]
    return SetAmount


def GetPicSet_url():
    setamount = int(GetSetAmount())
    global Set_n
    for Set_n in range(1, setamount+1):
        yield 'http://www.mmjpg.com/mm/'+str(Set_n)

# 获取每个图集的图片数量
def GetPicAmount_EverySet(PicSet_url):
    r_set = requests.get(PicSet_url, headers=header)
    r_set.encoding = r_set.apparent_encoding
    html_set = r_set.text
    soup_set = BeautifulSoup(html_set, 'html.parser')
    tag_pagenumber = soup_set.find_all(href = re.compile('^/mm/'))
    tag_lastpage = tag_pagenumber[6]
    PicAmount = tag_lastpage.string
    return PicAmount

# 获得每个图片的url
def GetImg_url(Pic_url):
    r_pic = requests.get(Pic_url, headers=header)
    r_pic.encoding = r_pic.apparent_encoding
    html_pic = r_pic.text
    soup_pic = BeautifulSoup(html_pic, 'html.parser')
    global set_name
    set_name = soup_pic.h2.string
    # 把相同图集图片的后缀去掉
    set_name = re.sub(r'\([0-9]+\)', '', set_name)

    imgTag = soup_pic.find('img')
    Img_url = imgTag.attrs['src']
    return Img_url

# 保存图片
def GetJpg():
    for PicSet_url in GetPicSet_url():
        global Set_n
        maxpage_Set = int(GetPicAmount_EverySet(PicSet_url))
        for pagenumber in range(1, maxpage_Set+1):
            PicWeb_url = 'http://www.mmjpg.com/mm/' + str(Set_n) + '/' + str(pagenumber)
            Img_url = GetImg_url(PicWeb_url)
            content = requests.get(Img_url, headers=header).content
            global set_name
            # Pic_name = r'C:\Users\MJR\Desktop\MM\\'+set_name + str(pagenumber) + '.jpg'
            # 分文件夹存放每个图集
            Pic_dir = os.path.join(r'C:\Users\MJR\Desktop\MM\\', set_name)
            if not os.path.exists(Pic_dir):
                os.mkdir(Pic_dir)
            # 文件全路径
            Pic_name = os.path.join(Pic_dir, str(pagenumber) + '.jpg')
            if os.path.exists(Pic_name):
                print('文件已存在:', Pic_name)
                continue

            with open(Pic_name, 'wb') as f:
                f.write(content)
            print('已保存第', Set_n, '个图集的第', pagenumber, '张图片')


GetJpg()



