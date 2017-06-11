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
                print ii1.select('h4 > a ')[0].get('title')#用户名
                print ii1.select('h4 > a')[0].get('href')#用户的链接

            nextpage=datasoupfriendinfo.select('#ct > div.mn > div > div.bm_c > div > div > a.nxt')
            if nextpage:
                nexturl1=nextpage[0].get('href')
                nexturl=nexturl1.replace('&amp','').replace(';','&')
                print nexturl
                friendinfoGet(nexturl)


        def liuyanban(urlliuyanban):#留言板处理
            responseliuyanban=session1.request(method='GET',url=urlliuyanban)
            datasoupliuyanban=BeautifulSoup(responseliuyanban.text,'lxml')
            for iii1 in datasoupliuyanban.select('#comment_ul > dl.bbda.cl'):
                # print iii1.select('dd.m.avt > a')[0].get('href')
                print iii1.select('dt > a')[0].get('href')#留言人的链接
                print iii1.select('dt > a')[0].text#留言人的名称
                print iii1.select('dd[id]')[0].text#留言人的留言内容
            print datasoupliuyanban
            nextpage=datasoupliuyanban.select('div.pgs.cl.mtm > div.pg > a.nxt')#这里功能不能实现,因为网页返回里边没有对应的下一页的url,可能需要处理js,反正各个板块是分开的,将来再回来写这一块
            if nextpage:
                nexturl=nextpage[0].get('href')
                print nexturl



        personalInfoget('http://home.mala.cn/home.php?mod=space&uid=752731')
        # liuyanban('http://home.mala.cn/home.php?mod=space&uid=752731')
        friendinfoGet('http://home.mala.cn/home.php?mod=space&uid=752731')

if __name__ == '__main__':
    thisclass=personalInfoGet()
    thisclass.personalInfoGetByOrder()