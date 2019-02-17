from app import app
from flask import jsonify, flash, request
from service import RegistrationService, CommonStudentsService, SuspendStudentService, StudentsToNotifyService

@app.route('/api/register', methods=['POST'])
def register_students():
    '''
    Registers a list of students to a specified teacher by their email addresses.

    Required inputs in the POST request body:
        teacher: A single string representing the teacher's email address.
        students: A list of strings representing different students' email addresses.
    '''
    service = RegistrationService(request)
    msg, status_code = service.register_students()
    return build_response(msg, status_code)

@app.route('/api/commonstudents', methods=['GET'])
def list_common_students():
    service = CommonStudentsService(request)
    msg, status_code = service.list_common_students()
    return build_response(msg, status_code)

@app.route('/api/suspend', methods=['POST'])
def suspend_student():
    service = SuspendStudentService(request)
    msg, status_code = service.suspend_student()
    return build_response(msg, status_code)

@app.route('/api/retrievefornotifications', methods=['POST'])
def retrieve_students_to_notify():
    service = StudentsToNotifyService(request)
    msg, status_code = service.retrieve_students_to_notify()
    return build_response(msg, status_code)

### Helper methods ###
def build_response(msg, status_code):
    response = jsonify(msg)
    response.status_code = status_code
    return response
    
def parse_registration_request(request_body):
    return request_body['teacher'], request_body['students']

if __name__ == "__main__":
    app.run()