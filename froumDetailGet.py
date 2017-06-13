#_*_coding:utf-8_*_
import sys

reload(sys)

sys.setdefaultencoding('utf-8')

import urllib2
import cookielib
import MySQLdb
import html5lib
import time
from bs4 import BeautifulSoup
import pymongo





class mala:
    def __init__(self):
        self.connect=MySQLdb.connect(host='127.0.0.1',user='root',passwd='asd123456',db='mala',charset='utf8')
        self.cursor=self.connect.cursor()
        self.client=pymongo.MongoClient('localhost',27017)
        self.DOC=self.client['mala_14669372']
        self.COL=self.DOC['detail']

    def malaread(self):
        cookieq=cookielib.LWPCookieJar()
        cookiehandler=urllib2.HTTPCookieProcessor(cookieq)
        openner=urllib2.build_opener(cookiehandler)
        headers1={
            'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        }

        def getdetail(url11=None):
            request1=urllib2.Request(url=url11,headers=headers1)
            response=openner.open(request1)
            datasoup=BeautifulSoup(response.read(),'html5lib')

            publisherhref=None
            publishername=None
            publishtime=None
            floor=None
            content=None

            for i in datasoup.select('#postlist > div'):
                try:
                    if i.select('div.pi > div > a'):
                        publishername= i.select('div.pi > div > a')[0].text
                        try:
                            publisherhref= i.select('div.pi > div > a')[0].get('href')
                        except Exception as e:
                            publisherhref=None
                    else:
                        publishername = i.select('div.pi > a > em')[0].text
                        publisherhref = None


                except Exception as e:
                    print e
                    publishername= '匿名'
                    publisherhref= 'None'

                print publishername
                print publisherhref
                try:
                    publishtime= i.select('tbody > tr > td.plc > div.pi > div > div.authi > em')[0].text.split(u'发表于 ')[1].replace('\n','').lstrip(' ').rstrip(' ')#pid68569410 > tbody > tr:nth-child(1) > td.plc > div.pi > div > div.authi
                    print publishtime

                    content= i.select('tbody > tr > td.plc > div.pct > div > div.t_fsz > table > tbody > tr')[0].text.decode('utf-8').encode('utf-8').replace('"','-')
                    print content
                    floor=i.select('tbody > tr > td.plc > div.pi > strong > a > em')[0].text
                    print floor

                    sql2='INSERT INTO mala.post_14669372 (publishername,publisherhref,publishertime,content,floor) VALUE ("%s","%s","%s","%s","%s")' %(publishername,publisherhref,publishtime,content,floor)
                    print sql2
                    self.cursor.execute(sql2)
                    self.connect.commit()

                except Exception as e:
                    print e

            nextpart=datasoup.select('#ct > div.pgs.mtm.mbm.cl > div > a.nxt')
            if nextpart:
                urlnext= nextpart[0].get('href')
                time.sleep(0.5)
                getdetail(urlnext)

            else:
                return

        getdetail(url11='http://www.mala.cn/thread-14686090-1-1.html')


if __name__ == '__main__':
    thisclass=mala()
    thisclass.malaread()