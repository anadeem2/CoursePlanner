import csv
import os
from datetime import timedelta
from flask import Flask, redirect, render_template, request, jsonify, url_for, session, flash
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from flask_mail import Mail, Message

# =========================================
#       Application Configurations
# =========================================

app = Flask(__name__)
app.config["SESSION_TYPE"] = "filesystem"

# Session Config
Session(app)

# Mail Config
app.config["MAIL_DEFAULT_SENDER"] = "classplannerit326@gmail.com"
app.config['MAIL_USERNAME'] = "classplannerit326@gmail.com"
app.config['MAIL_PASSWORD'] = "Planner123!"
app.config['MAIL_PORT'] = 587
app.config['MAIL_SERVER'] = "smtp.gmail.com"
app.config['MAIL_USE_TLS'] = True

# Database Config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///finaltest.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Intitializations
mail = Mail(app)
db = SQLAlchemy(app)


# =========================================
#               ORM Modeling
# =========================================

# Student model/class representing the user of application
class Student(db.Model):
    __tablename__ = 'Student'
    # Student ID primary key used to differentiate & track students
    sID = db.Column(db.Integer, primary_key=True)
    sEmail = db.Column(db.String(200), nullable=False)
    sFName = db.Column(db.String(200), nullable=True)
    sLName = db.Column(db.String(200), nullable=True)
    sPassword = db.Column(db.String(200), nullable=False)
    # Foriegn key used to refer to Major table
    sMajorID = db.Column(db.Integer, nullable=False)
    # cascade on delete contstrait (remove all user ratings when account deleted)
    course = db.relationship("Course", cascade="all, delete")

    # Constructor
    def __init__(self, email, password, fname, lname, majorID=0):
        self.sEmail = email
        self.sPassword = password
        self.sFName = fname
        self.sLName = lname
        self.sMajorID = majorID

    # equivanlent ToString
    def __repr__(self):
        return self.sID

# Course model/class representing instances of courses students are planning


class Course(db.Model):
    __tablename__ = 'Course'
    # Course ID primary key used to differentiate courses & students who take them
    cID = db.Column(db.Integer, primary_key=True)
    # Represents the corresponding course code (ex 326)
    cCode = db.Column(db.String(10), nullable=False)
    # Represents the corresponding department (ex IT)
    cDept = db.Column(db.String(10), nullable=False)
    # The name of the course (ex Principles of Software Engineering)
    cName = db.Column(db.String(200), nullable=False)
    # Grade 5 = A 1 = F - Float so it can be aggregated to produce average
    cGrade = db.Column(db.Float, nullable=True)
    # 1 = Yes Textbook is used 0 = Textbook was not used - Float so it can be aggregated to produce average
    cTextbook = db.Column(db.Float, nullable=True)
    # 1 = Course was offered online 0 = Course was in person - Float so it can be aggregated to produce average
    cOnline = db.Column(db.Float, nullable=True)
    # number of credits granted upon completing correponding course (ex 3)
    cCredits = db.Column(db.Integer, nullable=False)
    # 1-5 scale 5 = most difficult - Float so it can be aggregated to produce average
    cDifficulty = db.Column(db.Float, nullable=True)
    # Skills suggested as preperation for course and or used in course
    cSkill = db.Column(db.String(200), nullable=True)
    # Rating on the subjective preference/quality of course - 1-5 scale 5 = best quality
    cQuality = db.Column(db.Float, nullable=True)
    # Status indicating whether the course is IP - In progress/currently taking, T - taken/completed, P - planned for upcoming/future semesters
    cStatus = db.Column(db.String(4), nullable=True)
    # Student foreign key - students can take many courses. Cascade on delete - if student deletes account, no point in their ratings sticking around (we don't want outdated rating only current/active users matter)
    cStudentID = db.Column("cStudentID", ForeignKey(
        'Student.sID', ondelete='CASCADE'), nullable=False)

    # Constructor
    def __init__(self, studentID, dept, code, name, credits, status='In Progress'):
        self.cStudentID = studentID
        self.cCode = code
        self.cDept = dept
        self.cName = name
        self.cCredits = credits
        self.cStatus = status

    # To String
    def __repr__(self):
        return self.cDept+" "+self.cCode + " - " + self.cName

# CourseBank class/model representing course offerings available (used for instantiating student planning courses)


