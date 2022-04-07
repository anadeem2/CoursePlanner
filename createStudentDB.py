import sqlite3

from sqlalchemy import ForeignKey

connection = sqlite3.connect('final.db')
c = connection.cursor()

# c.execute("""DROP TABLE student""")
# c.execute("""DROP TABLE courses""")
# c.execute("""DROP TABLE CourseList""")

c.execute("""CREATE TABLE student(
                sID INTEGER,
                sEmail TEXT NOT NULL,
                sFName TEXT,
                sLName TEXT,
                sPassword TEXT NOT NULL,
                PRIMARY KEY(sID)) """)

c.execute("""CREATE TABLE course(
                cID INTEGER,
                cDept TEXT,
                cCode TEXT,
                cName TEXT,
                textBook TEXT, 
                PRIMARY KEY(cID)) """)


c.execute("""CREATE TABLE courseList(
                clID INTEGER,
                clStatus INTEGER,
                courseID INTEGER,
                studentID INTEGER,
                FOREIGN KEY(courseID) REFERENCES course(cID),
                FOREIGN KEY(studentID) REFERENCES course(sID),
                PRIMARY KEY(clID)) """)

connection.commit()
connection.close()

class Student(db.Model):
    sID = db.Column(db.Integer, pirmary_key=True)
    sEmail = db.Column(db.String(200), nullable=False)
    sFName = db.Column(db.String(200), nullable=False)
    sLName = db.Column(db.String(200), nullable=False)
    sPassword = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return self.sID


class Course(db.Model):
    cID = db.Column(db.Integer, pirmary_key=True)
    cDept = db.Column(db.String(200), nullable=False)  # IT
    cCode = db.Column(db.Integer(4), nullable=False)  # 383
    cName = db.Column(db.String(200), nullable=False)  # Operating Systems
     # Grade 5 = A 1 = F
    cAvgGrade = db.Column(db.Float(1), nullable=True)
    # 1 = True 0 = False
    cTextbook = db.Column(db.Float(1), nullable=True)
    cCredits = db.Column(db.Integer(1), nullable=False)
    # 1-5 scale 5 = most difficult
    cDifficulty = db.Column(db.Float(1), nullable=True)
    # skill suggestions
    cSkill = db.Column(db.String(200), nullable=True)
    # avg online
    cQuality = db.Column(db.Float(1), nullable=True)

    


    def __repr__(self):
        return self.cID


class CourseList(db.Model):
    clID = db.Column(db.Integer, pirmary_key=True)
    clStudentID = db.Column("clStudentID", ForeignKey('Student.sID'), nullable=False)
    clCourseID = db.Column("clCourseID", ForeignKey('Course.sID'), nullable=False)
    # 1 = Inprogress (IP), 2 =  Taken (T), 3 = Planned (P)
    clStatus = db.Column(db.Integer(1), nullable=False)
    clGrade = db.Column(db.String(2), nullable=True)
    

    def __repr__(self):
        return self.clID
