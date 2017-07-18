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
ACCESS_TOKEN = 'cf6MkYQIETJ7+jKqHJxVXDqOjHAGrTNfALgyds2qfY3HIslXGQ7GSAGJpALAa2TAZnLNT6u885N6P6w2BB2Qj1EQpdoiQjut0IVAWBlTOikyJwBbnYeAnRj9po9bwmCTJKH/ciE0bAJ+8PbtAOtERAdB04t89/1O/w1cDnyilFU='
HEADER = {
    "Content-Type": "application/json",
    "Authorization": "Bearer " + ACCESS_TOKEN
}

def index(request):
    return HttpResponse("This is bot api.")



def reply_text(reply_token, text):

    #config.txtを読み込む
    config = ConfigParser.SafeConfigParser()
    conf = os.path.join(os.path.dirname(__file__),'config.txt')
    config.read([os.path.expanduser(conf)])

    # show 予約情報の表示


    # 説明　正規表現
    explain = re.compile("explain*")

    reply = ""
    if text == "show":
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
        tables = soup.find_all('tr',class_='alt')
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
        		else:
        			line_message+="\n"
        			line_message += pk.text
    				print ("%s" % pk.text)

        reply = line_message;
    elif text == "regi":
        for i in range(int(split_text[0])):
            reply  += str([random.randint(1,int(split_text[1]))])
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
