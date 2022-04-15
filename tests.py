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



if __name__ == '__main__':
    unittest.main()
    