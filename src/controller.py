from flask import jsonify, flash, request
from .service import RegistrationService, CommonStudentsService, SuspendStudentService, StudentsToNotifyService
from .app import app

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
    '''
    Given a list of teachers' email addresses, return all students that are registered with all of the given teachers.

    Required inputs in the GET params:
        teacher: A string representing the teacher's email address. Multiple inputs of this param is allowed.
    '''
    service = CommonStudentsService(request)
    msg, status_code = service.list_common_students()
    return build_response(msg, status_code)

@app.route('/api/suspend', methods=['POST'])
def suspend_student():
    '''
    Given a specific student's email address, mark this student as suspended.

    Required inputs in the POST request body:
        student: A string representing the student's email address.
    '''
    service = SuspendStudentService(request)
    msg, status_code = service.suspend_student()
    return build_response(msg, status_code)

@app.route('/api/retrievefornotifications', methods=['POST'])
def retrieve_students_to_notify():
    '''
    Given a teacher's email address and a notification message, return the list of students which the notification should be sent to.
    A student should receive the notification only if 
        (1) He or she is not suspended, and 
        (2) He or she is registered with the teacher OR he or she is mentioned in the notification message.

    Required inputs in the POST request body:
        teacher: A string representing the the teacher's email address.
        notification: A string representing the notification message to be sent out.
    '''
    service = StudentsToNotifyService(request)
    msg, status_code = service.retrieve_students_to_notify()
    return build_response(msg, status_code)

def build_response(msg, status_code):
    response = jsonify(msg)
    response.status_code = status_code
    return response
    
def main():
    app.run()

if __name__ == "__main__":
    main()
