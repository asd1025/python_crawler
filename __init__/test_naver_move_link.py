from itertools import count
from urllib import response
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup

from collection import crawler


def ex01():
    request = Request('https://movie.naver.com/movie/sdb/rank/rmovie.nhn')
    # response = urlopen(request)
    html = response.read().decode('cp949')
    # print(html)

    bs = BeautifulSoup(html, 'html.parser')
    # 이쁘게 출력해줌
    # print(bs.prettify())

    divs = bs.findAll('div', attrs={'class': 'tit3'})
    # print(divs)
    for index, div in enumerate(divs):
        print(index + 1, div.a.text, div.a['href'], sep=" : ")
    print('======================================')


def proc_naver_movie_rank(html):
    # processing
    bs = BeautifulSoup(html, 'html.parser')
    results = bs.findAll('div', attrs={'class': 'tit3'})
    return results


def store_naver_movie_rank(data):
    for index, div in enumerate(data):
        print(index + 1, div.a.text, div.a['href'], sep=" : ")
    return data


def ex02():
    # fetch
    crawler.crawling(url='https://movie.naver.com/movie/sdb/rank/rmovie.nhn',
                     encoding='cp949',
                     proc1=proc_naver_movie_rank,
                     proc2=lambda data: list(map(lambda div: print(div[0],div[1].a.text,div[1].a['href'],sep=' : ' ), enumerate(data)))
)

def crawling_kyochon():
    results=[]
    for sido1 in range(1,18):
        for sido2 in count(start=1):
            url = 'http://www.kyochon.com/shop/domestic.asp?sido1={0}&sido2={1}&txtsearch='.format(sido1, sido2)
            html = crawler.crawling(url)

            # 끝 검출
            if html is None:
                break
            bs = BeautifulSoup(html,'html.parser')
            tag_ul = bs.find('ul',attrs={'class':'list'})
            tags_span = tag_ul.findAll('span',attrs={'class':'store_item'})

            for tag_span in tags_span :
                strings =  list (tag_span.strings)
                name=strings[1]
                address=strings[3].replace('\r\n\t','').strip()
                sidogu=address.split()[:2]
                results.append((name,address)+tuple(sidogu))

    for t in results:
        print(t)
crawling_kyochon()

# __name__ == '__main__' and not \
#     ex01() and not \
#     ex02()



