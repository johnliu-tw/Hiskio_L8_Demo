import os
from flask import Flask, request, abort
import pymysql
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)


app = Flask(__name__)
line_bot_api = LineBotApi('raZHQLNB/R+nmfOVW1tnFjZNH+bCgVZUI2RrCOFhU4HN74vUIFqkbEy1Rk7X2GkEZKonNoYEJ2B0yJ4sB/tOhhaELQXfpqzTLt3TcJj5C8GkV+m5ej94h86ReYbZCF3gucwjVtSJ4y5i2fqKVp/sqQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('199884981ae351b96e9bb4998308d5e5')

@app.route('/')
def hello():
    return "Hello World!"

@app.route('/get_data')
def get_data():
    connection = pymysql.connect (host='localhost',
                                    user='john',
                                    password='password',
                                    db='news',
                                    cursorclass=pymysql.cursors.DictCursor) 
    with connection.cursor() as cursor:   
        cursor = connection.cursor()
        sql = ''' SELECT * FROM new_media.news'''
        cursor.execute(sql)
        data = cursor.fetchall()
    
    connection.close()
    return data

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
  line_bot_api.reply_message(event.reply_token,TextSendMessage(text=event.message.text))

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'
if __name__ == '__main__':
    app.run()