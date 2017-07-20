# TaiikuSystembot

Heroku + Django
SFC体育システムの予約状況確認ができるlinebot
python 2.7.11

/bot/config.txt
name=SFCのログイン名
password=パスワード

を入力。

''$heroku create''

$git push heroku master

heroku createで作られたurlをコピーしておく。

Line developersにアクセス。
新しくline botを作成

webhook にコピーしたurlをはる
ACCESS TOKENをコピーして/bot/views.pyのACCESS TOKENの部分に貼り付け。

QRコードで友達登録する。


使い方
* command と打つとコマンド一覧が取得できる。
* check 現在の自分の予約状況の確認
* attend 出席状況の取得
* show 現在の予約状況の確認
* regi [ID] showで表示されたIDに対応した授業を予約
* remove 予約を削除 キュー

参考<http://qiita.com/yakan10/items/b7ad35c2cbba5db81462#_reference-cfc6654b05d0a7de3e40>
