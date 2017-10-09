# _*_ encoding:utf-8 _*_
__author__ = 'lifan'
__date__ = '2017/9/21 下午9:15'

import urllib.request
import bs4

url = 'https://www.cs.ucd.ie/AcademicProfile/NeilHurley/'
urlOpened = urllib.request.urlopen(url)
rawHtml = urlOpened.read()
soup = bs4.BeautifulSoup(rawHtml)
print(soup.title)
body_words = soup.body.get_text(strip=True)
print(body_words)
