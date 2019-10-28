import os
from flask import Flask
import pymysql
from dotenv import load_dotenv
load_dotenv()

USER = os.getenv("DB_USER")
PASSWORD = os.getenv("DB_PASSWORD")
SCHEMA = os.getenv("DB_SCHEMA")

app = Flask(__name__)


@app.route('/')
def hello():
    return "Hello World!"

@app.route('/get_data')
def get_data():
    connection = pymysql.connect (host='localhost',
                              user=USER,
                              password=PASSWORD,
                              db=SCHEMA,
                              cursorclass=pymysql.cursors.DictCursor) 
    with connection.cursor() as cursor:   
        cursor = connection.cursor()
        sql = ''' SELECT * FROM new_media.news'''
        cursor.execute(sql)
        data = cursor.fetchall()
    
    connection.close()
    return data
if __name__ == '__main__':
    app.run()