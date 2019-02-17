DROP DATABASE schooladmin;

CREATE DATABASE schooladmin;
USE schooladmin;

CREATE TABLE teacher ( 
    email varchar(254) NOT NULL PRIMARY KEY
);

CREATE TABLE student (
    email VARCHAR(254) NOT NULL PRIMARY KEY,
    is_suspended VARCHAR(5) NOT NULL,
    CONSTRAINT check_is_suspended CHECK (is_suspended IN ('true', 'false'))
);

CREATE TABLE registration (
    teacher_email varchar(254) NOT NULL REFERENCES teacher(email),
    student_email varchar(254) NOT NULL REFERENCES student(email),
    PRIMARY KEY (teacher_email, student_email)
);

INSERT INTO teacher VALUES ( 'teacher1@example.com' );
INSERT INTO teacher VALUES ( 'teacher2@example.com' );
INSERT INTO teacher VALUES ( 'teacher3@example.com' );
INSERT INTO teacher VALUES ( 'teacher4@example.com' );
INSERT INTO teacher VALUES ( 'teacher5@example.com' );
INSERT INTO teacher VALUES ( 'teacher6@example.com' );
INSERT INTO teacher VALUES ( 'teacher7@example.com' );
INSERT INTO teacher VALUES ( 'teacher8@example.com' );
INSERT INTO teacher VALUES ( 'teacher9@example.com' );

INSERT INTO student VALUES ( 'student1@example.com', 'false' );
INSERT INTO student VALUES ( 'student2@example.com', 'false' );
INSERT INTO student VALUES ( 'student3@example.com', 'false' );
INSERT INTO student VALUES ( 'student4@example.com', 'false' );
INSERT INTO student VALUES ( 'student5@example.com', 'false' );
INSERT INTO student VALUES ( 'student6@example.com', 'false' );
INSERT INTO student VALUES ( 'student7@example.com', 'false' );
INSERT INTO student VALUES ( 'student8@example.com', 'false' );
INSERT INTO student VALUES ( 'student9@example.com', 'false' );