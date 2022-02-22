from flask import Flask, redirect, render_template, request, jsonify, url_for, session, flash
from flask_session import Session
from cs50 import SQL
from flask_mail import Mail, Message
import os



# Application Configurations
app = Flask(__name__)
app.config["SESSION_PERMANENT"]=False
app.config["SESSION_TYPE"]="filesystem"
Session(app)

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


class Data:
    def __init__(self, id, name, email, phone):
        self.id = id
        self.name = name
        self.email = email
        self.phone = phone


x=Data(1,"IT327", "email@", "3095555555")
COURSES = [x]

@app.route('/')
def index():
    if not session.get("email"): #Check if session doesn't exist
        return render_template("index.html")

    # return render_template('dashboard.html', courses=COURSES)
    return render_template("mainpage.html", employees=COURSES)


@app.route('/login')  # Login page
def login():
    return render_template("login.html")


@app.route('/logout')  # Login page
def logout():
    session["email"]=None #remove session
    return redirect("/")


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
    sID = row[0]["sID"]

    # Add user session if checkbox true
    if request.method == "POST" and request.form.get("checkbox"):
        session["email"] = request.form.get("email")
        return redirect("/")

    # return render_template('dashboard.html', courses=COURSES)
    return render_template("mainpage.html", employees=COURSES)


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


# this route is for inserting data to mysql database via html forms
@app.route('/insert', methods=['POST'])
def insert():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        my_data = Data(sID, name, email, phone)
        COURSES.append(my_data)

        flash("Course Inserted Successfully")

        return render_template("mainpage.html", employees=COURSES)


# this is our update route where we are going to update our employee
@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        # my_data = Data.query.get(request.form.get('id'))
        for c in COURSES:
            if c.id==int(request.form.get('id')):
                c.name = request.form['name']
                c.email = request.form['email']
                c.phone = request.form['phone']
                break

        # db.session.commit()
        flash("Course Updated Successfully")

        return render_template("mainpage.html", employees=COURSES)


# This route is for deleting our employee
@app.route('/delete/<id>/', methods=['GET', 'POST'])
def delete(id):
    # my_data = Data.query.get(id)
    # db.session.delete(my_data)
    # db.session.commit()
    for c in COURSES:
        if c.id == int(id):
            COURSES.remove(c)
            break

    flash("Course Deleted Successfully")

    return render_template("mainpage.html", employees=COURSES)




if __name__ == "__main__":
    app.run(debug=True)
