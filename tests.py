import unittest
import app


class TestApp(unittest.TestCase):
    def test_login(self):
        email = "test@email.com"
        password = "123"

        user = app.Student.query.filter_by(sEmail=email, sPassword=password).first()
        self.assertIsNotNone(user)

        email = "test@email.com"
        password = "321"

        user = app.Student.query.filter_by(sEmail=email, sPassword=password).first()
        self.assertIsNone(user)


    def test_deleteUser(self):
        user_email = "test@email.com"
        user = app.Student.query.filter_by(sEmail=user_email).first()
        self.assertEqual(user.sEmail, user_email)

        user_email="usama@gmail.com"
        user = app.Student.query.filter_by(sEmail=user_email).first()
        self.assertEqual(user.sEmail, user_email)

        user_email = "notreal@gmail.com"
        user = app.Student.query.filter_by(sEmail=user_email).first()
        self.assertIsNone(user)

    def test_signUp(self):
        user_email = "newaccount@email.com"
        user_pass = "123"
        user_fname = "Pie"
        user_lname = "name"

        user = app.Student.query.filter_by(sEmail=user_email).first() #Account doesnt exist
        self.assertIsNone(user)

        student = app.Student(email=user_email, password=user_pass, fname=user_fname, lname=user_lname)
        user = app.Student.query.filter_by(sEmail=user_email).first()

        self.assertEqual(student.sEmail, user_email)
        self.assertEqual(student.sPassword, user_pass)
        self.assertEqual(student.sFName, user_fname)
        self.assertEqual(student.sLName, user_lname)

        user_email = "usama@gmail.com"

        user = app.Student.query.filter_by(sEmail=user_email).first()  # Account exist
        self.assertIsNotNone(user)

    def test_forgot(self):
        user_email = "test@email.com"
        user = app.Student.query.filter_by(sEmail=user_email).first()
        self.assertEqual(user.sEmail, "test@email.com")

        user_email = "fake@email.com"
        user = app.Student.query.filter_by(sEmail=user_email).first()
        self.assertIsNone(user)


    def __search_major_by_name(self, majorName):
        """Returns the query results for the Major Table when queried by the major's name"""
        return app.Major.query.filter_by(mName=majorName).first()

    def __search_major_by_id(self, majorID):
        """Returns the query results for the Major Table when queried by the major's name"""
        return app.Major.query.filter_by(mID=majorID).first()

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
        major = self.__search_major_by_name(
            "Political Science")  # no results will be found, so a None object is returned
        self.assertIsNone(major)

        major = self.__search_major_by_name("Waiter")
        self.assertIsNone(major)

        comsciMajor = self.__search_major_by_name("Computer Science")
        self.assertFalse(
            "Cyber Security" == comsciMajor.mName)  # comparing 'Cyber Security' w/ 'Computer Science' so expected result is False
        major = self.__search_major_by_name("Waiter")
        self.assertIsNone(major)

        comsciMajor = self.__search_major_by_name("Computer Science")
        self.assertFalse(
            "Cyber Security" == comsciMajor.mName)  # comparing 'Cyber Security' w/ 'Computer Science' so expected result is False

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

    def test_update_major(self):
        email = "test@email.com"
        password = "123"
        user = app.Student.query.filter_by(sEmail=email, sPassword=password).first()
        app.db.session.add(user)

        # Selecting first major
        major1 = self.__search_major_by_id(1)
        user.sMajorID = major1.mID
        self.assertEqual(self.__search_major_by_id(user.sMajorID), major1)

        # Seeing if DB is updated when the major is changed
        major2 = self.__search_major_by_id(2)
        user.sMajorID = major2.mID
        self.assertNotEqual(self.__search_major_by_id(user.sMajorID), major1)
        self.assertEqual(self.__search_major_by_id(user.sMajorID), major2)

        # Comparing other attributes of Major class
        curMajor = self.__search_major_by_id(user.sMajorID)  # current majorID is 2
        major3 = self.__search_major_by_id(3)
        self.assertEqual(curMajor.mID, major2.mID)
        self.assertEqual(curMajor.mName, major2.mName)
        self.assertEqual(curMajor.mDept, major2.mDept)
        self.assertNotEqual(curMajor.mID, major3.mID)
        self.assertNotEqual(curMajor.mName, major3.mName)

        app.db.session.commit()


if __name__ == '__main__':
    unittest.main()