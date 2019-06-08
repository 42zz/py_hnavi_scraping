# coding: UTF-8
import urllib2
import csv
import re
from bs4 import BeautifulSoup

CSV_FILE = "detail.csv"

# 文字変換
def replace_str(s):
    s = s.replace('\r\n', '')
    s = s.replace('\n', '')
    s = s.replace(' ', '')
    s = s.replace(u'\xa0', '')
    return s


# URLにアクセスしてCSVに格納する
def fetchDetail(url, title, cat):
    # URLにアクセスする 戻り値にはアクセスした結果やHTMLなどが入ったinstanceが帰ってきます
    instance = urllib2.urlopen(url)

    # instanceからHTMLを取り出して、BeautifulSoupで扱えるようにパースします
    soup = BeautifulSoup(instance, "html.parser")

    # テーブルを指定
    table = soup.findAll("table", {"class":"facility-table"})[1]
    rows = table.findAll("tr")

    with open(CSV_FILE, "a", encoding="utf_8_sig") as file:
        writer = csv.writer(file)
        headRow = []
        newRow = [title, cat, '', '', '']
        # csvRow = []
        for row in rows:
            th = replace_str(row.find("th").get_text())
            td = replace_str(row.find("td").get_text())

            if u'住所' in th:
                print title
                newRow[2] = td.encode("utf_8")
            elif u'電話番号' in th:
                newRow[3] = td.encode("utf_8")
            elif 'URL' in th:
                newRow[4] = td.encode("utf_8")

        # print newRow
        writer.writerow(newRow)

with open('data.csv', 'r') as f:
    reader = csv.reader(f)
    header = next(reader)  # ヘッダーを読み飛ばしたい時

    for row in reader:
        # list = row.decode("string-escape")
        fetchDetail(row[0], row[1], row[2])
        

# fetchDetail(url, title, cat)

