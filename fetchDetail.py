# coding: UTF-8
import urllib2
import csv
import re
from bs4 import BeautifulSoup

URL_CSV = "url.csv"
CSV_FILE = "data.csv"

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
    table = soup.findAll("table", {"class":"facility-table"})
    phone = soup.select(".facility-card__telephone-number")
    address = soup.select(".facility-head-menu__address")

    if(table or address or phone):
        if(table):
            rows = table[1].findAll("tr")
            with open(CSV_FILE, "a") as file:
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
        else:
            with open(CSV_FILE, "a") as file:
                writer = csv.writer(file)
                headRow = []
                print "OK2: " + title
                address = replace_str(address[0].get_text()).encode("utf_8") if address else ""
                phone = replace_str(phone[0].get_text()).encode("utf_8") if phone else ""
                newRow = [title, cat, address, phone, '']
                # print newRow
                writer.writerow(newRow)
    else:
        print "NG: " + title




with open(URL_CSV, 'r') as f:
    reader = csv.reader(f)
    header = next(reader)  # ヘッダーを読み飛ばしたい時

    for row in reader:
        # list = row.decode("string-escape")
        fetchDetail(row[0], row[1], row[2])
        

# fetchDetail(url, title, cat)

