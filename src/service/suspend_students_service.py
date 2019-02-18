import pymysql
from .response_templates import MSG_SUSPENSION_SERVER_ERROR, MSG_SUSPENSION_WRONG_INPUT, MSG_EMPTY_RESPONSE
from .response_templates import STATUS_CODE_BAD_REQUEST, STATUS_CODE_POST_SUCCESS, STATUS_CODE_SERVER_ERROR
from ..db.db_objects import Student
from ..db.db_config import mysql

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
