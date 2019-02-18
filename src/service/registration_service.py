import pymysql
from .response_templates import MSG_REGISTRATION_WRONG_INPUT, MSG_REGISTRATION_SERVER_ERROR, MSG_EMPTY_RESPONSE
from .response_templates import STATUS_CODE_BAD_REQUEST, STATUS_CODE_POST_SUCCESS, STATUS_CODE_SERVER_ERROR
from ..db.db_objects import Registration
from ..db.db_config import mysql

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
