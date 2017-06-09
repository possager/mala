#_*_coding:utf-8_*_
import requests
import cookielib
import MySQLdb
from  bs4 import BeautifulSoup



class mala_CD_index:
    def __init__(self):
        self.connect=MySQLdb.connect(host='127.0.0.1',user='root',passwd='asd123456',db='mala',charset='utf8')
        self.cursor=self.connect.cursor()
        self.headers={
            'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        }

    def index_get(self):
        session1=requests.session()
        session1.headers=self.headers
        cookie1=cookielib.LWPCookieJar()
        session1.cookies=cookie1
        print '11'
        def getindex(url1):
            response1=session1.request(method='GET',url=url1)
            # response1.encod
            datasoup=BeautifulSoup(response1.text,'lxml')
            for i in datasoup.select('#threadlisttableid > tbody'):
                try:
                    print '\n\n'
                    print i.select('tr > th > a.s.xst')[0].text#title
                    print i.select('tr > th > a.s.xst')[0].get('href')#href
                    # print i.select('tr > td.by > cite > a')[0].text#username
                    # print i.select('tr > td.by > cite > a')[0].get('href')#userhref
                    # print i.select('tr > td.by > em > span')[0].text
                    print i.select('tr > td.num > a')[0].text#replaynum
                    print i.select('tr > td.num > em')[0].text#viewnum
                    # print i.select('tr > td:nth-of-type(5) > cite > a')#lastviewername       #normalthread_14689291 > tr > td:nth-child(5) > cite
                    # print i.select('tr > td:nth-of-type(5) > cite > a')  # lastviewername
                    # print i.select('tr > td:nth-of-type(5) > em')

                    publisher_replayer_inf=i.select('tr > td.by')
                    publisherinf= publisher_replayer_inf[0].text.strip('\n').split('\n')#数组


                    replayerinf= publisher_replayer_inf[1].text.strip('\n').split('\n')#数组



                    hasPicture= i.select('tr > th > img[alt=attach_img]')
                    hasAttachment=i.select('tr > th > img[alt=attachment]')
                    isFreshPost=i.select('tr > th > img[src="static/image/stamp/011.small.gif"]')
                    hotValue=i.select(' tr > td.icn > a > img[src="static/image/common/hot_1.gif"]')
                    if hotValue:
                        print hotValue[0].get('title').replace(u'热度:','')#热度
                    else:
                        print 'None'
                    print '---------------------------------------'
                    print isFreshPost
                    print hasAttachment
                    print hasPicture





                except Exception as e:
                    print e

        getindex(url1='http://cd.mala.cn/')



if __name__ == '__main__':
    print 'hello'
    thisclass=mala_CD_index()
    thisclass.index_get()