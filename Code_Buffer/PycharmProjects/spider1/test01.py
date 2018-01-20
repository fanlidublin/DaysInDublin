# _*_ encoding:utf-8 _*_
__author__ = 'lifan'
__date__ = '2017/4/13 下午10:37'

from bs4 import BeautifulSoup
import re

html_doc = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class="story">...</p>
"""

soup = BeautifulSoup(html_doc,'html.parser',from_encoding='utf-8')

# test1
print 'All:'
links = soup.find_all('a')
for link in links:
    print link.name, link['href'],link.get_text()

# test2
print 'special:'
link_special = soup.find('a',href='http://example.com/tillie')
print link_special.name, link_special['href'],link_special.get_text()

# test3
print 'regular:'
link_special2 = soup.find('a',href=re.compile(r"ill"))
print link_special2.name, link_special2['href'],link_special2.get_text()

# test4
print 'paragraph:'
p_special3 = soup.find('p',class_='title')
print p_special3.name,p_special3.get_text()