class CourseBank(db.Model):
    # CourseBank ID primary key used to differentiate different offerings/storings
    cID = db.Column(db.Integer, primary_key=True)
    cDept = db.Column(db.String(200), nullable=False)
    cCode = db.Column(db.String(20), nullable=False)
    cName = db.Column(db.String(200), nullable=False)
    cCredits = db.Column(db.String(20), nullable=False)
    cDesc = db.Column(db.String(200), nullable=False)

    # Constructor
    def __init__(self, dept, code, name, credits, desc):
        self.cDept = dept
        self.cCode = code
        self.cName = name
        self.cCredits = credits
        self.cDesc = desc
    # ToString

    def __repr__(self):
        return self.cDept+" "+self.cCode

# Major class/model representing different major offerings students can choose from


class Major(db.Model):
    __tablename__ = 'Major'
    # Major ID primary key used to differentiate different majors
    mID = db.Column(db.Integer, primary_key=True)
    mName = db.Column(db.String(50), nullable=False)
    mDept = db.Column(db.String(200), nullable=False)

    # constructor
    def __init__(self, mName, mDept):
        self.mName = mName
        self.mDept = mDept

    # toString
    def __repr__(self):
        return self.mName

# =========================================
#             Controllers
# =========================================

# Index route - checks to see if user has a session stored - if true then render the corresponding dashboard/mainpage, otherwise redirect to landing page where they can choose to login or signup
# Student handler


@ app.route('/')
def index():
    if "user" not in session:  # Session does not exist
        return render_template("index.html")  # Login view

    return redirect(url_for("mainpage"))  # Student view


# Render Login page - page where user is prompted for login credentials
# Student handler

@ app.route('/login')
def login():
    return render_template("login.html")  # login view

# Logout user (forget user context) and remove session
# Student handler


@ app.route('/logout')
def logout():
    session.pop("user", None)
    return render_template("login.html")  # Login view

# Send forgotten password to respective user email address if form submitted otherwise render form
# Student handler + Contact handler


@ app.route('/forgot', methods=["GET", "POST"])
def forgot():
    # Only check for input if form is posted
    if request.method == 'POST':
        # grab inputs and check if an account exists under the email
        user_email = request.form.get("email")
        exists = Student.query.filter_by(sEmail=user_email).first()
        if exists:  # send an email with forgotten password
            message = Message(
                "Your forgotten password: " + exists.sPassword, recipients=[user_email])
            mail.send(message)
            flash("Email with password sucessfully sent")
            return redirect(url_for("login"))  # login view
        else:
            flash("Invalid email, please sign up")
            return redirect(url_for("signup"))  # login view
    else:  # render forgot form
        return render_template("forgot.html")  # login view

# Sign up page where users can create an account
# Student handler


@ app.route('/signup')
def signup():
    return render_template("signup.html")  # login view

# Removes user acc from database

# User can choose to delete their account & all of their courses + ratings
# Student handler + Contact Handler


@app.route('/deleteUser/')
def deleteUser():
    # send email confirmation to user email
    message = Message("Your account has been successfully deleted.", recipients=[
                      session['user'].sEmail])
    mail.send(message)

    # delete from database
    db.session.delete(session['user'])
    db.session.commit()

    # notify active user
    flash("Account removed.")
    return redirect(url_for("logout"))  # Login view

# Render contact us form and allow user to share feedback
# Student handler


@ app.route('/contactUs', methods=['POST'])
def contactUs():
    return render_template("contactUs.html")  # Student view

# Submit user feedback and forward to developer
# contact handler


@ app.route('/contacted', methods=["POST"])
def contacted():
    # Grab & store inputs
    email_subject = request.form.get("subject")
    email_message = request.form.get("message")
    admin_email = "developerit326@gmail.com"

    # Validate inputs
    if not email_subject or not email_message:
        flash("Missing fields")
        return render_template("contactUs.html")

    # Create and send message to devs
    message = Message("""\
        Subject:  {subject}""".format(subject=email_subject), recipients=[admin_email])
    message.body = " Message: {message}".format(message=email_message)

    # Send confirmaton email
    mail.send(message)

    # Notify active user
    flash("Feedback sent!")
    return redirect(url_for("mainpage"))  # student view

# Creates/register user account and saves to DB
# student handler + contact handler


