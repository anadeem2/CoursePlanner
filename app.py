from flask import Flask, render_template, request, jsonify
from cs50 import SQL
from flask_mail import Mail, Message

app = Flask(__name__)
app.config["MAIL_DEFAULT_SENDER"] = "classplannerit326@gmail.com"
app.config['MAIL_USERNAME'] = "classplannerit326@gmail.com"
app.config['MAIL_PASSWORD'] = "Planner123!"
app.config['MAIL_PORT'] = 587
app.config['MAIL_SERVER'] = "smtp.gmail.com"
app.config['MAIL_USE_TLS'] = True
mail = Mail(app)

db = SQL('sqlite:///student.db')
COURSES = ["IT327", "IT383", "IT179", "IT180", "IT326"]

@app.route('/')
def index():

    return render_template("index.html")

@app.route('/login') #Login page
def login():                                                
    return render_template("login.html")

@app.route('/signup') #Signup page
def signup():
    return render_template("signup.html")

@app.route('/registered', methods=["POST"]) #Registered Page
def registered():
    user_email = request.form.get("email")
    user_pass = request.form.get("password")

    row = db.execute("SELECT * FROM student WHERE email=?", user_email) #Check if account already exists
    if len(row) == 1:
        return render_template("error.html", message="Account already exists") #Throw error if exists
    else:
        db.execute("INSERT INTO student (email, password) VALUES (?,?)", user_email, user_pass) #Else add user info to DB

        # Send confirmaton email
        message = Message("You have been successfully registered! This is a confirmation email.", recipients=[user_email])
        mail.send(message)

        return render_template("registered.html") #Maybe redirect to mainpage


@app.route('/mainpage', methods=["POST"])
def mainpage():
    user_email = request.form.get("email")
    user_pass = request.form.get("password")

    row = db.execute("SELECT * FROM student WHERE email=? AND password=?", user_email, user_pass) #Confirm login authentication
    if len(row)==0:
        return render_template("error.html", message="Incorrect password or user")
    else:
        return render_template("mainpage.html", courses=COURSES)


if __name__ == "__main__":
    app.run(debug=True)