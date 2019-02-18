import unittest
from src.service.suspend_students_service import SuspendStudentService
from src.service.notify_students_service import StudentsToNotifyService
from src.service.response_templates import STATUS_CODE_GET_SUCCESS
from .helper import MockPostRequest, setup_test_db


class TestService(unittest.TestCase):

    def setUp(self):
        self.mysql_test = setup_test_db()

    def test_input_val(self):
        self.input_val_helper(StudentsToNotifyService(MockPostRequest({"teacher": "teacher1@example.com", "notification": "@student1@example.com"})), True)
        self.input_val_helper(StudentsToNotifyService(MockPostRequest({"teacher": "teacher1@example.com", "notification": ""})), True)
        self.input_val_helper(StudentsToNotifyService(MockPostRequest({"teacher": "", "notification": "@student1@example.com"})), False)
        self.input_val_helper(StudentsToNotifyService(MockPostRequest({})), False)

    def input_val_helper(self, service, expected):
        self.assertEqual(expected, service.is_valid_input())

    def test_notify_mentioned_students(self):
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


if __name__ == '__main__':
    unittest.main() 