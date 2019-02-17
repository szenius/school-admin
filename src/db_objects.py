class Teacher(object):
    '''
    Represents a row in the teacher table. Teachers have the following properties:

    Attributes:
        email: A string representing the teacher's email address. 
    '''
    def __init__(self, email):
        self.email = email
        self.sql_insert_template = "INSERT INTO teacher VALUES ( '{}' );"
    
    def insert_string(self):
        return self.sql_insert_template.format(self.email)

class Student(object):
    '''
    Represents a row in the student table. Students have the following properties:

    Attributes:
        email: A string representing the student's email address.
        is_suspended: A boolean indicating the student has been suspended.
    '''
    def __init__(self, email, is_suspended):
        self.email = email
        self.is_suspended = is_suspended
        self.sql_insert_template = "INSERT INTO student VALUES ( '{}', '{}' );"
        self.sql_suspend_template = "UPDATE student s SET s.is_suspended = '{}' WHERE s.email = '{}';"
        self.sql_check_suspend_template = "SELECT email FROM student s WHERE s.email IN ({}) AND s.is_suspended = 'false';"
    
    def insert_string(self):
        return self.sql_insert_template.format(self.email, self.is_suspended)

    def suspend_string(self):
        return self.sql_suspend_template.format(self.is_suspended, self.email)
    
    def check_suspension(self, emails=None):
        if not emails:
            emails = [self.email]
        return self.sql_check_suspend_template.format(','.join(['\'' + x + '\'' for x in emails]))

class Registration(object):
    '''
    Represents a row in the registration table. Links a teacher to a student registered under this teacher.

    Attributes:
        teacher_email: A string representing the email address of the teacher involved in this registration.
        student_email: A string representing the email address of the student involved in this registration.
    '''
    def __init__(self, teacher_email, student_email):
        self.teacher_email = teacher_email
        self.student_email = student_email

        self.sql_insert_template = "INSERT INTO registration VALUES( '{}', '{}' );"
        self.sql_search_students_template = "SELECT student_email FROM registration reg WHERE reg.teacher_email = '{}';"

    def insert_string(self):
        return self.sql_insert_template.format(self.teacher_email, self.student_email)

    def search_students(self):
        return self.sql_search_students_template.format(self.teacher_email)

    

