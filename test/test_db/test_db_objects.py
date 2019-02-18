import unittest
from src.db.db_objects import Teacher, Student, Registration

class TestDbObjects(unittest.TestCase):
    def test_teacher_insert_string(self):
        email = "teacher@example.com"
        teacher = Teacher(email)
        expected_insert_string = "INSERT INTO teacher VALUES ( '{}' );".format(email)
        self.assertEqual(expected_insert_string, teacher.insert_string())   
    
    def test_student_insert_string(self):
        email, is_suspended = "student@example.com", "false"
        student = Student(email, is_suspended)
        expected_insert_string = "INSERT INTO student VALUES ( '{}', '{}' );".format(email, is_suspended)
        self.assertEqual(expected_insert_string, student.insert_string())
    
    def test_student_suspend_string(self):
        email, is_suspended = "student@example.com", "true"
        student = Student(email, is_suspended)
        expected_suspend_string = "UPDATE student s SET s.is_suspended = '{}' WHERE s.email = '{}';".format(is_suspended, email)
        self.assertEqual(expected_suspend_string, student.suspend_string())

    def test_student_check_suspension(self):
        emails = ['example0@example.com', 'example1@example.com']
        student = Student(emails[0], None)
        expected_check_suspension_string = "SELECT email FROM student s WHERE s.email IN ('{}','{}') AND s.is_suspended = 'false';".format(emails[0], emails[1])
        self.assertEqual(expected_check_suspension_string, student.check_suspension(emails=emails))
        expected_check_suspension_string = "SELECT email FROM student s WHERE s.email IN ('{}') AND s.is_suspended = 'false';".format(emails[0])
        self.assertEqual(expected_check_suspension_string, student.check_suspension())

    def test_registration_insert_string(self):
        teacher_email, student_email = "teacher@example.com", "student@example.com"
        registration = Registration(teacher_email, student_email)
        expected_insert_string = "INSERT INTO registration VALUES ( '{}', '{}' );".format(teacher_email, student_email)
        self.assertEqual(expected_insert_string, registration.insert_string())
    
    def test_registration_search_students_by_teacher(self):
        teacher_email = "teacher@example.com"
        registration = Registration(teacher_email, None)
        expected_search_string = "SELECT student_email FROM registration reg WHERE reg.teacher_email = '{}';".format(teacher_email)
        self.assertEqual(expected_search_string, registration.search_students())


if __name__ == '__main__':
    unittest.main() 