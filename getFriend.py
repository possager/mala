import requests
import cookielib
import MySQLdb
import time
from bs4 import BeautifulSoup
import random

class FriendGet:
    def __init__(self):
        self.connect = MySQLdb.connect(host='127.0.0.1', user='root', passwd='asd123456', db='mala', charset='utf8')
        self.cursor = self.connect.cursor()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        }

    def FriendGetByOrder(self):
        session1=requests.session()
        cookie1=cookielib.LWPCookieJar()
        session1.cookies=cookie1
        session1.headers=session1.headers

        def friendget(urluid):
            response=session1.request(method='GET',url=urluid)
            datasoup=BeautifulSoup(response.text,'lxml')
            for i1 in datasoup.select('#statistic_content > div > ul > li'):
                print i1.text
            for i2 in datasoup.select('#visitor_content > ul > li'):
                print i2.text



        friendget('http://home.mala.cn/home.php?mod=space&uid=4115663')

if __name__ == '__main__':
    thisclass=FriendGet()
    thisclass.FriendGetByOrder()