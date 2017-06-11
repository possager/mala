#_*_coding:utf-8_*_
import requests
import cookielib
import MySQLdb
import time
from bs4 import BeautifulSoup
import random

class personalInfoGet:
    def __init__(self):
        self.connect = MySQLdb.connect(host='127.0.0.1', user='root', passwd='asd123456', db='mala', charset='utf8')
        self.cursor = self.connect.cursor()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        }

    def personalInfoGetByOrder(self):
        session1=requests.session()
        cookie1=cookielib.LWPCookieJar()
        session1.cookies=cookie1
        session1.headers=session1.headers

        def personalInfoget(urluid):
            response=session1.request(method='GET',url=urluid)
            datasoup=BeautifulSoup(response.text,'lxml')
            for i1 in datasoup.select('#statistic_content > div > ul > li'):
                try:
                    number=i1.text.split(': ')[1]
                    print number
                    print int(number)
                except Exception as e:
                    print e

            for i2 in datasoup.select('#visitor_content > ul > li'):#访客记录查询
                print i2.text


        def friendinfoGet(urlfriendinfo):
            urlfriendinfo1=urlfriendinfo+'&do=friend&view=me&from=space'
            responsefriendinfo=session1.request(method='GET',url=urlfriendinfo1)
            datasoupfriendinfo=BeautifulSoup(responsefriendinfo.text,'lxml')
            for ii1 in datasoupfriendinfo.select('#ct > div.mn > div > div.bm_c > ul > li'):
                print ii1.text


        personalInfoget('http://home.mala.cn/home.php?mod=space&uid=752731')
        # friendinfoGet('http://home.mala.cn/home.php?mod=space&uid=752731')

if __name__ == '__main__':
    thisclass=personalInfoGet()
    thisclass.personalInfoGetByOrder()