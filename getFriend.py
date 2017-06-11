#_*_coding:utf-8_*_
import requests
import cookielib
import MySQLdb
import time
from bs4 import BeautifulSoup
import random
from multiprocessing import pool

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
            numlist=[]
            owneruid=''
            owneruid1='111111111'
            try:
                ownername = datasoup.select('div > div.hm > h2 > a')[0].text
                owneruid1 = urluid.split('uid=')[1]
            except Exception as e:
                print e
            if len(owneruid1) > 9:
                owneruid = int(owneruid1.split('&')[0])
            else:
                owneruid = int(owneruid1)


            for i1 in datasoup.select('#statistic_content > div > ul > li'):
                try:
                    number=i1.text.split(': ')[1]
                    print number
                    numbernum= int(number)
                    numlist.append(numbernum)
                except Exception as e:
                    print e
                    number=0
                    numlist.append(number)
            print numlist



            visitorhref=''
            visitorname=''
            visitortime=''

            ####################这里个人信息栏的信息获取
            try:
                urlgerenxinxi=urluid+'&do=profile'
                print urlgerenxinxi
                responsegerenxinxi=session1.request(method='GET',url=urlgerenxinxi)
                datasoupgerenxinxi=BeautifulSoup(responsegerenxinxi.text,'lxml')
                youxiangrenzheng=0
                shipinrenzheng=1
                ongjianfangwenliang=0
                for i1j1 in datasoupgerenxinxi.select('div.mn > div > div.bm_c > div > div > ul.pf_l.cl.pbm.mbm > li'):
                    if u'未认证' in i1j1.text:
                        shipinrenzheng=0
                    if u'已验证' in i1j1.text:
                        youxiangrenzheng=1
                    if u'空间访问量' in i1j1.text:
                        ongjianfangwenliang=int(i1j1.text.replace(u'空间访问量',''))
                # print youxiangrenzheng,shipinrenzheng,ongjianfangwenliang
                xingbie=0
                shengri='2100-1-1 12:00'
                chushengdi=''
                juzhudi=''
                for i1j2 in datasoupgerenxinxi.select('div.mn > div > div.bm_c > div > div > ul.pf_l.cl > li'):
                    if u'男' in i1j2.text:
                        xingbie=1
                    if u'生日' in i1j2.text and u'年' in i1j2.text:
                        shengri=i1j2.text.replace(u'生日','').replace(u'年','-').replace(u'月','-').replace(u'日','').replace(' ','')
                        # print shengri
                    if u'出生地' in i1j2.text:
                        chushengdi= i1j2.text.replace(u'出生地','')
                        # print chushengdi
                    if u'居住地' in i1j2.text:
                        juzhudi =i1j2.text.replace(u'居住地','')
                    # print shengri
                yonghuzu=datasoupgerenxinxi.select(' div.mn > div > div.bm_c > div > div > ul > li > span > a')[0].text
                print yonghuzu

                zaixianshijian=0
                zhuceshijian='2100-1-1 12:00'
                zuihoufangwen='2100-1-1 12:00'
                shangcihuodongshijian='2100-1-1 12:00'
                shangcifabiaoshijian='2100-1-1 12:00'

                for i1j3 in datasoupgerenxinxi.select('#pbbs > li'):
                    if u'在线时间' in i1j3.text:
                        zaixianshijian= int(i1j3.text.replace(u'在线时间','').split(u' ')[0])
                    if u'注册时间' in i1j3.text:
                        zhuceshijian= i1j3.text.replace(u'注册时间','')
                    if u'最后访问' in i1j3.text:
                        zuihoufangwen= i1j3.text.replace(u'最后访问','')
                    if u'上次活动时间' in i1j3.text:
                        shangcihuodongshijian= i1j3.text.replace(u'上次活动时间','')
                    if u'上次发表时间' in i1j3.text:
                        shangcifabiaoshijian= i1j3.text.replace(u'上次发表时间','')
            except Exception as e:
                print e



            ######################个人信息

            for i2 in datasoup.select('#visitor_content > ul > li'):#访客记录查询
                visitorhref= i2.select(' p > a')[0].get('href')
                visitoruid=int(visitorhref.split('uid=')[1])
                visitorname= i2.select('p > a ')[0].text
                visitortime= i2.select('span.xg2')[0].text
                try:
                    sql_visitor='INSERT INTO mala.visitor (ownername,owneruid,visitorname,visitoruid,visittime) VALUE ("%s",%d,"%s",%d,"%s")'%(ownername,owneruid,visitorname,visitoruid,visitortime)
                    print sql_visitor
                    self.cursor.execute(sql_visitor)
                    self.connect.commit()
                except Exception as e:
                    print e

            try:
                sqlperson='INSERT INTO mala.personalinfo (ownername,owneruid,jifen,huajiao,xiaomijiao,jinbi,haoyou,zhuti,rizhi,xiangce,fenxiang,' \
                          'kongjianfangwenliang,youxiangyanzheng,' \
                          'shipinrenzheng,juzhudi,chushengdi,shangcifabiaoshijian,shangcihuodongshijian,zuihoufangwen,zhuceshijian,zaixianshijian,shengri,xingbie) ' \
                          'VALUE("%s",%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,' \
                          '%d,%d,%d,"%s","%s","%s","%s","%s","%s",%d,"%s",%d)'%(
                    ownername,owneruid,numlist[0],numlist[1],numlist[2],numlist[3],numlist[4],numlist[5],numlist[6],numlist[7],numlist[8],
                    ongjianfangwenliang,youxiangrenzheng,shipinrenzheng,juzhudi,chushengdi,shangcifabiaoshijian,shangcihuodongshijian,zuihoufangwen,zhuceshijian,zaixianshijian,shengri,xingbie
                )
                print sqlperson
                self.cursor.execute(sqlperson)
                self.connect.commit()
            except Exception as e:
                print e


        def friendinfoGet(urlfriendinfo):
            urlfriendinfo1=urlfriendinfo+'&do=friend&view=me&from=space'
            responsefriendinfo=session1.request(method='GET',url=urlfriendinfo1)
            datasoupfriendinfo=BeautifulSoup(responsefriendinfo.text,'lxml')
            try:
                ownername=datasoupfriendinfo.select('div > div.hm > h2 > a')[0].text
            except Exception as e:
                print e
            for ii1 in datasoupfriendinfo.select('#ct > div.mn > div > div.bm_c > ul > li'):
                try:
                    friendname= ii1.select('h4 > a ')[0].get('title')#用户名
                    ownerhref= ii1.select('h4 > a')[0].get('href')#用户的链接
                    frienduid=int(ownerhref.split('uid=')[1])
                    owneruid1=urlfriendinfo.split('uid=')[1]
                    if len(owneruid1)>9:
                        owneruid=int(owneruid1.split('&')[0])
                    else:
                        owneruid=int(owneruid1)


                    sqlperson_friend='INSERT INTO mala.friendshipall (ownername,owneruid,friendname,frienduid) VALUE ("%s",%d,"%s",%d)'%(ownername,owneruid,friendname,frienduid)
                    self.cursor.execute(sqlperson_friend)
                    self.connect.commit()
                    print sqlperson_friend
                except Exception as e:
                    print e



            nextpage=datasoupfriendinfo.select('#ct > div.mn > div > div.bm_c > div > div > a.nxt')
            if nextpage:
                nexturl1=nextpage[0].get('href')
                nexturl=nexturl1.replace('&amp','').replace(';','&')
                print nexturl
                time.sleep(random.randint(2,5))
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


        def run(uid=870):
            personalInfoget('http://home.mala.cn/home.php?mod=space&uid=752731')
            # liuyanban('http://home.mala.cn/home.php?mod=space&uid=752731')
            friendinfoGet('http://home.mala.cn/home.php?mod=space&uid=752731')

        run()

    def numyield(self):
        i=0
        while i < 7305075:
            yield i

if __name__ == '__main__':
    thisclass=personalInfoGet()
    thisclass.personalInfoGetByOrder()