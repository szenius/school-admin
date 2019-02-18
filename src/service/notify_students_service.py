import pymysql
from .response_templates import MSG_NOTIFY_SERVER_ERROR, MSG_NOTIFY_WRONG_INPUT
from .response_templates import STATUS_CODE_BAD_REQUEST, STATUS_CODE_GET_SUCCESS, STATUS_CODE_SERVER_ERROR
from ..db.db_objects import Student
from ..db.db_config import mysql
from .common_students_service import CommonStudentsService
import itertools
import re

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