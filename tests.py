import unittest
import app
from flask_session import Session
from flask_mail import Mail, Message

class TestDB(unittest.TestCase):

    def test_new_student(self):
        student = app.Student("test@email.com", "123", "Fname", "Lname")

        self.assertEqual(student.sEmail, "test@email.com")
        self.assertEqual(student.sPassword, "123")
        self.assertEqual(student.sFName, "Fname")
        self.assertEqual(student.sLName, "Lname")
        app.db.session.add(student)
        app.db.session.commit()


class TestApp(unittest.TestCase):
    APP_URL = "http://127.0.0.1:5000/"
    LOGIN_URL = f"{APP_URL}/login"

    def test_login(self):
        email="usama@gmail.com"
        password="123"

        user = app.Student.query.filter_by(sEmail=email, sPassword=password).first()
        self.assertEqual(user.sEmail, "usama@gmail.com")


class TestApp(unittest.TestCase):
    APP_URL = "http://127.0.0.1:5000/"
    SIGNUP_URL = f"{APP_URL}/signUp"

    def test_signUp(self):
        user_email="usama@gmail.com"
        user_pass="123"
        user_fname ="Usama"
        user_lname="Nadeem"

        user = app.Student.query.filter_by(email=user_email, password=user_pass, fname=user_fname, lname=user_lname).first()
        self.assertEqual(user.sEmail, "usama@gmail.com")

class TestApp(unittest.TestCase):
    APP_URL = "http://127.0.0.1:5000/"
    deleteUser_URL = f"{APP_URL}/deleteUser"

    def test_deleteUser(self):
        self.delete()
        session.commit()

class TestApp(unittest.TestCase):
    APP_URL = "http://127.0.0.1:5000/"
    deleteUser_URL = f"{APP_URL}/forgot"

    def test_forgot(self):
        user_email = "test@email.com"
        
        message = Message(
            "Your forgotten password: " + exists.sPassword, recipients=[user_email])
        mail.send(message)
        #I am not sure where the actual code for when the user resets the password with the email exists sorry 


    
       

if __name__ == '__main__':
    unittest.main()