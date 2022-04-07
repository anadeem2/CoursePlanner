import csv
import os

from datetime import timedelta
from flask import Flask, redirect, render_template, request, jsonify, url_for, session, flash
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from flask_mail import Mail, Message


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
mail = Mail(app)
user = None
COURSES = None
message = ''


class Student(db.Model):
    __tablename__ = 'Student'
    sID = db.Column(db.Integer, primary_key=True)
    sEmail = db.Column(db.String(200), nullable=False)
    sFName = db.Column(db.String(200), nullable=True)
    sLName = db.Column(db.String(200), nullable=True)
    sPassword = db.Column(db.String(200), nullable=False)
    sMajorID = db.Column(db.Integer, nullable=False)
    course = db.relationship("Course", cascade="all, delete")
    # sMajorID =  db.Column("sMajorID", ForeignKey('Major.mID'), nullable=False)

    def __init__(self, email, password, fname, lname, majorID=0):
        self.sEmail = email
        self.sPassword = password
        self.sFName = fname
        self.sLName = lname
        self.sMajorID = majorID

    def __repr__(self):
        return self.sID

    def setMajorID(self, id: int):
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
    #IP/Taken/Planned
    cStatus = db.Column(db.String(4), nullable=True)
    cStudentID = db.Column("cStudentID", ForeignKey('Student.sID', ondelete='CASCADE'), nullable=False) #FK

    def __init__(self, studentID, code, name, credits):
        self.cStudentID = studentID
        self.cCode = code
        self.cName = name
        self.cCredits = credits

    def __repr__(self):
        return self.cCode + " - " + self.cName

# class MajorRequirement(db.Model):
#     __tablename__ = 'MajorRequirement'
#     # rID = db.Column(db.Integer, primary_key=True)
#     majorID = db.Column("reqMajorID", ForeignKey(
#         'Major.mID'), primary_key=True, nullable=False)
#     # courseID = db.Column("reqCourseID", ForeignKey(
#     #     'Course.cID'), nullable=False)
#     majorCourseReq = db.relationship("Course")

#     def __init__(self, majorID):
#         self.majorID = majorID
    
#     def __repr__():
#         # print(str(majorID) + "req: " + str(courseID))
#         print(majorID)
    

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

    def __repr__(self):
        return self.Dept+" "+self.cCode


class Major(db.Model):
    __tablename__ = 'Major'
    mID = db.Column(db.Integer, primary_key = True)
    mName = db.Column(db.String(50), nullable=False) # Computer Science
    mDept = db.Column(db.String(200), nullable=False)  # IT

    def __int__(self, majorName, dept):
        self.mName=majorName
        self.mDept=dept

    def __repr__(self):
        return self.mName



@ app.route('/')
def index():
    global user
    global COURSES

    if "user" not in session:  # Check if session doesn't exist
        return render_template("index.html")

    user = session['user']
    COURSES = Course.query.filter_by(cStudentID=session['user'].sID).order_by("cStatus").all()
    return render_template("mainpage.html", courses=COURSES)


@ app.route('/login')  # Login page
def login():
    return render_template("login.html")


@ app.route('/logout')  # Logout
def logout():
    global user
    global COURSES

    session.pop("user", None)
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


@app.route('/deleteUser/')
def deleteUser():
    global user

    message = Message("Your account has been successfully deleted.", recipients=[user.sEmail])
    mail.send(message)

    db.session.delete(user)
    db.session.commit()

    flash("Account removed.")
    return redirect(url_for("logout"))


@ app.route('/contactUs')  # Contact Us page
def contactUs():
    return render_template("contactUs.html")


@ app.route('/contacted', methods=["POST"])  # Contacted Page
def contacted():
    email_subject = request.form.get("subject")
    email_message = request.form.get("message")
    admin_email = "developerit326@gmail.com"

    message = Message ("""\
        Subject:  {subject}""".format(subject=email_subject), recipients=[admin_email])
    message.body = " Message: {message}".format(message=email_message)

    # Send confirmaton email
    mail.send(message)
    flash("Feedback sent!")
    return render_template("mainpage.html")  # Maybe redirect to mainpage


@ app.route('/registered', methods=["POST"])  # Registered Page
def registered():
    user_email = request.form.get("email")
    user_pass = request.form.get("password")
    user_fname = request.form.get("fname")
    user_lname = request.form.get("lname")

    if not (user_email and user_pass and user_fname and user_lname):
        flash("Invalid credentials")
        return redirect(url_for("signup"))

    exists = Student.query.filter_by(sEmail=user_email).first()
    if not exists:
        usr = Student(email=user_email, password=user_pass, fname=user_fname, lname=user_lname)
        db.session.add(usr)
        db.session.commit()
    else:
        flash("Email already exists!")
        return redirect(url_for("login"))

    # Send confirmaton email
    message = Message(
        "You have been successfully registered! This is a confirmation email.", recipients=[user_email])
    mail.send(message)

    return render_template("login.html")  # Maybe redirect to mainpage


