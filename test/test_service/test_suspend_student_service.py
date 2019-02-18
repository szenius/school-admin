import unittest
import itertools
from src.service.suspend_students_service import SuspendStudentService
from .helper import MockPostRequest, setup_test_db
from src.service.response_templates import STATUS_CODE_POST_SUCCESS

class TestService(unittest.TestCase):

    def setUp(self):
        self.mysql_test = setup_test_db()

    def test_suspend_student_service_input_val(self):
        self.input_val_helper(SuspendStudentService(MockPostRequest({"student": "student1@example.com"})), True)
        self.input_val_helper(SuspendStudentService(MockPostRequest({"student": ""})), False)
        self.input_val_helper(SuspendStudentService(MockPostRequest({})), False)
    
    def input_val_helper(self, service, expected):
        self.assertEqual(expected, service.is_valid_input())

    def test_suspend_student(self):
        try:
            conn = self.mysql_test.connect()

            # Invoke suspension
            student_email = "student1@example.com"
            msg, status_code = SuspendStudentService(MockPostRequest({"student": student_email})).write_suspension(conn)
            self.assertEqual(STATUS_CODE_POST_SUCCESS, status_code)

            # Check if suspension was written to db
            cursor = conn.cursor()
            cursor.execute("SELECT is_suspended FROM student s WHERE s.email = '{}'".format(student_email))
            conn.commit()
            self.assertEqual(["true"], list(itertools.chain.from_iterable(cursor)))
        finally: 
            cursor.close()
            conn.close()


if __name__ == '__main__':
    unittest.main() 