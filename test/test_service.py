import unittest
from src.service import RegistrationService, CommonStudentsService, SuspendStudentService, StudentsToNotifyService
from flask import Flask
from flaskext.mysql import MySQL
import json

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

    def test_registration_service(self):
        mock_request = MockPostRequest({"teacher": "teacher@example.com", "students": ["student1@example.com", "student2@example.com"]})
        service = RegistrationService(mock_request)

class MockPostRequest(object):
    def __init__(self, json_data):
        self.json = json_data

if __name__ == '__main__':
    unittest.main() 