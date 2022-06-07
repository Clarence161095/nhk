import codecs
import json
import os
import re
import sys
from datetime import date

import requests
from bs4 import BeautifulSoup


def main():
    try:
        r = requests.get('http://www3.nhk.or.jp/news/easy/news-list.json')
        r.encoding = 'utf-8-sig'
        o = json.loads(r.text)
        parse(o)
    except:
        print("Error main")


def parse(o):
    try:
        contents = []
        i = 0
        for k, v in o[0].items():
            contents.append(parseDate(k, v))
            if (i > 30):
                break
            i = i + 1

        with open('nhk-easy.html', "w") as f:
            print('<?xml version="1.0" encoding="UTF-8" ?>', file=f)
            print("<!DOCTYPE html>", file=f)
            print("<html lang='ja'>", file=f)
            print(
                '<head><meta http-equiv="content-type" content="application/xhtml+xml; charset=UTF-8" >', file=f)
            print('<style type="text/css">body {  margin-left: 1em;  margin-right: 1em;  font-family: serif;  line-break: normal;  -epub-line-break: normal;  -webkit-line-break: normal;}p {  text-indent: 1em;}h1 {  font-size: 1.2rem;  font-weight: bold;}rt {  font-size: 0.15rem;  font-weight: normal;  color: rgba(0, 0, 0, 0.3);}img {  display: none;}</style>', file=f)
            print("</head>", file=f)
            print("<body>", file=f)
            for content in contents:
                print("<br />".join(content), file=f)
            print("</body>", file=f)
            print("</html>", file=f)
            print("File nhk-easy.html created")

            file = open('nhk-easy.opf', "w")
            file.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?><package version=\"3.0\" xmlns=\"http://www.idpf.org/2007/opf\"         unique-identifier=\"BookId\"> <metadata xmlns:dc=\"http://purl.org/dc/elements/1.1/\"           xmlns:dcterms=\"http://purl.org/dc/terms/\">   <dc:title>NHK Easy - tuan200</dc:title>    <dc:contributor>NHK</dc:contributor>   <dc:language>ja</dc:language>   <dc:publisher>NHK</dc:publisher> </metadata> <manifest>  <item id=\"titlepage\" href=\"nhk-easy.html\" media-type=\"application/xhtml+xml\" /> </manifest> <spine toc=\"tocncx\" page-progression-direction=\"rtl\">  <itemref idref=\"titlepage\" /> </spine></package>")
            file.close()

        with open('nhk-easy-vertical.html', "w") as f:
            print('<?xml version="1.0" encoding="UTF-8" ?>', file=f)
            print("<!DOCTYPE html>", file=f)
            print("<html lang='ja'>", file=f)
            print(
                '<head><meta http-equiv="content-type" content="application/xhtml+xml; charset=UTF-8" >', file=f)
            print('<style type="text/css">body {  margin-left: 1em;  margin-right: 1em;  font-family: serif;  writing-mode: tb-rl;  -epub-writing-mode: vertical-rl;  -webkit-writing-mode: vertical-rl;  line-break: normal;  -epub-line-break: normal;  -webkit-line-break: normal;}p {  text-indent: 1em;}h1 {  font-size: 1.2rem;  font-weight: bold;}rt {  font-size: 0.15rem;  font-weight: normal;  color: rgba(0, 0, 0, 0.3);}img {  display: none;}</style>', file=f)
            print("</head>", file=f)
            print("<body>", file=f)
            for content in contents:
                print("<br />".join(content), file=f)
            print("</body>", file=f)
            print("</html>", file=f)
            print("File nhk-easy-vertical.html created")

            file1 = open('nhk-easy-vertical.opf', "w")
            file1.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?><package version=\"3.0\" xmlns=\"http://www.idpf.org/2007/opf\"         unique-identifier=\"BookId\"> <metadata xmlns:dc=\"http://purl.org/dc/elements/1.1/\"           xmlns:dcterms=\"http://purl.org/dc/terms/\">   <dc:title>NHK Easy Vertical- tuan200</dc:title>    <dc:contributor>NHK</dc:contributor>   <dc:language>ja</dc:language>   <dc:publisher>NHK</dc:publisher> </metadata> <manifest>  <item id=\"titlepage\" href=\"nhk-easy-vertical.html\" media-type=\"application/xhtml+xml\" /> </manifest> <spine toc=\"tocncx\" page-progression-direction=\"rtl\">  <itemref idref=\"titlepage\" /> </spine></package>")
            file1.close()

        print("Done.")
    except:
        print("Error parsing")


def parseDate(date, news):
    try:
        items = []
        content = []
        for i in news:
            item = parseNews(i)
            items.append(item)
            content.append(item["content"])
        return content
    except:
        print("Error parsing")


def parseNews(news):
    try:
        news_id = news['news_id']
        news_time = news['news_prearranged_time'].replace(':', '-')
        title = news['title']
        print(title)
        title_ruby = news['title_with_ruby']
        news_uri = 'http://www3.nhk.or.jp/news/easy/' + \
            str(news_id) + '/' + str(news_id) + '.html'

        r = requests.get(news_uri)
        r.encoding = 'utf-8'

        soup = BeautifulSoup(r.text, 'html.parser')
        date = soup.find(
            'p', attrs={'class': 'article-main__date'}).contents[0]
        title = soup.find(
            'h1', attrs={'class': 'article-main__title'})  # .find('h2')
        article = soup.find('div', attrs={'class': 'article-main__body'})

        for a in article.findAll('a'):
            a.unwrap()

        return {
            "content": str(title) + str(article),
        }
    except:
        print("Error parsing")


main()
