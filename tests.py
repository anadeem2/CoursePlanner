import unittest
import app

class TestDB(unittest.TestCase):

    def test_new_student(self):
        student = app.Student("test@email.com", "123", "Fname", "Lname")

        self.assertEqual(student.sEmail, "test@email.com")
        self.assertEqual(student.sPassword, "123")
        self.assertEqual(student.sFName, "Fname")
        self.assertEqual(student.sLName, "Lname")

        # app.db.session.add(student)
        # app.db.session.commit()


class TestApp(unittest.TestCase):

    def test_login(self):
        email="test@email.com"
        password="123"

        user = app.Student.query.filter_by(sEmail=email, sPassword=password).first()
        self.assertEqual(user.sEmail, "test@email.com")

    def test_logout(self):
        email="test@email.com"
        password="123"

        print(app.user)
        app.user = app.Student.query.filter_by(sEmail=email, sPassword=password).first()
        print(app.user.sEmail)

        app.logout()
        print("hello")

        self.assertEqual(app.user, None)


if __name__ == '__main__':
    unittest.main()