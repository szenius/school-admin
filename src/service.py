import pymysql
from .response_templates import *
from .db_objects import Teacher, Student, Registration
from .db_config import mysql
import itertools
import re

class RegistrationService(object):
    '''
    Service object that takes care of registering pairs of teachers and students.
    '''

    def __init__(self, request):
        request_json = request.json
        self.teacher_email = request_json['teacher']
        self.student_emails = request_json['students']

    def register_students(self):
        # Input validation
        if not self.is_valid_input():
            return {"message": MSG_REGISTRATION_WRONG_INPUT}, STATUS_CODE_BAD_REQUEST

        # Write registration to database
        try:
            conn = mysql.connect()
            return self.write_registration(conn)
        finally: 
            conn.close()

    def write_registration(self, conn):
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            
            for student_email in self.student_emails:
                registration = Registration(self.teacher_email, student_email)
                cursor.execute(registration.insert_string())
                conn.commit()
            
            return MSG_EMPTY_RESPONSE, STATUS_CODE_POST_SUCCESS
        except Exception as e:
            print(e)
            return {"message": MSG_REGISTRATION_SERVER_ERROR}, STATUS_CODE_SERVER_ERROR
        finally: 
            cursor.close()
            
    def is_valid_input(self):
        return self.teacher_email and self.student_emails and len(self.student_emails) != 0

class CommonStudentsService(object):
    def __init__(self, request, teacher_emails=None):
        if not teacher_emails:
            self.teacher_emails = request.args.getlist('teacher')
        else:
            self.teacher_emails = teacher_emails

    def list_common_students(self):
        # Input validation
        if not self.is_valid_input():
            return {"message": MSG_LIST_STUDENTS_WRONG_INPUT}, STATUS_CODE_BAD_REQUEST
                
        # Get list of common students from database
        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            results = []
            for teacher_email in self.teacher_emails:
                registration = Registration(teacher_email, None)
                cursor.execute(registration.search_students())

                if len(results) == 0:
                    results.extend(list(list(itertools.chain.from_iterable(cursor))))
                else:
                    results = list(set(results) & set(list(list(itertools.chain.from_iterable(cursor)))))
                                    
            return {"students": results}, STATUS_CODE_GET_SUCCESS
        except Exception as e:
            print(e)
            return {"message": MSG_LIST_STUDENTS_SERVER_ERROR}, STATUS_CODE_SERVER_ERROR
        finally: 
            cursor.close()
            conn.close()

    def is_valid_input(self):
        return self.teacher_emails and len(self.teacher_emails) != 0

class SuspendStudentService(object):
    def __init__(self, request):
        request_json = request.json
        self.student_email = request_json['student']

    def suspend_student(self):
        # Input validation
        if not self.is_valid_input():
            return {"message": MSG_SUSPENSION_WRONG_INPUT}, STATUS_CODE_BAD_REQUEST
        
        # Write suspension into student table
        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            student = Student(self.student_email, 'true')
            cursor.execute(student.suspend_string())
            conn.commit()
            
            return MSG_EMPTY_RESPONSE, STATUS_CODE_POST_SUCCESS
        except Exception as e:
            print(e)
            return {"message": MSG_SUSPENSION_SERVER_ERROR}, STATUS_CODE_SERVER_ERROR
        finally:
            cursor.close()
            conn.close()

    def is_valid_input(self):
        return self.student_email and len(self.student_email) != 0

class StudentsToNotifyService(object):
    def __init__(self, request):
        request_json = request.json
        self.teacher_email = request_json['teacher']
        self.notification = request_json['notification']
    
    def retrieve_students_to_notify(self):
        # Input validation
        if not self.is_valid_input():
            return {"message": MSG_NOTIFY_WRONG_INPUT}, STATUS_CODE_BAD_REQUEST

        # Retrieve students registered under this teacher
        cands = self.get_registered_students()

        # Get list of students mentioned in notification
        cands.extend(self.get_mentioned_students())
        cands = list(set(cands))

        # Return only the students that are not suspended
        student = Student(None, None)
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(student.check_suspension(emails=cands))
            recipients = list(itertools.chain.from_iterable(cursor))

            return {"recipients": recipients}, STATUS_CODE_GET_SUCCESS
        except Exception as e:
            print(e)
            return MSG_NOTIFY_SERVER_ERROR, STATUS_CODE_SERVER_ERROR
        finally:
            cursor.close()
            conn.close()

    def get_registered_students(self):
        common_students_service = CommonStudentsService(None, teacher_emails=[self.teacher_email])
        registered_students, status_code = common_students_service.list_common_students()
        if status_code != STATUS_CODE_GET_SUCCESS:
            return registered_students, status_code
        return registered_students['students']
    
    def get_mentioned_students(self):
        return [str[1:] for str in re.findall(r'@[\w\.-]+@[\w\.-]+', self.notification)]

    def is_valid_input(self):
        return self.teacher_email and self.notification and len(self.teacher_email) != 0