@ app.route('/validate', methods=["POST"])
def validate():
    global user
    global COURSES

    user_email = request.form.get("email")
    user_pass = request.form.get("password")

    if not user_email or not user_pass:
        flash("Invalid credentials")
        return redirect(url_for("signup"))

    user = Student.query.filter_by(sEmail=user_email).first()
    if not user:
        flash("No user account for email")
        return redirect(url_for("signup"))

    if user.sPassword != user_pass:
        flash("Incorrect password!")
        return redirect(url_for("login"))

    # Add user session if checkbox true
    if request.method == "POST" and request.form.get("checkbox"):
        session.permanent = True
        session["user"] = user


    COURSES = Course.query.filter_by(cStudentID=user.sID).order_by("cStatus").all()
    return render_template("mainpage.html", courses=COURSES)


# this route is for inserting data to mysql database via html forms
@ app.route('/insert', methods=['POST'])
def insert():
    global user
    global COURSES

    code = request.form['code']
    name = request.form['name']
    credits = request.form['credits']

    newCourse = Course(user.sID, code, name, credits)
    db.session.add(newCourse)
    db.session.commit()

    flash("Course Inserted Successfully")
    COURSES = Course.query.filter_by(cStudentID=user.sID).order_by("cStatus").all()
    return render_template("mainpage.html", courses=COURSES)


# this is our update route where we are going to update course
@ app.route('/update/<int:id>', methods=['POST'])
def update(id):
    global user
    global COURSES

    updateCourse = Course.query.filter_by(
        cStudentID=user.sID, cID=id).first()

    if request.form.get('textbook'):
        updateCourse.cTextbook = request.form.get('textbook')
    if request.form.get('difficulty'):
        updateCourse.cDifficulty = request.form.get('difficulty')
    if request.form.get('skill'):
        updateCourse.cSkill = request.form.get('skill')
    if request.form.get('quality'):
        updateCourse.cQuality = request.form.get('quality')
    if request.form.get('grade'):
        updateCourse.cGrade = request.form.get('grade')
    if request.form.get('status'):
        updateCourse.cStatus = request.form.get('status')
    if request.form.get('online'):
        updateCourse.cOnline = request.form.get('online')
    db.session.commit()

    flash("Course Updated Successfully")
    COURSES = Course.query.filter_by(cStudentID=user.sID).order_by("cStatus").all()
    return render_template("mainpage.html", courses=COURSES)


# This route is for deleting course
@ app.route('/delete/<id>/', methods=['GET', 'POST'])
def delete(id):
    global user
    global COURSES

    Course.query.filter_by(
        cStudentID=user.sID, cID=id).delete()
    db.session.commit()

    flash("Course Deleted Successfully")
    COURSES = Course.query.filter_by(cStudentID=user.sID).order_by("cStatus").all()
    return render_template("mainpage.html", courses=COURSES)


@app.route('/viewmajors', methods=['GET', 'POST'])
def viewmajors():
    global user
    global COURSES

    majors = Major.query.all()

    curMajor = db.session.query(Major)\
        .filter(Major.mID == user.sMajorID).first()

    if not curMajor: curMajor="Undecided"

    return render_template("viewmajors.html", majors=majors, curMajor=curMajor)


# updates the major in the DB and displays a message reflecting that to that user
@ app.route('/updatemajor/<int:majorID>', methods=['GET', 'POST'])
def selectmajor(majorID):
    global user
    global COURSES

    updateUser = Student.query.filter_by(sID=user.sID).first()
    updateUser.sMajorID = majorID
    db.session.commit()

    flash("Major Successfully Updated")
    user = Student.query.filter_by(sID=user.sID).first()
    return render_template('mainpage.html', courses=COURSES)

@app.route('/viewcourses', methods=['GET', 'POST'])
def viewcourses():
    global user
    global COURSES

    coursebank = CourseBank.query.all()

    

    return render_template("viewcourses.html", coursebank=coursebank)

@ app.route('/mainpage')
def mainpage():
    global user
    global COURSES

    COURSES = Course.query.filter_by(cStudentID=user.sID).order_by("cStatus").all()
    return render_template('mainpage.html', courses=COURSES)


def createMajors():
    db.session.query(Major).delete()
    comSci = Major(mName='Computer Science', mDept="IT")
    db.session.add(comSci)

    cyberSec = Major(mName='Cyber Security', mDept="IT")
    db.session.add(cyberSec)

    infoTech = Major(mName='Information Technology', mDept="IT")
    db.session.add(infoTech)
    db.session.commit()

    majors = Major.query.all()
    for major in majors:
        print(major)         
    for maj in majors:
        print(maj.mID, maj.mName, maj.mDept)


def createCourseBank():
    db.session.query(CourseBank).delete()
    with open("IT 326 course list.csv", "r") as f:
        reader = csv.reader(f, delimiter=",")
        for line in reader:
            dept, code, name, credits, desc = line[0], line[1], line[2], line[3], line[5]
            newCourse = CourseBank(dept, code, name, credits, desc)
            db.session.add(newCourse)
    db.session.commit()

    courses = CourseBank.query.all()
    for c in courses[1:]:
        print(c.cDept,
              c.cCode,
              c.cName,
              c.cCredits)




if __name__ == "__main__":
    db.create_all()
    # createCourseBank()
    # createMajors()
    # courses = CourseBank.query.all()
    # for c in courses[1:]:
    #     print(c.cDept,
    #           c.cCode,
    #           c.cName,
    #           c.cCredits)
    app.run(debug=True)
