#_*_coding:utf-8_*_
import requests
import cookielib
from bs4 import BeautifulSoup
import threading
import MySQLdb
import random
import time


class malaDetailGet:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        }
        self.threshold=10


    def detailget(self):
        # threadlock = threading.Lock()

        def get(url1,session1,cursor1,connect1,cursor2,connect2):
            print url1
            try:
                response=session1.request(method='GET',url=url1)
                response.encoding='gbk'
                pagenumstr=url1.split('thread-')[1].split('-')[1]
                threadnum=int(url1.split('thread-')[1].split('-')[0])
                if int(pagenumstr)==1:
                    sql_Update_dealed='UPDATE mala.index_CD set dealed=1 where href="%s"'%(url1)
                    cursor1.execute(sql_Update_dealed)
                    connect1.commit()
            except Exception as e:
                print e
                return
            datasoup=BeautifulSoup(response.text,'lxml')

            publisherhref = None
            publishername = None
            publishtime = None
            floor = None
            content = None

            for element in datasoup.select('#postlist > div'):
                try:
                    if element.select('div.pi > div > a'):
                        publishername = element.select('div.pi > div > a')[0].text#很奇怪一个网站的帖子某个元素会在两个地方出现
                        try:
                            publisherhref = element.select('div.pi > div > a')[0].get('href')
                        except Exception as e:
                            publisherhref = None
                    else:
                        publishername = element.select('div.pi > a > em')[0].text
                        publisherhref = None

                except Exception as e:
                    print e,'在查找发言人的名称和链接时出错'
                    publishername = '匿名'
                    publisherhref = 'None'

                print publishername
                print publisherhref
                try:
                    # print element.select('td.plc > div.pi > div.pti > div.authi > em')
                    publishtime = \
                        element.select('td.plc > div.pi > div > div.authi > em')[0].text.replace(u'发表于 ','').replace(
                        '\n', '').lstrip(' ').rstrip(' ')
                    print publishtime
                    try:
                        print element.select(' td.plc > div.pct > div > div > table > tr > td')[0].text
                        content = element.select(' td.plc > div.pct > div > div > table > tr > td ')[
                        0].text.replace('"', '-').replace('\n', ' ')
                        print content
                    except Exception as e:
                        content='抓取内容时出错,丫蛋的内容老是抓取失败,有毛病'
                    floor = element.select('td.plc > div.pi > strong > a > em')[0].text
                    print floor

                    sql2 = 'INSERT INTO mala.forumdetail (publishername,publisherhref,publishertime,content,floor,ownerthread) VALUE ("%s","%s","%s","%s","%s",%d)' % (
                    publishername, publisherhref, publishtime, content, floor,threadnum)
                    print sql2
                    cursor1.execute(sql2)
                    connect1.commit()
                except Exception as e:
                    print e

            nextpart = datasoup.select('#ct > div.pgs.mtm.mbm.cl > div > a.nxt')
            if nextpart:
                urlnext = nextpart[0].get('href')
                time.sleep(0.5)
                get(url1=urlnext,session1=session1,cursor1=cursor1,connect1=connect1,cursor2=cursor2,connect2=connect2)

            else:
                return




        def run(url1):
            # threadlock.acquire()
            cookie1=cookielib.LWPCookieJar()
            session1=requests.session()
            session1.cookies=cookie1
            session1.headers=session1.headers

            connect1=MySQLdb.connect(host='127.0.0.1',user='root',db='mala',passwd='asd123456',charset='utf8')
            connect2=MySQLdb.connect(host='127.0.0.1',user='root',db='proxy',passwd='asd123456',charset='utf8')
            cursor1=connect1.cursor()
            cursor2=connect2.cursor()

            sqlproxy_select = 'SELECT * FROM proxy.mala_proxy_live WHERE errornum > 0'
            cursor1.execute(sqlproxy_select)
            connect1.commit()
            proxydata = cursor1.fetchall()

            proxylist = []
            for i in proxydata:
                dict1 = {
                    'http': 'http://' + i[0] + ':' + i[1]
                }
                proxylist.append(dict1)

            session1.proxies = proxylist[random.randint(0, len(proxylist) - 1)]


            get(url1=url1,session1=session1,cursor1=cursor1,connect1=connect1,cursor2=cursor2,connect2=connect2)
            # threadlock.release()

        def begain():
            threadlistInBegain=[]
            urllist=urlGet()

            while threadlistInBegain or urllist:
                for thread1 in threadlistInBegain:
                    if not thread1.is_alive():
                        threadlistInBegain.remove(thread1)
                        print 'debug1'
                    print 'debug2'
                while len(threadlistInBegain) < self.threshold and urllist:
                    url_ToBe_use=urllist.pop()
                    thread2=threading.Thread(target=run,args=(url_ToBe_use,))
                    thread2.setDaemon(True)
                    thread2.start()
                    threadlistInBegain.append(thread2)
                time.sleep(5)

        def urlGet():
            sqlindex = 'SELECT href FROM mala.index_CD WHERE dealed=0'
            connect_Url = MySQLdb.connect(host='127.0.0.1', user='root', db='mala', passwd='asd123456', charset='utf8')
            cursor_Url = connect_Url.cursor()
            cursor_Url.execute(sqlindex)
            dataurl = cursor_Url.fetchall()
            urllist=[]
            for i in dataurl:
                urllist.append(i[0])
            return urllist

        begain()




if __name__ == '__main__':
    thisclass=malaDetailGet()
    thisclass.detailget()