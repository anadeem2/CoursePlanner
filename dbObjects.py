
from time import sleep
from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from flask_session import Session
import os
from datetime import timedelta

app = Flask(__name__)
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

app.permanent_session_lifetime = timedelta(days=7)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///finaltest.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Application Configurations
app = Flask(__name__)
app.config["SESSION_TYPE"] = "filesystem"
Session(app)



class Student(db.Model):
    __tablename__ = 'Student'
    sID = db.Column(db.Integer, primary_key=True)
    sEmail = db.Column(db.String(200), nullable=False)
    sFName = db.Column(db.String(200), nullable=True)
    sLName = db.Column(db.String(200), nullable=True)
    sPassword = db.Column(db.String(200), nullable=False)
    sMajorID = db.Column(db.Integer, nullable=False)
    # sMajorID =  db.Column("sMajorID", ForeignKey(
    #     'Major.mID'), nullable=False)
    def __init__(self, email, password, fname, lname, majorID=1):
        self.sEmail = email
        self.sPassword = password
        self.sFName = fname
        self.sLName = lname
        self.sMajorID = majorID

    def __repr__(self):
        return self.sID
    
    def setMajorID(self,id: int):
        self.sMajorID = id

class Course(db.Model):
    __tablename__ = 'Course'
    cID = db.Column(db.Integer, primary_key=True)
    cCode = db.Column(db.String(10), nullable=False)  # IT383
    cName = db.Column(db.String(200), nullable=False)  # Operating Systems
    # Grade 5 = A 1 = F
    cGrade = db.Column(db.Float, nullable=True)
    # 1 = True 0 = False
    cTextbook = db.Column(db.Float, nullable=True)
    cOnline = db.Column(db.Float, nullable=True)
    cCredits = db.Column(db.Integer, nullable=False)
    # 1-5 scale 5 = most difficult
    cDifficulty = db.Column(db.Float, nullable=True)
    # skill suggestions
    cSkill = db.Column(db.String(200), nullable=True)
    # avg online
    cQuality = db.Column(db.Float, nullable=True)
    cStudentID = db.Column("cStudentID", ForeignKey(
        'Student.sID'), nullable=False)

    cStatus = db.Column(db.String(4), nullable=True)

    def __init__(self, studentID, code, name, credits):
        self.cStudentID = studentID
        self.cCode = code
        self.cName = name
        self.cCredits = credits

    def __repr__(self):
        return self.cCode + " - " + self.cName

class Major(db.Model):
    __tablename__ = 'Major'
    mID = db.Column(db.Integer, primary_key = True)
    mName = db.Column(db.String(50), nullable=False) # Computer Science

    def __int__(self, majorName):
        self.mName = majorName
    

    def __repr__(self):
        return self.mName


# class CourseList(db.Model):
#     __tablename__ = 'CourseList'
#     clID = db.Column(db.Integer, primary_key=True)
#     clStudentID = db.Column("clStudentID", ForeignKey(
#         'Student.sID'), nullable=False)
#     clCourseID = db.Column("clCourseID", ForeignKey(
#         'Course.cID'), nullable=False)
#     # 1 = Inprogress (IP), 2 =  Taken (T), 3 = Planned (P)
#     clStatus = db.Column(db.Integer, nullable=False)
#     clGrade = db.Column(db.String, nullable=True)

#     def __init__(self, stuID, courseID, status):
#         self.clStudentID = stuID
#         self.clCourseID = courseID
#         self.clStatus = status

#     def __repr__(self):
#         return self.clID


# class Data:
#     def __init__(self, id, name, email, phone):
#         self.id = id
#         self.name = name
#         self.email = email
#         self.phone = phone

def testMajor():
    db.session.query(Major).delete() #  nvm just try this tehn
    comSci = Major(mName='Computer Science')
    db.session.add(comSci)

    cyberSec = Major(mName='Cyber Security')
    db.session.add(cyberSec)
    
    infoTech = Major(mName='Information Technology') 
    db.session.add(infoTech)

    majors = Major.query.all()
    for major in majors:
        print(major)

def testStudent():
    # db.session.query(Student).delete()
    # db.session.execute("ALTER TABLE Student ADD sMajorID Integer")
    # db.session.commit()
    tjfreie = Student(email='tjfreie.ilstu.edu',password='password',fname='Tom',lname='Freier')
    db.session.add(tjfreie)
    db.session.commit()


if __name__ == '__main__':
    # Student.__table__.drop()
    db.create_all()
    db.session.commit()
    # testMajor()
    # testStudent()
    
    