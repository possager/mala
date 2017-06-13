#_*_coding:utf-8_*_
import requests
import cookielib
import MySQLdb
from bs4 import BeautifulSoup
import time
import random


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

        duplicate_key_num=1
        threshold=100

        def getindex(url1):
            response1=session1.request(method='GET',url=url1)
            # response1.encod
            datasoup=BeautifulSoup(response1.text,'lxml')
            for i in datasoup.select('#threadlisttableid > tbody'):
                try:
                    print '\n\n'
                    title= i.select('tr > th > a.s.xst')[0].text.replace('"',"-").replace("'",'|')#title
                    href= i.select('tr > th > a.s.xst')[0].get('href')#href
                    replayernum= i.select('tr > td.num > a')[0].text#replaynum
                    viewernum= i.select('tr > td.num > em')[0].text#viewnum
                    publisher_replayer_inf=i.select('tr > td.by')
                    publisherhref=i.select('tr > td.by > cite > a')[0].get('href')
                    publisherinf= publisher_replayer_inf[0].text.strip('\n').split('\n')#数组

                    publishername=publisherinf[0]
                    publishtime=publisherinf[1]
                    replayerinf= publisher_replayer_inf[1].text.strip('\n').split('\n')#数组
                    replayername=replayerinf[0]#回复人员的名称
                    replayertime=replayerinf[1]#回复的时间

                    print replayername,'----name'
                    print replayertime

                    hasAttachmentnum=0
                    hasPicturenum=0
                    beenAgreednum=0
                    isFreshPostnum=0


                    hasPicture= i.select('tr > th > img[alt=attach_img]')
                    hasAttachment=i.select('tr > th > img[alt=attachment]')
                    isFreshPost=i.select('tr > th > img[src="static/image/stamp/011.small.gif"]')
                    beenAgreed=i.select('tr > th > img[alt=agree]')
                    hotValue=i.select(' tr > td.icn > a > img[src="static/image/common/hot_1.gif"]')

                    if hasPicture:
                        hasPicturenum=1
                    if hasAttachment:
                        hasAttachmentnum=1
                    if isFreshPost:
                        isFreshPostnum=1
                    if beenAgreed:
                        beenAgreednum=1

                    hotValuenum=0
                    if hotValue:
                        hotValuenum= hotValue[0].get('title').replace(u'热度:','')#热度
                    else:
                        hotValuenum=0
                    print '---------------------------------------'
                    sql_insert_cd='INSERT INTO index_CD (href,title,publishername,publishtime,publisherhref,viewernum,replayernum,lastreplayername,lastreplaytime,isFreshPost,hasAttachment,beenAgreed,hasPicture,hotValue)' \
                                  'VALUE ("%s","%s","%s","%s","%s","%d","%d","%s","%s","%d","%d","%d","%d","%d")'%(href,title,publishername,publishtime,publisherhref,int(viewernum),int(replayernum),
                                                                                                                   replayername,replayertime,isFreshPostnum,hasAttachmentnum,beenAgreednum,hasPicturenum,int(hotValuenum))

                    try:
                        print sql_insert_cd
                        self.cursor.execute(sql_insert_cd)
                        self.connect.commit()
                    except Exception as e:
                        duplicate_key_num=duplicate_key_num+1
                        print e


                except Exception as e:
                    print e

            if duplicate_key_num > threshold:
                print '重复过多,策略性停止'
                return

            print response1.url
            thispagenum=response1.url.split('-')[-1].split('.')[0]
            thispagenum1=int(thispagenum)
            if thispagenum1<500:
                urlsplit=response1.url.split('-')
                urlnext=urlsplit[0]+'-'+urlsplit[1]+'-'+str(thispagenum1+1)+'.html'
                print urlnext
                time.sleep(random.randint(2,5))
                getindex(urlnext)
        getindex(url1='http://cd.mala.cn/forum-70-3.html')



if __name__ == '__main__':
    print 'hello'
    thisclass=mala_CD_index()
    thisclass.index_get()