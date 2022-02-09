from flask import Flask, redirect, render_template, request, jsonify, url_for
from cs50 import SQL
from flask_mail import Mail, Message
import os


# Application Configurations
app = Flask(__name__)
app.config["MAIL_DEFAULT_SENDER"] = "classplannerit326@gmail.com"
app.config['MAIL_USERNAME'] = "classplannerit326@gmail.com"
app.config['MAIL_PASSWORD'] = "Planner123!"
app.config['MAIL_PORT'] = 587
app.config['MAIL_SERVER'] = "smtp.gmail.com"
app.config['MAIL_USE_TLS'] = True

# Intitializations
db = SQL('sqlite:///planner.db')
mail = Mail(app)
sID = None
message = ''
messageType = ''


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/login')  # Login page
def login():
    return render_template("login.html")


@app.route('/signup')  # Signup page
def signup():
    return render_template("signup.html")


@app.route('/registered', methods=["POST"])  # Registered Page
def registered():
    user_email = request.form.get("email")
    user_pass = request.form.get("password")

    row=db.execute("SELECT sID FROM student WHERE sEmail = ?", user_email)
    if len(row) == 1: return render_template("error.html", message="Account already exists")

    db.execute("INSERT INTO student(sEmail, sPassword) VALUES(?,?)", user_email, user_pass)

    # Send confirmaton email
    message = Message("You have been successfully registered! This is a confirmation email.", recipients=[user_email])
    mail.send(message)

    return render_template("login.html")  # Maybe redirect to mainpage


@app.route('/validate', methods=["POST"])
def validate():
    user_email = request.form.get("email")
    user_pass = request.form.get("password")

    row=db.execute("SELECT sID FROM student WHERE sEmail = ? AND sPassword = ?", user_email, user_pass)
    if len(row)==0: return render_template("error.html", message="Incorrect password or user")

    COURSES = [("hello","this","is","tuple")]
    return render_template('dashboard.html', courses=COURSES)


@app.route('/dashboard', methods=["POST"])
def dashboard():
    course = ''
    status = ''

    # INSERT into mySQL database
    if (request.form['save'] == ("saveCourse")):
        course = request.form['save']
        course = request.form['status']

        db.execute("INSERT INTO CourseList(cID, sID, clType) VALUES(?,?,?)", int(course), sID, status)

        message = "Record has been created!"
        messageType = "success"
        courses = db.execute("SELECT * FROM INTO CourseList(cID, sID, clType) VALUES(?,?,?)")
        return render_template('dashboard.html', courses=courses)


if __name__ == "__main__":
    app.run(debug=True)
