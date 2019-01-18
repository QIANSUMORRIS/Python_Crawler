#_*_coding:utf-8_*_
import os
import time
import requests
from lxml import etree

url = 'http://maoyan.com/films'
headers = {
'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
}
def clear(s):
    return s.replace(' ','').replace('\n','')
page=0
while True:
    r = requests.get(url,headers=headers).content.decode('utf-8')
    # print(r)
    html = etree.HTML(r)
    content = html.xpath('//dd')
    # print(len(content))
    # exit()
    num=1
    for i in content:
        title = i.xpath('./div[2]/a/text()')[0]
        try:
            grade_movie = i.xpath('./div[3]/i[1]/text()')[0] + i.xpath('./div[3]/i[2]/text()')[0]
        except:
            pass
        page_link = 'http://maoyan.com' + i.xpath('./div[2]/a/@href')[0]
        r2 = requests.get(page_link,headers=headers).content.decode('utf-8')
        html2 = etree.HTML(r2)
        location_movie = html2.xpath('//div[@class="movie-brief-container"]/ul/li[2]/text()')[0]
        location_movie = clear(location_movie)
        date_movie =  html2.xpath('//div[@class="movie-brief-container"]/ul/li[3]/text()')[0]
        pic_movie = html2.xpath('//div[@class="avatar-shadow"]/img/@src')[0]
        r_img = requests.get(pic_movie,headers=headers,stream=True)
        # img_path = os.path.dirname(__file__)
        # img_path = os.path.join(img_path,'movie_img/')
        # img_path = img_path + title + '.jpg'
        with open('movie_img/'+title+'.jpg','wb') as file:
            for i in r_img.iter_content(1024):
                file.write(i)
        with open('movie_info.csv','a+') as file2:
            file2.write(title+','+grade_movie+','+location_movie+','+date_movie+'\n')
        print('爬取第{}页{}部电影'.format(page+1,num))
        num+=1
        time.sleep(0.5)

    if page<4:
        page+=1
        url = 'http://maoyan.com/films?offset='+str(page*30)
        time.sleep(0.5)
    else:
        break
