#_*_coding:utf-8_*_
import requests
import cookielib
import MySQLdb
import time
from bs4 import BeautifulSoup
import random
import threading
import pymongo
from multiprocessing import pool

#mysql是个大坑




threadlock=threading.Lock()

class personalInfoGet:
    def __init__(self):
        self.connect = MySQLdb.connect(host='127.0.0.1', user='root', passwd='asd123456', db='mala', charset='utf8')
        self.connect2=MySQLdb.connect(host='127.0.0.1', user='root', passwd='asd123456', db='proxy', charset='utf8')

        self.cursor = self.connect.cursor()
        self.cursor2=self.connect2.cursor()

        self.client=pymongo.MongoClient('localhost',27017)
        self.proxyCOL=self.client['IpProxy2']
        self.proxyDOC=self.proxyCOL['Ip_Live_mala']


        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        }

    def personalInfoGetByOrder(self):
        # session1=requests.session()
        # cookie1=cookielib.LWPCookieJar()
        # session1.cookies=cookie1
        # session1.headers=session1.headers


        ################################################获取代理ip,放进列表中
        # proxylist=[]
        # sqlproxyget = 'SELECT * FROM proxy.mala_proxy_live WHERE errornum > 0'
        # self.cursor2.execute(sqlproxyget)
        # proxylistdata = self.cursor2.fetchall()
        # for i in proxylistdata:
        #     print i[0], '-------->', i[1]
        #     dict1 = {'http': 'http://' + i[0] + ':' + i[1]}
        #     proxylist.append(dict1)





        def personalInfoget(urluid,session1,connect1,cursor1,connect2,cursor2):
            try:
                response=session1.request(method='GET',url=urluid)
                sqlproxy_success='UPDATE proxy.mala_proxy_live SET usednum = usednum+1 WHERE ip ="%s"'%(session1.proxies['http'].replace('http://','').split(':')[0])
                cursor2.execute(sqlproxy_success)
                connect2.commit()
            except Exception as e:
                print e
                # print session1.proxies
                proxyip= session1.proxies['http'].replace('http://','').split(':')[0]
                # print proxyip
                # self.proxyDOC.update({'ip':proxyip},{'$inc':{'errornum':-1}})


                sqldelete='UPDATE proxy.mala_proxy_live SET errornum=errornum-1 WHERE ip ="%s"'%(proxyip)
                print sqldelete
                cursor2.execute(sqldelete)
                connect2.commit()

                return

            datasoup=BeautifulSoup(response.text,'lxml')
            numlist=[]
            owneruid=''
            owneruid1='111111111'

            #后来发在try模块中的变量容易发生错误,因为try若被打断,里边声明变量的语句就不会被执行.所以将变量声明挪到这里.
            visitorhref = ''
            visitorname = ''
            visitortime = ''
            youxiangrenzheng=0
            shipinrenzheng=1
            ongjianfangwenliang=0
            xingbie = 0
            shengri = '2100-01-01 12:00'
            chushengdi = ''
            juzhudi = ''
            zaixianshijian = 0
            zhuceshijian = '2100-01-01 12:00'
            zuihoufangwen = '2100-01-01 12:00'
            shangcihuodongshijian = '2100-01-01 12:00'
            shangcifabiaoshijian = '2100-01-01 12:00'

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
                    number=0
                    numlist.append(number)
            print numlist



            # visitorhref=''
            # visitorname=''
            # visitortime=''

            ####################这里个人信息栏的信息获取
            try:
                urlgerenxinxi=urluid+'&do=profile'
                print urlgerenxinxi
                responsegerenxinxi=session1.request(method='GET',url=urlgerenxinxi)
                datasoupgerenxinxi=BeautifulSoup(responsegerenxinxi.text,'lxml')
                # youxiangrenzheng=0
                # shipinrenzheng=1
                # ongjianfangwenliang=0
                # xingbie = 0
                # shengri = '2100-1-1 12:00'
                # chushengdi = ''
                # juzhudi = ''
                for i1j1 in datasoupgerenxinxi.select('div.mn > div > div.bm_c > div > div > ul.pf_l.cl.pbm.mbm > li'):
                    if u'未认证' in i1j1.text:
                        shipinrenzheng=0
                    if u'已验证' in i1j1.text:
                        youxiangrenzheng=1
                    if u'空间访问量' in i1j1.text:
                        try:
                            ongjianfangwenliang=int(i1j1.text.replace(u'空间访问量',''))
                        except Exception as e:
                            print e
                # print youxiangrenzheng,shipinrenzheng,ongjianfangwenliang

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

                # zaixianshijian=0
                # zhuceshijian='2100-1-1 12:00'
                # zuihoufangwen='2100-1-1 12:00'
                # shangcihuodongshijian='2100-1-1 12:00'
                # shangcifabiaoshijian='2100-1-1 12:00'

                for i1j3 in datasoupgerenxinxi.select('#pbbs > li'):
                    if u'在线时间' in i1j3.text:
                        zaixianshijian= int(i1j3.text.replace(u'在线时间','').split(u' ')[0])
                    if u'注册时间' in i1j3.text:
                        zhuceshijian= i1j3.text.replace(u'注册时间','')
                    if u'最后访问' in i1j3.text:
                        if len(i1j3.text)>6:
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
                    cursor1.execute(sql_visitor)
                    connect1.commit()
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
                cursor1.execute(sqlperson)
                connect1.commit()
            except Exception as e:
                print e


        def friendinfoGet(urlfriendinfo,session1,connect1,cursor1,connect2,cursor2):
            urlfriendinfo1=urlfriendinfo+'&do=friend&view=me&from=space'
            try:
                responsefriendinfo=session1.request(method='GET',url=urlfriendinfo1)
                sqlproxy_success = 'UPDATE proxy.mala_proxy_live SET usednum = usednum+1 WHERE ip ="%s"' % (
                session1.proxies['http'].replace('http://', '').split(':')[0])
                cursor2.execute(sqlproxy_success)
                print sqlproxy_success
                connect2.commit()
            except Exception as e:
                print e
                # print session1.proxies
                proxyip= session1.proxies['http'].replace('http://','').split(':')[0]
                # print proxyip

                sqldelete='UPDATE proxy.mala_proxy_live SET errornum=errornum-1 WHERE ip ="%s"'%(proxyip)
                print sqldelete
                cursor2.execute(sqldelete)
                connect2.commit()

                # self.proxyDOC.update({'ip':proxyip},{'$inc':{'errornum':-1}})
                return
            # responsefriendinfo=session1.request(method='GET',url=urlfriendinfo1)
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
                    cursor1.execute(sqlperson_friend)
                    # self.cursor.close()
                    # self.cursor2 = self.connect2.cursor()
                    connect1.commit()
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


        def liuyanban(urlliuyanban,session1):#留言板处理
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

            session1 = requests.session()
            cookie1 = cookielib.LWPCookieJar()
            session1.cookies = cookie1
            session1.headers = session1.headers
            connect1 = MySQLdb.connect(host='127.0.0.1', user='root', passwd='asd123456', db='mala', charset='utf8')
            cursor1 = connect1.cursor()

            connect2=MySQLdb.connect(host='127.0.0.1', user='root', passwd='asd123456', db='proxy', charset='utf8')
            cursor2=connect2.cursor()

            sqlproxy_select='SELECT * FROM proxy.mala_proxy_live WHERE errornum > 0'
            cursor1.execute(sqlproxy_select)
            connect1.commit()
            proxydata=cursor1.fetchall()


            proxylist = []
            #
            # for i in self.proxyDOC.find({'errornum':{'$gt':0}}):
            #     dict1 = {'http': 'http://' + i['ip'] + ':' + i['port']}
            #     proxylist.append(dict1)
            # print proxylist
            for i in proxydata:
                dict1={
                    'http':'http://'+i[0]+':'+i[1]
                }
                proxylist.append(dict1)


            session1.proxies=proxylist[random.randint(0,len(proxylist)-1)]
            personalInfoget('http://home.mala.cn/home.php?mod=space&uid='+str(uid),session1=session1,connect1=connect1,cursor1=cursor1,connect2=connect2,cursor2=cursor2)
            # liuyanban('http://home.mala.cn/home.php?mod=space&uid=752731')
            friendinfoGet('http://home.mala.cn/home.php?mod=space&uid='+str(uid),session1=session1,connect1=connect1,cursor1=cursor1,connect2=connect2,cursor2=cursor2)



        ###############################################在这个方法内部用threading来启动多线程
        uid=40481
        threadlist=[]
        max_threads=30
        while uid < 7305075 or threadlist:
            for thread1 in threadlist:
                if not thread1.is_alive():
                    threadlist.remove(thread1)
            while len(threadlist) < max_threads and uid < 7305075:
                uid+=1
                # urlinTread='http://home.mala.cn/home.php?mod=space&uid='+str(uid)
                thread2=threading.Thread(target=run,args=(uid,))
                thread2.setDaemon(True)

                thread2.start()
                threadlist.append(thread2)
            time.sleep(5)


        ################################################多线程threading
    def numyield(self):
        i=4688
        while i < 7305075:
            yield i
            i+=1

if __name__ == '__main__':
    thisclass=personalInfoGet()
    thisclass.personalInfoGetByOrder()