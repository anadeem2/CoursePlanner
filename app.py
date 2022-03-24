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
from dbObjects import Student, Course, Major, CourseBank


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


def getGlobalUser():
    return user

@ app.route('/')
def index():
    global COURSES

    if "email" not in session:  # Check if session doesn't exist
        return render_template("index.html")

    # return render_template('dashboard.html', courses=COURSES)
    print("test")
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
    global COURSES

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
        session["email"] = request.form.get("email")

    # return render_template('dashboard.html', courses=COURSES)
    COURSES = Course.query.filter_by(cStudentID=user.sID).all()
    return render_template("mainpage.html", courses=COURSES)

@app.route('/viewmajors', methods = ['GET','POST'])
def viewmajors():   
    global user
    majors = Major.query.all()

    curMajor = db.session.query(Major)\
        .filter(Major.mID == user.sMajorID).first()

    return render_template("viewmajors.html",majors=majors,curMajor=curMajor)

# updates the major in the DB and displays a message reflecting that to that user
@ app.route('/updatemajor/<int:id>', methods=['GET','POST'])
def selectmajor(id):
    global user
    majors = Major.query.all()

    if user == None:
        return render_template("/validate.html")

    updateMajor = Student.query.filter_by(sID=user.sID).first()
    updateMajor.sMajorID = id

    majorName = db.session.query(Major).filter(Major.mID == id).first()

    db.session.commit()
    flash("Major Successfully Updated")
    return render_template('viewmajors.html',majors=majors,curMajor=majorName)



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

if __name__ == "__main__":
    # db.session.query(Major).delete()
    # comSci = Major(mName='Computer Science', cDept="IT")
    # db.session.add(comSci)
    #
    # cyberSec = Major(mName='Cyber Security', cDept="IT")
    # db.session.add(cyberSec)
    #
    # infoTech = Major(mName='Information Technology', cDept="IT")
    # db.session.add(infoTech)

    # db.session.query(CourseBank).delete()
    # with open("IT 326 course list.csv", "r") as f:
    #     reader = csv.reader(f, delimiter=",")
    #     for line in reader:
    #         dept, code, name, credits, desc = line[0], line[1], line[2], line[3], line[5]
    #         newCourse = CourseBank(dept, code, name, credits, desc)
    #         db.session.add(newCourse)

    db.session.commit()
    db.create_all()

    # courses = CourseBank.query.all()
    # for c in courses[1:]:
    #     print(c.cDept,
    #           c.cCode,
    #           c.cName,
    #           c.cCredits)

    # majors = Major.query.all()
    # for maj in majors:
    #     print(maj.mID, maj.mName)

    app.run(debug=True)
