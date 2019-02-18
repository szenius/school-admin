import unittest
import itertools
from src.service.registration_service import RegistrationService
from src.service.common_students_service import CommonStudentsService
from src.service.response_templates import STATUS_CODE_GET_SUCCESS
from .helper import MockGetRequest, MockPostRequest, setup_test_db

class TestService(unittest.TestCase):

    def setUp(self):
        self.mysql_test = setup_test_db()

    def test_common_students_service_input_val(self):
        self.input_val_helper(CommonStudentsService(MockGetRequest({"teacher": ["teacher1@example.com", "teacher2@example.com"]})), True)
        self.input_val_helper(CommonStudentsService(MockGetRequest({"teacher": ["", "teacher2@example.com"]})), False)
        self.input_val_helper(CommonStudentsService(MockGetRequest({"teacher": []})), False)
        self.input_val_helper(CommonStudentsService(MockGetRequest({})), False)

    def input_val_helper(self, service, expected):
        self.assertEqual(expected, service.is_valid_input())

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


if __name__ == '__main__':
    unittest.main() 