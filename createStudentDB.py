import sqlite3

connection = sqlite3.connect('planner.db')
c = connection.cursor()

# c.execute("""DROP TABLE student""")
# c.execute("""DROP TABLE courses""")
# c.execute("""DROP TABLE CourseList""")

c.execute("""CREATE TABLE student(
                sID INTEGER,
                sEmail TEXT NOT NULL,
                sFName TEXT,
                sLName TEXT,
                sUsername TEXT,
                sPassword TEXT NOT NULL,
                PRIMARY KEY(sID)) """)

c.execute("""CREATE TABLE courses(
                cID INTEGER,
                cDept TEXT,
                cCode TEXT,
                cName TEXT,
                PRIMARY KEY(cID)) """)



c.execute("""CREATE TABLE CourseList(
                cID INTEGER,
                cDept TEXT,
                cCode TEXT,
                cName TEXT,
                PRIMARY KEY(cID)) """)

connection.commit()
connection.close()

# class Student(db.Model):
#     sID = db.Column(db.Integer, pirmary_key=True)
#     sEmail = db.Column(db.String(200), nullable=False)
#     sFName = db.Column(db.String(200), nullable=False)
#     sLName = db.Column(db.String(200), nullable=False)
#     sUsername = db.Column(db.String(200), nullable=False)
#     sPassword = db.Column(db.String(200), nullable=False)
#     # sCourseList = db.relationship("CourseList")

#     # def __repr__(self):
#     #     return self.sID


# class Course(db.Model):
#     cID = db.Column(db.Integer, pirmary_key=True)
#     cDept = db.Column(db.String(200), nullable=False)  # IT
#     cCode = db.Column(db.Integer(4), nullable=False)  # 383
#     cName = db.Column(db.String(200), nullable=False)  # Operating Systems
#     # Humanties (H), Language in Humanities (LH), etc.
#     cGenEd = db.Column(db.String(2), nullable=True)
#     # GenEd (0), Core class (1), Elective (2)
#     cRequirement = db.Column(db.Integer(2), nullable=True)
#     cCredits = db.Column(db.Integer(2), nullable=False)
#     # cCourseList = db.relationship("CourseList")

#     def __repr__(self):
#         return self.cID


# class CourseList(db.Model):
#     clID = db.Column(db.Integer, pirmary_key=True)
#     # cID = db.Collumn(db.Integer, foreign_key = 'Course.cID')
#     # cID = db.Collumn(db.Integer, foreign_key = 'Student.sID')
#     # Inprogress (IP), Taken (T), Planned (P)
#     clType = db.Column(db.String(2), nullable=False)
#     clGrade = db.Column(db.String(2), nullable=True)
#     clDifficulity = db.Column(db.String(2), nullable=True)
#     clPreRequisite = db.Column(db.String(200), nullable=True)
#     clSkills = db.Column(db.String(200), nullable=True)

#     def __repr__(self):
#         return self.clID

