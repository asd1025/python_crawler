import os
from datetime import datetime, time
import ssl
import sys
from itertools import count
from urllib.request import Request, urlopen
# import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
import time

from collection import crawler


def crawling_pelicana():
    results = []
    for page in count(start=1) :
        url = 'https://pelicana.co.kr/store/stroe_search.html?branch_name=&gu=&si=&page=%d' % page
        html=crawler.crawling(url)

        bs = BeautifulSoup(html, 'html.parser')

        tag_table=bs.find('table',attrs={'class':'table'})
        tag_body=tag_table.find('tbody')
        tags_tr=tag_body.findAll('tr')

        # 끝 검출
        if len(tags_tr) == 0:
            break

        for tag_tr in tags_tr :
            strings=list(tag_tr.strings)
            name=strings[1]
            address=strings[3]
            sidogu=address.split()[:2]
            results.append( (name,address)+tuple(sidogu) )

    # store
    # table= pd.DataFrame(results,columns=['name','address','sido','gungu'])
    # table.to_csv('__result__/pelicana.csv', encoding='UTF-8', mode='w', index=True)






# def crawling_pelicana():
#     results = []
#
#     for page in range (1,5) :
#         url =   'https://pelicana.co.kr/store/stroe_search.html?branch_name=&gu=&si=&page=%d' % page
#         try :
#
#             request = Request(url)
#             # ssl._create_default_https_context = ssl._create_unverified_context()
#             context = ssl._create_unverified_context()
#             response = urlopen(request ,context=context)
#             receive = response.read()
#             html=receive.decode('utf-8',errors='replace')
#             print(f'{datetime.now()}:success for request [{url}]')
#
#
#         except Exception as e :
#             print(f'{e}: {datetime.now()}',file=sys.stderr)
#             # continue
#         bs=BeautifulSoup(html,'html.parser')
#         tag_table=bs.find('table',attrs={'class':'table'})
#         tag_body=tag_table.find('tbody')
#         tags_tr=tag_body.findAll('tr')
#
#         #끝 검출
#         if len(tags_tr) == 0:
#             break
#
#         for tag_tr in tags_tr :
#             strings=list(tag_tr.strings)
#             name=strings[1]
#             address=strings[3]
#             sidogu=address.split()[:2]
#             results.append( (name,address)+tuple(sidogu) )
#
#     # store
#     table= pd.DataFrame(results,columns=['name','address','sido','gungu'])
#     table.to_csv('__result__/pelicana.csv', encoding='UTF-8', mode='w', index=True)
#
#     for t in results:
#         print(t)


def crawling_nene():
    results = []
    for page in range(1,50):
        try :

            url = 'https://nenechicken.com/17_new/sub_shop01.asp?ex_select=1&ex_select2=&IndexSword=&GUBUN=A&page=%d' % page
            request = Request(url)
            response = urlopen(request )
            receive=response.read()
            html = receive.decode('utf-8', errors='replace')
            print(f'{datetime.now()}:success for request [{url}]')

        except Exception as e:
            print(f'{e}: {datetime.now()}', file=sys.stderr)
            # continue
        bs = BeautifulSoup(html, 'html.parser')
        tag_table=bs.find('div',attrs={'class':'shopWrap'})
        shopInfo=tag_table.findAll('div',attrs={'class':'shopInfo'})
        shopNames=tag_table.findAll('div',attrs={'class':'shopName'})
        shopAddrs=tag_table.findAll('div',attrs={'class':'shopAdd'})
        # print(shopInfo )
        # 끝 검출
        if len(shopInfo) == None:
            break
        for index,shop  in enumerate(shopInfo)  :
            sidogu=shopAddrs[index].text.split()[:2]
            info=(shopNames[index].text,shopAddrs[index].text)
            results.append(info+tuple(sidogu))

    # store
    # table = pd.DataFrame(results, columns=['name', 'address', 'sido', 'gungu'])
    # BASE_DIR=os.path.dirname(os.path.abspath(__file__))
    # RESULT_DIR=f'{BASE_DIR}/__results__'
    # print(BASE_DIR)
    # table.to_csv('/root/crawling-results/nene.csv', encoding='UTF-8', mode='w', index=True)
    # for t in results:
    #     print(t)

    print('===================')

def crawling_goobne():
    results=[]
    url= 'http://www.goobne.co.kr/store/search_store.jsp'

    # 첫 페이지 로딩
    wd = webdriver.Chrome('D:\cafe24\chromedriver_win32\chromedriver.exe')
    wd.get(url)
    time.sleep(5)

    for page in count(start=1) :
        # 자바스크립트 실행
        script= 'store.getList(%d)' % page
        wd.execute_script(script)
        print(f'{datetime.now()}:success for request [{url}]')
        time.sleep(3)

        # 실행 결과 rendering 된 HTML 가져오기
        html=wd.page_source

        # parsing with bs4
        bs=BeautifulSoup(html,'html.parser')
        tag_tbody = bs.find('tbody',attrs={"id":"store_list"})
        tags_tr = tag_tbody.findAll('tr')

        # detect last page
        if tags_tr[0].get('class') is None:
            break

        for tag_tr in tags_tr :
            strings = list(tag_tr.strings)
            name = strings[1]
            address=strings[6]
            sidogu = address.split()[:2]
            results.append( (name,address)+tuple(sidogu) )
    wd.quit()
    for t in results:
        print(t)


    # store
    #     table = pd.DataFrame(results, columns=['name', 'address', 'sido', 'gungu'])
        # table.to_csv('__result__/goobne.csv', encoding='UTF-8', mode='w', index=True)

if __name__ == '__main__':
    #pelicana
    # crawling_pelicana()
    crawling_nene()
    # crawling_goobne()