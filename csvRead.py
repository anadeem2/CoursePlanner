import csv

with open("IT 326 course list.csv", "r") as f:
    reader = csv.reader(f, delimiter=",")
    for line in reader:
        dept,code,name,credits,desc = line[0],line[1],line[2],line[3],line[5]
        print(dept,code,name,credits,desc)





    # COURSES = CourseBank.query.filter_by(cDept="IT").all()
    # for c in COURSES:
    #     print(c.cDept,c.cCode)