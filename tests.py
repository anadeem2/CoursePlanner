import unittest
import app

class TestDB(unittest.TestCase):

    def test_new_student(self):
        student = app.Student("test@email.com", "123", "Fname", "Lname")

        self.assertEqual(student.sEmail, "test@email.com")
        self.assertEqual(student.sPassword, "123")
        self.assertEqual(student.sFName, "Fname")
        self.assertEqual(student.sLName, "Lname")


class TestApp(unittest.TestCase):
    APP_URL = "http://127.0.0.1:5000/"
    LOGIN_URL = f"{APP_URL}/login"

    def test_login(self):
        email="usama@gmail.com"
        password="123"

        user = app.Student.query.filter_by(sEmail=email, sPassword=password).first()
        self.assertEqual(user.sEmail, "usama@gmail.com")




if __name__ == '__main__':
    unittest.main()