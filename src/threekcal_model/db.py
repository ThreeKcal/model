import pymysql.cursors
import os

def get_connection():

    connection = pymysql.connect(host=os.getenv("DB_IP",'localhost'),
                                 port =int(os.getenv("DB_PORT", "53306")),
                                 user = 'master', password = '1234',
                                 database = 'modeldb',
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection
