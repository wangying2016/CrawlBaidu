from urllib.request import urlopen
from urllib.request import Request
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import re
import pprint


print('Please input keyword:')
keyword = input()
print('Please input results limit:')
limit = input()

info = []
page = 0

while True:
    # 1. Pretend Browser, Open first page.
    try:
        url = 'https://www.baidu.com/s?wd=' + keyword + '&pn=' + str(page)
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) '
                                 'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'}
        req = Request(url=url, headers=headers)
        html = urlopen(req)
    except HTTPError:
        print('Open ' + 'https://www.baidu.com/s?wd=' + keyword + ' failed')
        break

    # 2. Record data in one page.
    bsObj = BeautifulSoup(html)
    for result in bsObj.find('div', {'id': 'content_left'})\
                       .findAll('div', class_=re.compile('^result(.)*c-container(.)*')):
        try:
            newResult = {}
            newResult['title'] = result.find('h3', class_=re.compile('t(.)*')).get_text().strip().replace('|', '\|')
            newResult['brief'] = result.find('div', {'class': 'c-abstract'}).get_text().strip().replace('|', '\|')
            newResult['url'] = result.find('h3').find('a').attrs['href']
            if len(info) < int(limit):
                info.append(newResult)
            else:
                break
        except AttributeError:
            print('This reuslt missing something! No worries though!')
            continue

    # 3. Move to new page.
    if len(info) >= int(limit):
        break
    nextPage = bsObj.find('a', text='下一页>')
    if nextPage is None:
        print('No more results!')
        break
    else:
        page += 10

with open('record.md', 'w', encoding='utf-8') as md:
    md.write('| 标题 |' + ' 简介 |' + ' 链接 |\n')
    md.write('| --- |' + ' --- |' + ' --- |\n')
    for result in info:
        md.write(('| ' + str(result['title']) + ' | ' +
                  str(result['brief']) + ' |' +
                  str(result['url']) + ' |\n'))

pprint.pprint(info)

