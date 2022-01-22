import sqlite3

connection = sqlite3.connect('IT326Project\student.db')
c = connection.cursor()

c.execute("""CREATE TABLE student(
                id INTEGER,
                email TEXT NOT NULL,
                password TEXT NOT NULL,
                PRIMARY KEY(id)) """)

connection.commit()
connection.close()