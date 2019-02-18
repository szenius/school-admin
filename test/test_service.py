import unittest
from src.service import RegistrationService, CommonStudentsService, SuspendStudentService, StudentsToNotifyService
from flask import Flask
from flaskext.mysql import MySQL
import json
from src.response_templates import *
import itertools

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
        try:
            conn = self.mysql_test.connect()
            cursor = conn.cursor()
            cursor.callproc('init_db')
            conn.commit()
        finally:
            cursor.close()
            conn.close()

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

    def test_register_students(self):
        try:
            conn = self.mysql_test.connect()

            # Check that the correct status code is returned
            teacher_email, student_emails = "teacher1@example.com", ["student1@example.com", "student2@example.com"]
            msg, status_code = RegistrationService(MockPostRequest({"teacher": teacher_email, "students": student_emails})).write_registration(conn)
            self.assertEqual(STATUS_CODE_POST_SUCCESS, status_code)

            # Test whether registrations are correctly added for each teacher-student pair
            cursor = conn.cursor()
            for student_email in student_emails:
                count = cursor.execute("SELECT * FROM registration r WHERE r.teacher_email = '{}' AND r.student_email = '{}';".format(teacher_email, student_email))
                conn.commit()
                self.assertEqual(1, count)
        finally:
            cursor.close()
            conn.close()

    def test_list_common_students(self):
        try:
            conn = self.mysql_test.connect()
            
            # First set up registrations in the db
            teacher1, teacher1_students = "teacher1@example.com", ["student1@example.com", "student3@example.com"]
            teacher2, teacher2_students = "teacher2@example.com", ["student1@example.com", "student2@example.com"]
            RegistrationService(MockPostRequest({"teacher": teacher1, "students": teacher1_students})).write_registration(conn)
            RegistrationService(MockPostRequest({"teacher": teacher2, "students": teacher2_students})).write_registration(conn)

            # Verify list of common students
            results, status_code = CommonStudentsService(MockGetRequest({"teacher": [teacher1, teacher2]})).get_common_students(conn)
            self.assertEqual(list(set(teacher1_students) & set(teacher2_students)), results['students'])
            self.assertEqual(STATUS_CODE_GET_SUCCESS, status_code)
        finally:
            conn.close()
    
    def test_suspend_student(self):
        try:
            conn = self.mysql_test.connect()

            # Invoke suspension
            student_email = "student1@example.com"
            msg, status_code = SuspendStudentService(MockPostRequest({"student": student_email})).write_suspension(conn)

            # Check if suspension was written to db
            cursor = conn.cursor()
            cursor.execute("SELECT is_suspended FROM student s WHERE s.email = '{}'".format(student_email))
            conn.commit()
            self.assertEqual(["true"], list(itertools.chain.from_iterable(cursor)))
        finally: 
            cursor.close()
            conn.close()

    def test_mentioned_students(self):
        self.assertEqual(["student1@example.com", "student9@example.com"], StudentsToNotifyService(MockPostRequest({"teacher": "teacher1@example.com", "notification": "@student1@example.com, @student9@example.com"})).get_mentioned_students())
        self.assertEqual([], StudentsToNotifyService(MockPostRequest({"teacher": "teacher1@example.com", "notification": ""})).get_mentioned_students())

    def test_remove_suspended_students(self):
        try:
            conn = self.mysql_test.connect()

            # Write a suspension to db
            suspended_student = "student1@example.com"
            SuspendStudentService(MockPostRequest({"student": suspended_student})).write_suspension(conn)

            # Check if suspended student is removed from list
            expected = ["student2@example.com"]
            cands = expected.copy()
            cands.append(suspended_student)
            results, status_code = StudentsToNotifyService(MockPostRequest({"teacher": "teacher1@example.com", "notification": ""})).remove_suspended_students(conn, cands)
            self.assertEqual(expected, results['recipients'])
            self.assertEqual(STATUS_CODE_GET_SUCCESS, status_code)
        finally:
            conn.close()


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