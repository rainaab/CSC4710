import sqlite3

# Connect to database
con = sqlite3.connect('univ.db')
cur = con.cursor()

cur.execute("DROP TABLE IF EXISTS instructor")

cur.execute("""
CREATE TABLE instructor (
    id INTEGER PRIMARY KEY, 
    name TEXT,
    department TEXT,
    salary REAL
)
""")
cur.execute("""
INSERT INTO instructor
VALUES (1, 'Johnathon Godbey', 'Math', 75000)
""")

cur.execute("""
INSERT INTO instructor
VALUES (2, 'Barry Iforgot', 'English', 80000)
""")

cur.execute("""
INSERT INTO instructor
VALUES (3, 'Omesh Kini', 'Finance', 70000)
""")

cur.execute("""
INSERT INTO instructor
VALUES (4, 'Zendaya Holland', 'Acting', 95000)
""")

con.commit()

instructor_id = input("Enter instructor ID: ")

cur.execute(
    "SELECT * FROM instructor WHERE id = ?",
    (instructor_id,)
)
result = cur.fetchone()

if result:
    print(result)
else:
    print("Instructor not found.")

con.close()