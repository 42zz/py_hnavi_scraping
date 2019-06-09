# coding: UTF-8
import urllib2
import csv
from bs4 import BeautifulSoup


# 検索リストからURLを抽出する

# アクセスするURL
CSV = "url.csv"
BASE = "https://h-navi.jp"
PAGE = "/support_facility/aichi"
URL = BASE + PAGE

# init csv file
with open(CSV, 'w') as csvFile:
  writer = csv.writer(csvFile)
  writer.writerow(["URL", "タイトル", "カテゴリ"])
csvFile.close()


###################
# データをCSVに格納 #
def fetchUrl(pageNum):
  url = URL + "?page=" + pageNum

  # Fetch HTML
  instance = urllib2.urlopen(url)
  soup = BeautifulSoup(instance, "html.parser")
  div = soup.findAll("div", { "class":"facility-card__top-area"})

  for el in div:
    a = el.a
    el_txt = a.select('.facility-card__text')[0].string.strip()
    el_ttl = a.select('.facility-card__name')[0].string.strip()
    print el_ttl

    data1 = BASE + a.get('href').encode('utf_8')
    data2 = el_ttl.encode('utf_8')
    data3 = el_txt.encode('utf_8')

  # csv 書き込み
    with open(CSV, 'a') as csvFile:
      writer = csv.writer(csvFile)
      writer.writerow([data1, data2, data3])
    csvFile.close()

#################
# ページ数を取得
# return int
def getNumPages():
  instance = urllib2.urlopen(URL)
  soup = BeautifulSoup(instance, "html.parser")
  element = soup.select(".pagination > .page:last-child")
  return int(element[0].a.get_text())

#################
# fetchUrlをページ数分まわす
#
def fetchPages(pageNum):
  n = 1
  while n < pageNum:
    fetchUrl(str(pageNum))
    n += 1
  return pageNum

n = 1
num = getNumPages()
while n < num + 1:
  fetchUrl(str(n))
  n += 1