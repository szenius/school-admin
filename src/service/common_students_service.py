import pymysql
from .response_templates import MSG_LIST_STUDENTS_SERVER_ERROR, MSG_LIST_STUDENTS_WRONG_INPUT
from .response_templates import STATUS_CODE_BAD_REQUEST, STATUS_CODE_GET_SUCCESS, STATUS_CODE_SERVER_ERROR
from ..db.db_objects import Registration
from ..db.db_config import mysql
import itertools

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