@ app.route('/registered', methods=["POST"])
def registered():
    # Grab initialization fields
    user_email = request.form.get("email")
    user_pass = request.form.get("password")
    user_fname = request.form.get("fname")
    user_lname = request.form.get("lname")

    # Validate input
    if not (user_email and user_pass and user_fname and user_lname):
        flash("Invalid credentials")
        return redirect(url_for("signup"))  # login view

    # Verify email/user does not already exist
    exists = Student.query.filter_by(sEmail=user_email).first()
    if not exists:  # Create account if does not exist
        # Create student object
        usr = Student(email=user_email, password=user_pass,
                      fname=user_fname, lname=user_lname)
        # Commit, save, and store in database
        db.session.add(usr)
        db.session.commit()
    else:
        # Notify active user
        flash("Email already exists!")
        return redirect(url_for("login"))  # login view

    # Send confirmaton email
    message = Message(
        "You have been successfully registered! This is a confirmation email.", recipients=[user_email])
    mail.send(message)

    return render_template("login.html")  # login view

# Validates user login credentials
# student handler


@ app.route('/validate', methods=["POST"])
def validate():
    # Grab fields
    user_email = request.form.get("email")
    user_pass = request.form.get("password")

    # Validate input
    if not user_email or not user_pass:
        flash("Invalid credentials")
        return redirect(url_for("signup"))  # login view

    user = Student.query.filter_by(sEmail=user_email).first()
    if not user:  # Verify query was successful
        flash("No user account for email")
        return redirect(url_for("signup"))  # login view
    # Verify password
    if user.sPassword != user_pass:
        flash("Incorrect password!")
        return redirect(url_for("login"))

    # Save user session 7-days if remember-me true, else 60min
    if request.form.get("checkbox"):
        app.permanent_session_lifetime = timedelta(days=7)
        session.permanent = True
    else:
        app.permanent_session_lifetime = timedelta(minutes=60)
        session.permanent = False

    # Create user session
    session['user'] = user

    return redirect(url_for("mainpage"))  # student view


# Updates user account information
# student handler + contact handler

@ app.route('/editUser', methods=['POST'])
def editUser():
    # Required to requery and grab db cursor to student object again
    updateUser = Student.query.filter_by(sID=session['user'].sID).first()

    # only update provided fields (if evalues to false if null)
    if request.form.get('fname'):
        updateUser.sFName = request.form.get('fname')
    if request.form.get('lname'):
        updateUser.sLName = request.form.get('lname')

    # Save & store to database
    db.session.commit()

    # Send confirmation email
    message = Message("Your account has information has been successfully updated.", recipients=[
                      session['user'].sEmail])
    mail.send(message)

    # Notify user
    flash("User information updated.")
    return redirect(url_for("mainpage"))  # student view

# Update selected course ratings
# Course handler


@ app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):

    # Grab db cursor to course object
    updateCourse = Course.query.filter_by(
        cStudentID=session['user'].sID, cID=id).first()

    # only update provided fields (if evalues to false if null)
    if request.form.get('textbook'):  # ProcessTextbookUsed
        updateCourse.cTextbook = request.form.get('textbook')
    if request.form.get('difficulty'):  # ProcessDifficulty
        updateCourse.cDifficulty = request.form.get('difficulty')
    if request.form.get('skill'):  # ProcessSkill
        updateCourse.cSkill = request.form.get('skill')
    if request.form.get('quality'):  # ProcessQuality
        updateCourse.cQuality = request.form.get('quality')
    if request.form.get('grade'):  # ProcessGrade
        updateCourse.cGrade = request.form.get('grade')
    if request.form.get('status'):  # ProcessStatus
        updateCourse.cStatus = request.form.get('status')
    if request.form.get('online'):  # ProcessOnlineAvail
        updateCourse.cOnline = request.form.get('online')

    # Save & store to database
    db.session.commit()

    # Notify user
    flash("Course Updated Successfully")
    return redirect(url_for("mainpage"))  # student view

# Removes selected course from user dashboard
# Course handler


@ app.route('/delete/<id>/', methods=['GET'])
def delete(id):
    # Grab db cursor to course object
    Course.query.filter_by(
        cStudentID=session['user'].sID, cID=id).delete()

    # Save & store to database
    db.session.commit()

    # Notify user
    flash("Course Deleted Successfully")
    return redirect(url_for("mainpage"))  # student view

# Display available major selections to user
# major handler


@app.route('/viewmajors', methods=['POST'])
def viewmajors():
    # Query all major offering from DB
    majors = Major.query.all()

    # Preselect and show user their currently selected major
    curMajor = db.session.query(Major)\
        .filter(Major.mID == session['user'].sMajorID).first()

    # If null, the major is undecided & let user know
    if not curMajor:
        curMajor = "Undecided"

    # major view
    return render_template("viewmajors.html", majors=majors, curMajor=curMajor)

