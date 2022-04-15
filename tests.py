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

    

    def __search_major_by_name(self, majorName):
        """Returns the query results for the Major Table when queried by the major's name"""
        return app.Major.query.filter_by(mName=majorName).first()
             
    
    def test_succesful_search_major(self):   
        major = self.__search_major_by_name("Computer Science")
        self.assertEqual("Computer Science", major.mName)

        major = self.__search_major_by_name("Cyber Security")
        self.assertEqual("Cyber Security", major.mName)

        major = self.__search_major_by_name("Information Technology")
        self.assertEqual("Information Technology", major.mName)


    def test_failed_search_major(self):
        major = self.__search_major_by_name("Political Science") # no results will be found, so a None object is returned
        self.assertIsNone(major)

        major = self.__search_major_by_name("Waiter")
        self.assertIsNone(major)


        comsciMajor = self.__search_major_by_name("Computer Science")
        self.assertFalse("Cyber Security" == comsciMajor.mName) # comparing 'Cyber Security' w/ 'Computer Science' so expected result is False

        self.assertEqual(app.user, None)


if __name__ == '__main__':
    unittest.main()
    