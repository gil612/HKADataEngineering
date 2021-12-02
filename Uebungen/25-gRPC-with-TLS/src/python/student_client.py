"""Python gRPC student client"""

from __future__ import print_function
import logging
import grpc
import time

import student_pb2
import student_pb2_grpc

# retrieve information about a student with specified givenname and surname
def list_student(stub,surname,givenname):
    # ListStudent: unary method call to gRPC server
    response=stub.ListStudent(student_pb2.Name(
        surname=surname,givenname=givenname
    ))
    return response

# print information about a student
def print_student(response,surname,givenname):
    if (response.exists):
        print('\tStudent {} {} is borne in year {}.'.format(givenname,surname,response.yearOfBirth))
    else:
        print('\tStudent {} {} is not enrolled.'.format(givenname,surname))


def run():
    # read public certificate
    with open('..\..\certificate\server.crt', 'rb') as f:
        trusted_certs = f.read()
    # create credentials
    credentials = grpc.ssl_channel_credentials(root_certificates=trusted_certs)
    # open connection to gRPC server
    with grpc.secure_channel('md2c0gdc:5001',credentials=credentials) as channel:
        # get communication channel
        stub = student_pb2_grpc.StudentsStub(channel)
        print('Getting information about student Sebastian Birkenmeier ...')
        # get information about student Sebastian Birkenmeier from server
        response=list_student(stub,surname='Birkenmeier',givenname='Sebastian')
        print_student(response,surname='Birkenmeier',givenname='Sebastian')
        print('Getting information about student Richard Mueller ...')
        response=list_student(stub,surname='Mueller',givenname='Richard')
        print_student(response,surname='Mueller',givenname='Richard')
        faculties=[student_pb2.Faculty.FacultyName.InformatikWirtschaftsinformatik,
            student_pb2.Faculty.FacultyName.ArchitekturBauwesen]
        for faculty in faculties:
            print('Retrieving students enrolled at faculty {}.'.format(faculty))
            students=stub.ListStudents(student_pb2.Faculty(facultyname=faculty))
            cnt=0
            for student in students:
                # time.sleep(0.5)
                print('{})\t{}\t{}\t{}'.format(cnt,student.name.surname,student.name.givenname,student.yearOfBirth))
                cnt+=1
            if cnt==0:
                print('No students are enrolled to faculty {}.'.format(faculty))
        print('Retrieving all students (streaming for ever in 5 seconds)')
        time.sleep(5)
        # Initiate streaming method call to gRPC server
        # gRPC server responds with never ending random information about students
        # parameter: faculty name as "filter"
        students=stub.ListStudents(student_pb2.Faculty(facultyname=student_pb2.Faculty.FacultyName.Unspecified))
        cnt=0
        for student in students:
            #time.sleep(0.05)
            print('{})\t{}\t{}\t{}'.format(cnt,student.name.surname,student.name.givenname,student.yearOfBirth))
            cnt+=1

if __name__ == '__main__':
    logging.basicConfig()
    run()