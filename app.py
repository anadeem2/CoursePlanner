from flask import Flask, render_template, request
from cs50 import SQL

app = Flask(__name__)
db = SQL('student.db')


@app.route('/')
def index():                                                  
    return render_template("index.html")

@app.route('/login')
def login():                                                
    return render_template("login.html")

@app.route('/signup')
def signup():
    return render_template("signup.html")

@app.route('/registered', methods=["POST"])
def registered():
    user_email = request.form.get("email")
    user_pass = request.form.get("password")
    db.execute("INSERT INTO student (email, password) VALUES (?,?)", user_email, user_pass)

    return render_template("registered.html")


@app.route('/mainpage', methods=["POST"])
def mainpage():        
    user_email = request.form.get("email")
    user_pass = request.form.get("password")

    row = db.execute("SELECT FROM student WHERE email=? AND password=?", user_email, user_pass)
    print(row)
    if len(row)==0:
        return render_template("error.html", message="Incorrect password or user")
    else:
        return render_template("mainpage.html")

if __name__ == "__main__":
    app.run(debug=True)