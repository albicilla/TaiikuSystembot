# -*- encoding: utf-8 -*-
import json
import random
import requests

from django.shortcuts import render
from django.http import HttpResponse

# localで実行するときは以下三行のコメントアウトをはずす
import sys
path="/Users/albicilla/programming/osoBOT/osomatsu_bot/bot/"
sys.path.append(path)
reload(sys)
sys.setdefaultencoding('utf8')

from load_serif import osomatsu_serif  # 先ほどのおそ松のセリフ一覧をimport
import re #正規表現


##スクレイピング用
import urllib
from bs4 import BeautifulSoup
#import cookielib
import future
import os
import re
import mechanize
import ConfigParser
import sys
import re
import requests

REPLY_ENDPOINT = 'https://api.line.me/v2/bot/message/reply'
ACCESS_TOKEN = '94cHxQ5/qOuUS2WbyCDvI+JTb97CKGV24IC6nB3PRrvK85u4INKsY1MCZ6PC3VwzeLHswQgdZQYeNlFPUp4R6PJU+uJXYyrqt71l+L/Gd8aZQ1HZ6Jkrt7px6qzxpW9+xT6+RF2TJtKPDSdTGf4y7QdB04t89/1O/w1cDnyilFU='
HEADER = {
    "Content-Type": "application/json",
    "Authorization": "Bearer " + ACCESS_TOKEN
}

def index(request):
    return HttpResponse("This is bot api.")