# Allow user to select his/her desired and or update
# major handler


@ app.route('/updatemajor/<int:majorID>', methods=['POST'])
def selectmajor(majorID):
    # Required to requery and grab db cursor to student object again
    updateUser = Student.query.filter_by(sID=session['user'].sID).first()
    # Make update
    updateUser.sMajorID = majorID
    # Save & store to database
    db.session.commit()
    # Notify active user
    flash("Major Successfully Updated")
    return redirect(url_for("mainpage"))  # student view

# Display course offerings to student based on their major selection
# Course handler


@app.route('/viewcourses', methods=['POST'])
def viewcourses():
    # Only show offerings if major is selected (offerings shown based on major)
    if session['user'].sMajorID == 0:
        flash("Must select major")
        return redirect(url_for("mainpage"))  # student view

    # Grab user department
    curMajor = Major.query.filter_by(
        mID=session['user'].sMajorID).first()  # Get user dept

    # Filter offerings by department
    coursebank = CourseBank.query.filter_by(
        cDept=curMajor.mDept).all()  # query by dept

    # Course view
    return render_template("viewcourses.html", coursebank=coursebank, db=db.session)

# Adds selected course to user's dashboard/plan
# Course handler


@app.route('/insertcourse/<id>', methods=['POST'])
def insertcourse(id):
    # Grab course data from course bank table
    course = CourseBank.query.filter_by(cID=id).first()
    # Initialize, create, and assign course object to student
    newCourse = Course(session['user'].sID, course.cDept,
                       course.cCode, course.cName, course.cCredits)
    # Add, save, and store to db
    db.session.add(newCourse)
    db.session.commit()

    # notfiy user
    flash("Course Inserted Successfully")
    return redirect(url_for("mainpage"))  # student view

# Renders users dashboard/plan page
# Student handler


@ app.route('/mainpage', methods=['POST', 'GET'])
def mainpage():
    # Refresh user & display list of courses student is taking
    session['user'] = Student.query.filter_by(sID=session['user'].sID).first()
    # Unnecessary check (only happens when we drop database & user had stored session - unapplicable in production)
    # if not (session['user']):
    #     return redirect(url_for("logout"))
    COURSES = Course.query.filter_by(
        cStudentID=session['user'].sID).order_by("cStatus").all()

    # student view
    return render_template('mainpage.html', courses=COURSES, name=session['user'].sFName)


# =========================================
#          Data initializations
# =========================================
# These methods are only needed to be ran once - static data

# Create and insert the currently offered courses
def createMajors():
    # Drop majors
    db.session.query(Major).delete()

    # create majors
    comSci = Major(mName='Computer Science', mDept="IT")
    db.session.add(comSci)

    cyberSec = Major(mName='Cyber Security', mDept="IT")
    db.session.add(cyberSec)

    infoTech = Major(mName='Information Technology', mDept="IT")
    db.session.add(infoTech)
    db.session.commit()

    # Test to ensure data inserted
    # majors = Major.query.all()
    # for maj in majors:
    #     print(maj.mID, maj.mName, maj.mDept)


# Create and insert course offerings (imported from CSV) and store them into coursebank table
def createCourseBank():
    # Drop table in case (don't want duplicates)
    db.session.query(CourseBank).delete()
    # import course offerings from CSV and store into DB
    with open("IT 326 course list.csv", "r") as f:
        reader = csv.reader(f, delimiter=",")
        for line in reader:
            dept, code, name, credits, desc = line[0], line[1], line[2].replace(
                '"', ''), line[3], line[5].replace('"', '')
            # Create courebank db records/objects
            newCourse = CourseBank(dept, code, name, credits, desc)
            # Add to cursor
            db.session.add(newCourse)
    # Save and store
    db.session.commit()

    # Helper to test if courses inserted properly
    # courses = CourseBank.query.all()
    # for c in courses[1:]:
    #     print(c.cDept,
    #           c.cCode,
    #           c.cName,
    #           c.cCredits)


if __name__ == "__main__":
    # Should only need to call these methods once
    db.create_all()

    # Only call first time running app, comment otherwise
    # createCourseBank()
    # createMajors()

    # can choose to turn of debug for faster performance
    app.run(debug=True)
