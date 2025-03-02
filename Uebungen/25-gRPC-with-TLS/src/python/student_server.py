# for certificates see https://www.sandtable.com/using-ssl-with-grpc-in-python/
# creation of self-signed certificate with openssl
# IMPORTANT: "Common Name" must match the hostname of the laptop
# openssl req -newkey rsa:2048 -nodes -keyout server.key -x509 -days 365 -out server.crt

"""Python implementation of the student server"""

from concurrent import futures
import logging

# Faker creates random names, ...
from faker import Faker
import grpc
# class information generated by proto compiler
import student_pb2
# method information generated by proto compiler
import student_pb2_grpc
import pandas as pd

fake=Faker()

# read students of faculty WI-IWI from csv-file
def read_students_database()->pd.DataFrame:
    df=pd.read_csv('../../data/students.csv',delimiter=';')
    df['facultyname']=student_pb2.Faculty.FacultyName.InformatikWirtschaftsinformatik
    return df

# check whether student exists and return information from dataframe
def get_student(students_db,name:student_pb2.Name):
    # filter dataframe by surname and givenname
    df=students_db[(students_db['surname'] == name.surname) & (students_db['givenname'] == name.givenname) ]
    # check whether student exists
    if df.shape[0]>0:
        # create student information (as defined in student.proto)
        student=student_pb2.Student(
            name=name,
            faculty=student_pb2.Faculty(facultyname=3),
            yearOfBirth=fake.random_int(min=17,max=35,step=1),
            exists=True
        )
        return student
    else:
        # student does not exist
        # create student information (as defined in student.proto)
        return student_pb2.Student(
            name=name,
            faculty=student_pb2.Faculty(facultyname=0),
            yearOfBirth=0,
            exists=False
        )

# get random student information (as defined in student.proto)
def get_student_random():
    student=student_pb2.Student(
        name=student_pb2.Name(
            surname=fake.name(),
            givenname=fake.name()
        ),
        faculty=student_pb2.Faculty(facultyname=3),
        yearOfBirth=fake.random_int(min=17,max=35,step=1)
    )
    return student

# implement StudentsServicer (service Students as defined in student.proto)
class StudentServicer(student_pb2_grpc.StudentsServicer):
    def __init__(self):
        self.students_db=read_students_database()

    # interface defined in proto file
    def ListStudent(self, request, context):
        # get information about student from dataframe
        student=get_student(self.students_db,request)
        return student

    # interface defined in proto file
    # parameter request contains the faculty
    def ListStudents(self, request, context):
        # create random information and stream for ever if no faculty is specified
        if request.facultyname==student_pb2.Faculty.FacultyName.Unspecified:
            while(True):
                yield get_student_random()
        else:
            # search in dataframe students_db for students that belong to the specified faculty
            df=self.students_db[self.students_db['facultyname']==request.facultyname]
            for index,row in df.iterrows():
                # create student information (as defined in student.proto)
                student=student_pb2.Student(
                    name=student_pb2.Name(
                        surname=row['surname'],
                        givenname=row['givenname']
                    ),
                    faculty=request, # student_pb2.Faculty(facultyname=3),
                    yearOfBirth=fake.random_int(min=17,max=35,step=1),
                    exists=True
                )
                yield student
    
def serve():
    # instantiate the grpc server
    server=grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    student_pb2_grpc.add_StudentsServicer_to_server(StudentServicer(),server)
    # open port for insecure communication
    #server.add_insecure_port('[::]:50051')
    # read private key
    with open('..\..\certificate\server.key', 'rb') as f:
        private_key = f.read()
    # read public certificate
    with open('..\..\certificate\server.crt', 'rb') as f:
        certificate_chain = f.read()
    # create server credentials
    server_credentials = grpc.ssl_server_credentials(((private_key, certificate_chain,),))

    server.add_secure_port('[::]:5001', server_credentials)
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    logging.basicConfig()
    serve()