def reply_text(reply_token, text):



    # show 予約情報の表示


    # 予約　正規表現
    regi = re.compile("regi*.")

    reply = ""
    if text == "show":
        #config.txtを読み込む
        config = ConfigParser.SafeConfigParser()
        conf = os.path.join(os.path.dirname(__file__),'config.txt')
        config.read([os.path.expanduser(conf)])
        #scraping
        browser = mechanize.Browser()
        #robot.txtを無効化しておくとちゃんと開ける
        browser.set_handle_robots(False)
        #URLを指定して読み込み　体育システムのURL


        #取得したhtmlを出力
            #print html.read()
        TOP_URL = 'https://wellness.sfc.keio.ac.jp/v3/'
        browser.open('https://wellness.sfc.keio.ac.jp/v3/')

        #0番目のフォームを選択
        browser.select_form(nr=0)
        #洗濯したフォームに値を設定
        browser.form['login'] = config.get('config','name')
        browser.form['password'] = config.get('config','password')
        #submitする
        res = browser.submit()
        res_html = res.read()
        soup = BeautifulSoup(res_html, "html.parser")
        #lineに通知
        line_message =''
        tables = soup.find_all('tr')
        idx = 0
        for sk in tables:
            p = sk.findAll('td')
            for pk in p:
                if re.match(u'[シ]',pk.text) or re.match(u'[予約]',pk.text) :
                    print ("　lkjlk")
                elif re.match('\(',pk.text):
                    line_message+="\n"
                elif re.match('^[0-9]{1,}$',pk.text):
                    line_message += u" 空き数"
                    line_message += pk.text
                    line_message += " ID="
                    line_message += str([idx])
                    idx += 1
                else:
                    line_message+="\n"
                    line_message += pk.text
                    print ("%s" % pk.text)

        reply = line_message;
    elif re.match(regi,text):
        print (u"予約処理")
        #config.txtを読み込む
        config = ConfigParser.SafeConfigParser()
        conf = os.path.join(os.path.dirname(__file__),'config.txt')
        config.read([os.path.expanduser(conf)])
        #scraping
        browser = mechanize.Browser()
        #robot.txtを無効化しておくとちゃんと開ける
        browser.set_handle_robots(False)
        #URLを指定して読み込み　体育システムのURL


        #取得したhtmlを出力
            #print html.read()
        TOP_URL = 'https://wellness.sfc.keio.ac.jp/v3/'
        browser.open('https://wellness.sfc.keio.ac.jp/v3/')

        #0番目のフォームを選択
        browser.select_form(nr=0)
        #洗濯したフォームに値を設定
        browser.form['login'] = config.get('config','name')
        browser.form['password'] = config.get('config','password')
        #submitする
        res = browser.submit()
        res_html = res.read()
        soup = BeautifulSoup(res_html, "html.parser")
        #lineに通知
        line_message =''
        tables = soup.find_all('tr')

        #パースして上からいくつ目のものを知りたいかをパラメタに与える
        print (text)
        #正規表現
        pattern=r'([+-]?[0-9]+\.?[0-9]*)'
        ynum = re.findall(pattern,text)
        print (ynum[0])
        yidx = 0
        yoyaku_url=""
        for sk in tables:
            a = sk.findAll('a')
            for ak in a:
                if(ak.text == u"予約"):
                    if yidx == int(ynum[0]):
                        print("%s's url is %s" % (ak.text, ak.attrs['href']))
                        yoyaku_url = ak.attrs['href']
                    yidx += 1
        res = browser.open(yoyaku_url.decode("utf-8"))
        browser.select_form(nr=1)
        res = browser.submit()
        res_html = res.read()
        soup = BeautifulSoup(res_html, "html.parser")
        #print (soup)
        res_error = soup.findAll("p", attrs={"class": "error"})[0].text
        res_error = res_error.strip()

        if res_error == u"同じ週に予約し出席(欠席)できるのは2コマまでです．":
            print(res_error)
            return False
        elif res_error == u"すでに予約済みです．":
            print(res_error)
            return False
        else:
            browser.select_form(nr=1)
            browser.submit()# 予約確定
            print("予約しました")

        reply = "予約しました"
    elif text == "attend":
        print (u"確認処理")
        #config.txtを読み込む
        config = ConfigParser.SafeConfigParser()
        conf = os.path.join(os.path.dirname(__file__),'config.txt')
        config.read([os.path.expanduser(conf)])
        #scraping
        browser = mechanize.Browser()
        #robot.txtを無効化しておくとちゃんと開ける
        browser.set_handle_robots(False)
        #URLを指定して読み込み　体育システムのURL


        #取得したhtmlを出力
            #print html.read()
        TOP_URL = 'https://wellness.sfc.keio.ac.jp/v3/'
        browser.open('https://wellness.sfc.keio.ac.jp/v3/')

        #0番目のフォームを選択
        browser.select_form(nr=0)
        #洗濯したフォームに値を設定
        browser.form['login'] = config.get('config','name')
        browser.form['password'] = config.get('config','password')
        #submitする
        res = browser.submit()
        res_html = res.read()
        soup = BeautifulSoup(res_html, "html.parser")

        res_attend = soup.findAll("div", attrs={"class": "attend"})[0].text
        res_attend = res_attend.strip()

        print (res_attend)
        reply = res_attend
    elif text == "check":
        #config.txtを読み込む
        config = ConfigParser.SafeConfigParser()
        conf = os.path.join(os.path.dirname(__file__),'config.txt')
        config.read([os.path.expanduser(conf)])
        #scraping
        browser = mechanize.Browser()
        #robot.txtを無効化しておくとちゃんと開ける
        browser.set_handle_robots(False)
        #URLを指定して読み込み　体育システムのURL


        #取得したhtmlを出力
            #print html.read()
        TOP_URL = 'https://wellness.sfc.keio.ac.jp/v3/'
        browser.open('https://wellness.sfc.keio.ac.jp/v3/')

        #0番目のフォームを選択
        browser.select_form(nr=0)
        #洗濯したフォームに値を設定
        browser.form['login'] = config.get('config','name')
        browser.form['password'] = config.get('config','password')
        #submitする
        res = browser.submit()
        res_html = res.read()
        soup = BeautifulSoup(res_html, "html.parser")

        tables = soup.find_all('ul')
        yidx = 0
        kakunin_url=""
        line_message=""
        for sk in tables:
            a = sk.findAll('a')
            for ak in a:
                if yidx == 1:
                    print("%s's url is %s" % (ak.text, ak.attrs['href']))
                    kakunin_url = ak.attrs['href']
                yidx += 1
        print (kakunin_url)
        kakunin_url = "https://wellness.sfc.keio.ac.jp"+kakunin_url
        res = browser.open(kakunin_url.decode("utf-8"))
        res_html = res.read()
        soup = BeautifulSoup(res_html, "html.parser")
        #print (soup)
        tables = soup.find_all('tr')
        idx = 0
        for sk in tables:
            p = sk.findAll('td')
            for pk in p:
                if re.match(u'[シ]',pk.text) or re.match(u'[予約]',pk.text) :
                    print ("　lkjlk")
                elif re.match('\(',pk.text):
                    line_message+="\n"
                else:
                    line_message+="\n"
                    line_message += pk.text
                    print ("%s" % pk.text)

        reply = "以下の授業が予約されています\n"
        reply += line_message
    elif text=="remove":
        #config.txtを読み込む
        config = ConfigParser.SafeConfigParser()
        conf = os.path.join(os.path.dirname(__file__),'config.txt')
        config.read([os.path.expanduser(conf)])
        #scraping
        browser = mechanize.Browser()
        #robot.txtを無効化しておくとちゃんと開ける
        browser.set_handle_robots(False)
        #URLを指定して読み込み　体育システムのURL


        #取得したhtmlを出力
            #print html.read()
        TOP_URL = 'https://wellness.sfc.keio.ac.jp/v3/'
        browser.open('https://wellness.sfc.keio.ac.jp/v3/')

        #0番目のフォームを選択
        browser.select_form(nr=0)
        #洗濯したフォームに値を設定
        browser.form['login'] = config.get('config','name')
        browser.form['password'] = config.get('config','password')
        #submitする
        res = browser.submit()
        res_html = res.read()
        soup = BeautifulSoup(res_html, "html.parser")

        tables = soup.find_all('ul')
        yidx = 0
        kakunin_url=""
        line_message=""
        for sk in tables:
            a = sk.findAll('a')
            for ak in a:
                if yidx == 1:
                    print("%s's url is %s" % (ak.text, ak.attrs['href']))
                    kakunin_url = ak.attrs['href']
                yidx += 1
        print (kakunin_url)
        kakunin_url = "https://wellness.sfc.keio.ac.jp"+kakunin_url
        res = browser.open(kakunin_url.decode("utf-8"))
        res_html = res.read()
        soup = BeautifulSoup(res_html, "html.parser")

        tables = soup.find_all('p')
        for sk in tables:
            if sk.text == u"現在予約している授業はありません．":
                reply = "現在予約している授業はありません．"

        #チェックボックスにチェックを入れる
        browser.select_form(nr=1)
        browser.find_control(type="checkbox").items[0].selected=True
        res=browser.submit()
        res_html = res.read()
        soup = BeautifulSoup(res_html, "html.parser")
        res_error = soup.findAll("p", attrs={"class": "error"})[0].text

        reply = res_error



    else:
        reply = random.choice(osomatsu_serif)

    payload = {
          "replyToken":reply_token,
          "messages":[
                {
                    "type":"text",
                    "text": reply
                }
            ]
    }

    requests.post(REPLY_ENDPOINT, headers=HEADER, data=json.dumps(payload)) # LINEにデータを送信
    return reply

def callback(request):
    reply = ""
    request_json = json.loads(request.body.decode('utf-8')) # requestの情報をdict形式で取得

    for e in request_json['events']:
        reply_token = e['replyToken']  # 返信先トークンの取得
        message_type = e['message']['type']   # typeの取得

        if message_type == 'text':
            text = e['message']['text']    # 受信メッセージの取得
            reply += reply_text(reply_token, text)   # LINEにセリフを送信する関数
    return HttpResponse(reply)  # テスト用
