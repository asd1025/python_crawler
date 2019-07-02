import ssl
import sys
from urllib.request import Request, urlopen
from datetime import datetime

from bs4 import BeautifulSoup


def crawling(url='',
             encoding='utf-8',
             proc1=lambda data :data,
             proc2=lambda data :data,
             err = lambda e : print(f'{e}: {datetime.now()}',file=sys.stderr) ) :

     try :

        request = Request(url)
        ssl._create_default_https_context = ssl._create_unverified_context()
        context = ssl._create_unverified_context()
        response = urlopen(request ,context=context)
        receive = response.read()
        return proc2(proc1((receive.decode(encoding,errors='replace'))))


     except Exception as e :
        err(e)

