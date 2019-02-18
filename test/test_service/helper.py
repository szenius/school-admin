from flask import Flask
from flaskext.mysql import MySQL

class MockPostRequest(object):
    def __init__(self, json_data):
        self.json = json_data


class MockGetRequest(object):
    def __init__(self, data):
        self.args = Args(data)


class Args(object):
    def __init__(self, data):
        self.data = data
    
    def getlist(self, key):
        return self.data[key] if key in self.data else None


def setup_test_db():        
    app = Flask(__name__)
    mysql_test = MySQL()

    # MySQL configurations
    app.config['MYSQL_DATABASE_USER'] = 'root'
    app.config['MYSQL_DATABASE_PASSWORD'] = '0027'
    app.config['MYSQL_DATABASE_DB'] = 'testschooladmin'
    app.config['MYSQL_DATABASE_HOST'] = 'localhost'
    mysql_test.init_app(app)

    # Initialize test database
    try:
        conn = mysql_test.connect()
        cursor = conn.cursor()
        cursor.callproc('init_db')
        conn.commit()
    finally:
        cursor.close()
        conn.close()
    
    return mysql_test
