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
             
    def __search_coursebank_by_name(self, courseName):
        """Returns the query results for the Course Table when queried by the course's name"""
        return app.CourseBank.query.filter_by(cName=courseName).first()

    def __search_coursebank_by_code(self, courseCode):
        """Returns the query results for the CourseBank Table when queried by the cours's code (ie, 180) """
        return app.CourseBank.query.filter_by(cCode=courseCode).first()

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


    def test_succesful_search_course(self):
        course = self.__search_coursebank_by_name("Principles Of Software Engineering")
        self.assertEqual("Principles Of Software Engineering", course.cName)
        
        course = self.__search_coursebank_by_name("C++ Programming")
        self.assertEqual("C++ Programming", course.cName)

        it326byCode = self.__search_coursebank_by_code(326)
        it326byName = self.__search_coursebank_by_name("Principles Of Software Engineering")
        self.assertEqual(it326byCode, it326byName)

    
    def test_failed_search_course(self):
        course = self.__search_coursebank_by_name("Intro to Underwater Basket Weaving")
        self.assertIsNone(course)

        course = self.__search_coursebank_by_code(1)
        self.assertIsNone(course)

        it326 = self.__search_coursebank_by_name("Principles Of Software Engineering")
        self.assertFalse(it326.cName == "C++ Programming")

if __name__ == '__main__':
    unittest.main()
    