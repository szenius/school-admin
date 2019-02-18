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
        if not ('teacher' in request_json and 'students' in request_json):
            self.teacher_email = None
            self.student_emails = None 
        else:
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
        if not (self.teacher_email and self.student_emails):
            return False
        for student_email in self.student_emails:
            if not student_email:
                return False
        return True

class CommonStudentsService(object):
    '''
    Service object that takes care of listing students who are all registered to a given group of teachers.
    '''

    def __init__(self, request, teacher_emails=None):
        if not ((request and request.args.getlist('teacher')) or teacher_emails):
            self.teacher_emails = None
        elif not teacher_emails:
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
            return self.get_common_students(conn)
        finally:
            conn.close()

    def get_common_students(self, conn):
        try:
            cursor = conn.cursor()

            results = []
            for teacher_email in self.teacher_emails:
                registration = Registration(teacher_email, None)
                cursor.execute(registration.search_students())
                conn.commit()

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

    def is_valid_input(self):
        if not self.teacher_emails:
            return False
        for teacher_email in self.teacher_emails:
            if not teacher_email:
                return False
        return True

class SuspendStudentService(object):
    '''
    Service object that takes care of suspending a specified student.
    '''

    def __init__(self, request):
        request_json = request.json
        if 'student' not in request_json:
            self.student_email = None
        else:
            self.student_email = request_json['student']

    def suspend_student(self):
        # Input validation
        if not self.is_valid_input():
            return {"message": MSG_SUSPENSION_WRONG_INPUT}, STATUS_CODE_BAD_REQUEST
        
        # Write suspension into student table
        try:
            conn = mysql.connect()
            return self.write_suspension(conn)
        finally:
            conn.close()
    
    def write_suspension(self, conn):
        try:
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

    def is_valid_input(self):
        return bool(self.student_email)

class StudentsToNotifyService(object):
    '''
    Service object that retrieves students to be notified.
    '''

    def __init__(self, request):
        request_json = request.json
        if not ('teacher' in request_json and 'notification' in request_json):
            self.teacher_email = None
            self.notification = None
        else:
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
        try:
            conn = mysql.connect()
            return self.remove_suspended_students(conn, cands)
        finally:
            conn.close()
    
    def remove_suspended_students(self, conn, cands):
        student = Student(None, None)
        try:
            cursor = conn.cursor()
            cursor.execute(student.check_suspension(emails=cands))
            recipients = list(itertools.chain.from_iterable(cursor))
            return {"recipients": recipients}, STATUS_CODE_GET_SUCCESS
        except Exception as e:
            print(e)
            return MSG_NOTIFY_SERVER_ERROR, STATUS_CODE_SERVER_ERROR
        finally:
            cursor.close()

    def get_registered_students(self):
        common_students_service = CommonStudentsService(None, teacher_emails=[self.teacher_email])
        registered_students, status_code = common_students_service.list_common_students()
        if status_code != STATUS_CODE_GET_SUCCESS:
            return registered_students, status_code
        return registered_students['students']
    
    def get_mentioned_students(self):
        return [str[1:] for str in re.findall(r'@[\w\.-]+@[\w\.-]+', self.notification)]

    def is_valid_input(self):
        return bool(self.notification is not None and self.teacher_email)



