import os
from flask import Flask
import pymysql

app = Flask(__name__)


@app.route('/')
def hello():
    return "Hello World!"

@app.route('/get_data')
def get_data():
  connection = pymysql.connect (host='localhost',
                              user='root',
                              password='password',
                              db='new_media',
                              cursorclass=pymysql.cursors.DictCursor)
    return "Hello World!"

if __name__ == '__main__':
    app.run()