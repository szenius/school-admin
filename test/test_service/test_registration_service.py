import unittest
import itertools
from src.service.registration_service import RegistrationService
from src.service.response_templates import STATUS_CODE_POST_SUCCESS
from .helper import MockPostRequest, setup_test_db

class TestService(unittest.TestCase):

    def setUp(self):
        self.mysql_test = setup_test_db()

    def test_registration_service_input_val(self):
        self.input_val_helper(RegistrationService(MockPostRequest({"teacher": "teacher1@example.com", "students": ["student1@example.com", "student2@example.com"]})), True)
        self.input_val_helper(RegistrationService(MockPostRequest({})), False)
        self.input_val_helper(RegistrationService(MockPostRequest({"teacher": "", "students": ["student1@example.com", "student2@example.com"]})), False)
        self.input_val_helper(RegistrationService(MockPostRequest({"teacher": "teacher1@example.com", "students": ["", "student2@example.com"]})), False)
        self.input_val_helper(RegistrationService(MockPostRequest({"teacher": "teacher1@example.com", "students": []})), False)

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


if __name__ == '__main__':
    unittest.main() 