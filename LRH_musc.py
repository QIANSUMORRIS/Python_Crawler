#_*_coding:utf-8_*_
from lxml import etree
import time
import requests
import json

url = 'https://u.y.qq.com/cgi-bin/musicu.fcg?callback=getUCGI9249430843284883&g_tk=9794679&jsonpCallback=getUCGI9249430843284883&loginUin=361486939&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0&data=%7B%22singerAlbum%22%3A%7B%22method%22%3A%22get_singer_album%22%2C%22param%22%3A%7B%22singermid%22%3A%22000aHmbL2aPXWH%22%2C%22order%22%3A%22time%22%2C%22begin%22%3A0%2C%22num%22%3A30%2C%22exstatus%22%3A1%7D%2C%22module%22%3A%22music.web_singer_info_svr%22%7D%7D'
headers = {
'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
}
r = requests.get(url,headers=headers).text
#dict格式
# print(r)
r = r[24:-1]
# print(r)
album_js = json.loads(r)
num1=1
for i in range(13):
    album_mid = album_js['singerAlbum']['data']['list'][i]['album_mid']
    get_album_page = 'https://y.qq.com/n/yqq/album/' + str(album_mid) + '.html#stat=y_new.singer.album.album_pic'
    # print(get_album_page)
    r2 = requests.get(get_album_page,headers=headers).text
    html2 = etree.HTML(r2)
    album_id = html2.xpath('//ul[@class="songlist__list"]/li')[1:]
    # print((len(album_id)))
    # exit()
    num2=1
    for j in album_id:
        soundid = j.xpath('//div[@class="songlist__songname"]/span/a/@href')[0][22:-5]
        with open('soundmin.txt','a+',encoding='utf-8') as file:
            file.write('=======================' + soundid + '======================='+'\n')
        print('爬取的是{}张专辑的第{}首歌'.format(num1,num2))
        num2 += 1
        time.sleep(0.5)
    num1 += 1
    time.sleep(0.5)




