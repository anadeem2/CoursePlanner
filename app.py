from time import sleep
from turtle import st
import csv
from flask import Flask, redirect, render_template, request, jsonify, url_for, session, flash
from flask_session import Session
# from cs50 import SQL
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from flask_mail import Mail, Message
import os
from random import randint
from datetime import timedelta


# Application Configurations
app = Flask(__name__)
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
app.permanent_session_lifetime = timedelta(days=7)
app.config["MAIL_DEFAULT_SENDER"] = "classplannerit326@gmail.com"
app.config['MAIL_USERNAME'] = "classplannerit326@gmail.com"
app.config['MAIL_PASSWORD'] = "Planner123!"
app.config['MAIL_PORT'] = 587
app.config['MAIL_SERVER'] = "smtp.gmail.com"
app.config['MAIL_USE_TLS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///finaltest.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# # Intitializations
# db = SQL('sqlite:///planner.db')
mail = Mail(app)
user = None
COURSES = None
message = ''
userID = None

class Student(db.Model):
    __tablename__ = 'Student'
    sID = db.Column(db.Integer, primary_key=True)
    sEmail = db.Column(db.String(200), nullable=False)
    sFName = db.Column(db.String(200), nullable=True)
    sLName = db.Column(db.String(200), nullable=True)
    sPassword = db.Column(db.String(200), nullable=False)
    sMajorID = db.Column(db.Integer, nullable=False)
    def __init__(self, email, password, fname, lname, sMajorID=1):
        self.sEmail = email
        self.sPassword = password
        self.sFName = fname
        self.sLName = lname
        self.sMajorID = sMajorID

    def __repr__(self):
        return self.sID


class Course(db.Model):
    __tablename__ = 'Course'
    cID = db.Column(db.Integer, primary_key=True)
    cCode = db.Column(db.String(10), nullable=False)  # IT383
    cName = db.Column(db.String(200), nullable=False)  # Operating Systems
    # Grade 4=A, 3.5=B, etc
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


class CourseBank(db.Model):
    cID = db.Column(db.Integer, primary_key=True)
    cDept = db.Column(db.String(200), nullable=False)  # IT
    cCode = db.Column(db.String(20), nullable=False)  # 383
    cName = db.Column(db.String(200), nullable=False)  # Operating Systems
    cCredits = db.Column(db.String(20), nullable=False)
    cDesc = db.Column(db.String(200), nullable=False)
    
    def __init__(self, dept,code,name,credits,desc):
        self.cDept = dept
        self.cCode = code
        self.cName = name
        self.cCredits = credits
        self.cDesc = desc

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


# x = Data(1, "IT327", "email@", "3095555555")
# # COURSES = [x]
# user = None
# COURSES = None


@ app.route('/')
def index():
    global COURSES

    if "email" not in session:  # Check if session doesn't exist
        return render_template("index.html")

    # return render_template('dashboard.html', courses=COURSES)
    return render_template("mainpage.html", courses=COURSES)


@ app.route('/login')  # Login page
def login():
    return render_template("login.html")


@ app.route('/logout')  # Logout
def logout():
    session.pop("email", None)
    global user
    global COURSES
    COURSES = user = None
    return render_template("login.html")


@ app.route('/forgot', methods=["POST", "GET"])  # Login page
def forgot():
    if request.method == 'POST':
        user_email = request.form.get("email")
        exists = Student.query.filter_by(sEmail=user_email).first()
        if exists:
            message = Message(
                "Your forgotten password: " + exists.sPassword, recipients=[user_email])
            mail.send(message)
            flash("Email with password sucessfully sent")
            return redirect(url_for("login"))
        else:
            flash("Invalid email, please sign up")
            return redirect(url_for("signup"))
    else:
        return render_template("forgot.html")


@ app.route('/signup')  # Signup page
def signup():
    return render_template("signup.html")


@ app.route('/registered', methods=["POST"])  # Registered Page
def registered():
    user_email = request.form.get("email")
    user_pass = request.form.get("password")

    exists = Student.query.filter_by(sEmail=user_email).first()
    if not exists:
        usr = Student(email=user_email, password=user_pass, fname='', lname='')
        db.session.add(usr)
        db.session.commit()
        # return render_template("error.html", message="Account already exists")
    else:
        flash("Email already exists!")
        return redirect(url_for("login"))

    # db.execute("INSERT INTO student(sEmail, sPassword) VALUES(?,?)",
    #            user_email, user_pass)

    # Send confirmaton email
    message = Message(
        "You have been successfully registered! This is a confirmation email.", recipients=[user_email])
    mail.send(message)

    return render_template("login.html")  # Maybe redirect to mainpage


@ app.route('/validate', methods=["POST"])
def validate():
    user_email = request.form.get("email")
    user_pass = request.form.get("password")

    global user
    global userID
    global COURSES

    user = Student.query.filter_by(sEmail=user_email).first()
    userID = user.sID
    if not user:
        flash("No user account for email")
        return redirect(url_for("signup"))

    if user.sPassword != user_pass:
        flash("Incorrect password!")
        return redirect(url_for("login"))

    # Add user session if checkbox true
    if request.method == "POST" and request.form.get("checkbox"):
        session.permanent = True
        session["email"] = request.form.get("email")

    # return render_template('dashboard.html', courses=COURSES)
    COURSES = Course.query.filter_by(cStudentID=userID).all()
    return render_template("mainpage.html", courses=COURSES)


@ app.route('/dashboard', methods=["POST"])
def dashboard():
    course = ''
    status = ''

    # INSERT into mySQL database
    if (request.form['save'] == ("saveCourse")):
        course = request.form['save']
        course = request.form['status']

        db.execute("INSERT INTO CourseList(cID, sID, clType) VALUES(?,?,?)", int(
            course), sID, status)

        message = "Record has been created!"
        messageType = "success"
        courses = db.execute(
            "SELECT * FROM INTO CourseList(cID, sID, clType) VALUES(?,?,?)")
        return render_template('dashboard.html', courses=courses)


# this route is for inserting data to mysql database via html forms
@ app.route('/insert', methods=['POST'])
def insert():
    global COURSES

    code = request.form['code']
    name = request.form['name']
    credits = request.form['credits']

    newCourse = Course(user.sID, code, name, credits)
    db.session.add(newCourse)
    db.session.commit()

    COURSES = Course.query.filter_by(cStudentID=user.sID).all()

    flash("Course Inserted Successfully")

    return render_template("mainpage.html", courses=COURSES)


# this is our update route where we are going to update our employee
@ app.route('/update/<int:id>', methods=['POST'])
def update(id):
    global COURSES
    # my_data = Data.query.get(request.form.get('id'))
    updateCourse = Course.query.filter_by(
        cStudentID=user.sID, cID=id).first()


    if request.form.get('textbook'): updateCourse.cTextbook = request.form.get('textbook')
    if request.form.get('difficulty'): updateCourse.cDifficulty = request.form.get('difficulty')
    if request.form.get('skill'): updateCourse.cSkill = request.form.get('skill')
    if request.form.get('quality'): updateCourse.cQuality = request.form.get('quality')
    if request.form.get('grade'): updateCourse.cGrade = request.form.get('grade')
    if request.form.get('status'): updateCourse.cStatus = request.form.get('status')
    if request.form.get('online'): updateCourse.cOnline = request.form.get('online')
    db.session.commit()

    # db.session.query(Course)\
    #     .filter(Course.cStudentID == user.sID, Course.cID == request.form.get('id'))\
    #     .update({
    #         Course.cTextbook: request.form['textbook'],
    #         Course.cDifficulty: request.form['difficulty'],
    #         Course.cSkill: request.form['difficulty'],
    #         Course.cQuality: request.form['quality'],
    #         Course.cGrade: request.form['grade']
    #     })
    # db.session.commit()

    # db.session.commit()
    flash("Course Updated Successfully")

    COURSES = Course.query.filter_by(cStudentID=user.sID).all()

    return render_template("mainpage.html", courses=COURSES)


# This route is for deleting our employee
@ app.route('/delete/<id>/', methods=['GET', 'POST'])
def delete(id):
    global COURSES
    # my_data = Data.query.get(id)
    # db.session.delete(my_data)
    # db.session.commit()
    Course.query.filter_by(
        cStudentID=user.sID, cID=id).delete()
    db.session.commit()

    flash("Course Deleted Successfully")

    COURSES = Course.query.filter_by(cStudentID=user.sID).all()
    return render_template("mainpage.html", courses=COURSES)

@app.route('/viewmajors', methods=['GET', 'POST'])
def viewmajors():
    global userID
    majors = Major.query.all()
    user = db.session.query(Student)\
        .filter(Student.sID == userID).first()

    print("user:" + str(user.sID) + "\tuser.sMajorID: " + str(user.sMajorID))
    

    curMajor = db.session.query(Major)\
        .filter(Major.mID == user.sMajorID).first()
    
    return render_template("viewmajors.html", majors=majors, curMajor=curMajor)

# updates the major in the DB and displays a message reflecting that to that user
@ app.route('/updatemajor/<int:majorID>', methods=['GET', 'POST'])
def selectmajor(majorID):
    global userID
    global COURSES
    majors = Major.query.all()
    user = db.session.query(Student)\
        .filter(Student.sID == userID).first()
    if user == None:
        return render_template("/validate.html")

    # print("before updating: " + str(user.sMajorID))

    user.sMajorID = majorID
    db.session.commit()


    # print("after updating: " + str(user.sMajorID))
    majorName = db.session.query(Major)\
        .filter(Major.mID == user.sMajorID).first() # querying for row that matches the user's majorID
    COURSES = Course.query.filter_by(cStudentID=user.sID).all()
    print(majorName)
    flash("Major Successfully Updated")
    return render_template('mainpage.html', courses=COURSES)

@ app.route('/mainpage')
def mainpage():
    courses = Course.query.filter_by(cStudentID=user.sID).all()
    return render_template('mainpage.html', courses=courses)

def createMajors():
    
    # undecided = Major(mName='Undecided')
    # db.session.add(undecided)
    # db.session.commit()
    # comSci = Major(mName='Computer Science')
    # db.session.add(comSci)
    # db.session.commit()
    # cyberSec = Major(mName='Cyber Security')
    # db.session.add(cyberSec)
    # db.session.commit()
    # infoTech = Major(mName='Information Technology') 
    # db.session.add(infoTech)
    # db.session.commit()
    majors = Major.query.all()
    for major in majors:
        print(major) 

if __name__ == "__main__":
    db.create_all()
    
    db.session.commit()
    # createMajors()
    # db.session.query(Major).delete()
    # db.session.query(Student).delete()

    # with open("IT 326 course list.csv", "r") as f:
    #     reader = csv.reader(f, delimiter=",")
    #     for line in reader:
    #         dept, code, name, credits, desc = line[0], line[1], line[2], line[3], line[5]
    #         newCourse = CourseBank(dept, code, name, credits, desc)
    #         db.session.add(newCourse)
    # db.session.commit()

    app.run(debug=True)
