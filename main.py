# encoding: utf-8
import os
from flask import Flask, request, abort
import pymysql
from datetime import date, timedelta
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

import sys  
reload(sys)  
sys.setdefaultencoding('utf8')
type = sys.getfilesystemencoding()

app = Flask(__name__)
line_bot_api = LineBotApi('raZHQLNB/R+nmfOVW1tnFjZNH+bCgVZUI2RrCOFhU4HN74vUIFqkbEy1Rk7X2GkEZKonNoYEJ2B0yJ4sB/tOhhaELQXfpqzTLt3TcJj5C8GkV+m5ej94h86ReYbZCF3gucwjVtSJ4y5i2fqKVp/sqQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('199884981ae351b96e9bb4998308d5e5')

@app.route('/')
def hello():
    return "Hello World!"
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    connection = pymysql.connect (host='localhost',
                                    user='john',
                                    password='password',
                                    db='new_media',
                                    cursorclass=pymysql.cursors.DictCursor) 
    with connection.cursor() as cursor:   
        cursor = connection.cursor()
        text = ''
        if(event.message.text.find("article") != -1):
            date = event.message.text.split(' ')[0].decode('utf-8')
            brand = event.message.text.split(' ')[2].decode('utf-8')
            if( date == 'week' ):
                time = str(date.today() - timedelta(weeks = 1))
                sql = ''' SELECT * FROM new_media.news where date >={} and brand = {}'''.format(time, brand)
                cursor.execute(sql)
                articles = cursor.fetchall()
                for article in articles:
                    text = text + '''{}, 相關tag: {}, 分享數: {}, 來源: {} \n\n'''.format(article['title'], article['tag'], article['share'], article['brand'])
            else:
                sql = ''' SELECT * FROM new_media.news where date >={} and brand = "{}"'''.format(date, brand)
                cursor.execute(sql)
                articles = cursor.fetchall()
                for article in articles:
                    text = text + '''{}, 相關tag: {}, 分享數: {}, 來源: {} \n\n'''.format(article['title'], article['tag'], article['share'], article['brand'])
        if(event.message.text.find("facebook") != -1):
            date = event.message.text.split(' ')[0].decode('utf-8')
            if( date == 'week' ):
                text = '本週貼文總觸及人數為 1052 人, 推廣人數為 188 人, 共 55 個讚, 1009 個留言'
            else:
                text = date + '的貼文總觸及人數為 43 人, 推廣人數為 22 人, 共 17 個讚, 44 個留言'
        else:
            text = '看謀啦～'

    line_bot_api.reply_message(event.reply_token,TextSendMessage(text=text))
    connection.close()
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    # body = request.body.decode('utf-8')
    body = request.get_data(as_text=True).decode('utf-8')

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'
if __name__ == '__main__':
    app.run()
