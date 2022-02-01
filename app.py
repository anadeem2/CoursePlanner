from email import message
from flask import Flask, redirect, render_template, request, jsonify, url_for
# from cs50 import SQL
from flask_mail import Mail, Message
import pyodbc
import os
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy.orm import relationship

# Application Configurations
app = Flask(__name__)
app.config["MAIL_DEFAULT_SENDER"] = "classplannerit326@gmail.com"
app.config['MAIL_USERNAME'] = "classplannerit326@gmail.com"
app.config['MAIL_PASSWORD'] = "Planner123!"
app.config['MAIL_PORT'] = 587
app.config['MAIL_SERVER'] = "smtp.gmail.com"
app.config['MAIL_USE_TLS'] = True

# Intitializations
db = None
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
    try:
        db.execute("SELECT sID FROM student WHERE sEmail = ?", user_email)
    except pyodbc.Error as e:
        return render_template("error.html", message="Account already exists")

    db.execute("INSERT INTO student(sEmail, sPassword) VALUES(?,?)",
               user_email, user_pass)
    db.commit()

    # Send confirmaton email
    message = Message(
        "You have been successfully registered! This is a confirmation email.", recipients=[user_email])
    mail.send(message)

    return render_template("login.html")  # Maybe redirect to mainpage


@app.route('/validate', methods=["POST"])
def validate():
    user_email = request.form.get("email")
    user_pass = request.form.get("password")

    try:
        db.execute("SELECT sID FROM student WHERE sEmail = ?", user_email)
        try:
            db.execute(
                "SELECT sID FROM student WHERE sEmail = ? AND sPassword = ?", user_email, user_pass)
            for row in db.fetchall():
                sID = row[0]
        except pyodbc.Error as e:
            return render_template("error.html", message="Incorrect password")
    except pyodbc.Error as e:
        return render_template("error.html", message="Account does not exist")
    print(sID)
    # courses = db.execute("{CALL StudentCourses}", (sID,))
    courses = db.execute("{CALL StudentCourses}")
    # for course in courses.fetchall():
    #     print(course)
    return render_template('dashboard.html', courses=courses)


@app.route('/dashboard', methods=["POST"])
def dashboard():
    course = ''
    status = ''

    # INSERT into mySQL database
    if (request.form['save'] == ("saveCourse")):
        course = request.form['save']
        course = request.form['status']

        db.execute(
            "INSERT INTO CourseList(cID, sID, clType) VALUES(?,?,?)", int(course), sID, status)

        db.commit()

        message = "Record has been created!"
        messageType = "success"
        courses = db.execute("{CALL StudentCourses}")
        return render_template('dashboard.html', courses=courses)

    # // DELETE from mySQL database
    # if (isset($_GET['delete'])) {
    #     $id = $_GET['delete'];
    #     $mysqli->query("DELETE FROM data WHERE id=$id") or die ($mysqli->error());

    #     $_SESSION['message'] = "Record has been Deleted!";
    #     $_SESSION['msg_type'] = "danger";

    #     header("Location: index.php");
    # }

    # //EDIT
    # if (isset($_GET['edit'])) {
    #     $id = $_GET['edit'];
    #     $update = true;
    #     $result = $mysqli->query("SELECT * FROM data WHERE id=$id") or die($mysqli->error());
    #     if ($result->num_rows) {
    #         $row = $result->fetch_array();
    #         $task = $row['task'];
    #         $description = $row['description'];
    #         $status = $row['status'];
    #     }
    # }

    # if (isset($_POST['update'])){
    #     $id = $_POST['id'];
    #     $task = $_POST['task'];
    #     $description = $_POST['description'];
    #     $status = $_POST['status'];

    #     $mysqli->query("UPDATE data SET task='$task', description='$description', status='$status' WHERE id=$id") or die($mysqli->error);
    #     $_SESSION['message'] = "Record has been updated!";
    #     $_SESSION['msg_type'] = "warning";

    #     header('Location: index.php');
    # }

    # ?>


if __name__ == "__main__":
    # Connect & setup database
    try:
        dbString = r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' + \
            os.getcwd() + r'\db.accdb;'
        conn = pyodbc.connect(dbString)
        db = conn.cursor()
    except pyodbc.Error as e:
        print("Error connecting to DB: ", e)

    app.run(debug=True)
