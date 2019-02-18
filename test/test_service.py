import unittest
from src.service import RegistrationService, CommonStudentsService, SuspendStudentService, StudentsToNotifyService
from flask import Flask
from flaskext.mysql import MySQL
import json
from src.response_templates import *

class TestService(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.mysql_test = MySQL()

        # MySQL configurations
        self.app.config['MYSQL_DATABASE_USER'] = 'root'
        self.app.config['MYSQL_DATABASE_PASSWORD'] = '0027'
        self.app.config['MYSQL_DATABASE_DB'] = 'testschooladmin'
        self.app.config['MYSQL_DATABASE_HOST'] = 'localhost'
        self.mysql_test.init_app(self.app)

        # Initialize test database
        conn = self.mysql_test.connect()
        cursor = conn.cursor()
        cursor.callproc('init_db')

    def test_registration_service_input_val(self):
        self.input_val_helper(RegistrationService(MockPostRequest({"teacher": "teacher1@example.com", "students": ["student1@example.com", "student2@example.com"]})), True)
        self.input_val_helper(RegistrationService(MockPostRequest({})), False)
        self.input_val_helper(RegistrationService(MockPostRequest({"teacher": "", "students": ["student1@example.com", "student2@example.com"]})), False)
        self.input_val_helper(RegistrationService(MockPostRequest({"teacher": "teacher1@example.com", "students": ["", "student2@example.com"]})), False)
        self.input_val_helper(RegistrationService(MockPostRequest({"teacher": "teacher1@example.com", "students": []})), False)

    def test_common_students_service_input_val(self):
        self.input_val_helper(CommonStudentsService(MockGetRequest({"teacher": ["teacher1@example.com", "teacher2@example.com"]})), True)
        self.input_val_helper(CommonStudentsService(MockGetRequest({"teacher": ["", "teacher2@example.com"]})), False)
        self.input_val_helper(CommonStudentsService(MockGetRequest({"teacher": []})), False)
        self.input_val_helper(CommonStudentsService(MockGetRequest({})), False)

    def test_suspend_student_service_input_val(self):
        self.input_val_helper(SuspendStudentService(MockPostRequest({"student": "student1@example.com"})), True)
        self.input_val_helper(SuspendStudentService(MockPostRequest({"student": ""})), False)
        self.input_val_helper(SuspendStudentService(MockPostRequest({})), False)
    
    def test_students_to_notify_service_input_val(self):
        self.input_val_helper(StudentsToNotifyService(MockPostRequest({"teacher": "teacher1@example.com", "notification": "@student1@example.com"})), True)
        self.input_val_helper(StudentsToNotifyService(MockPostRequest({"teacher": "teacher1@example.com", "notification": ""})), True)
        self.input_val_helper(StudentsToNotifyService(MockPostRequest({"teacher": "", "notification": "@student1@example.com"})), False)
        self.input_val_helper(StudentsToNotifyService(MockPostRequest({})), False)

    def input_val_helper(self, service, expected):
        self.assertEqual(expected, service.is_valid_input())

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

if __name__ == '__main__':
    unittest.main() 