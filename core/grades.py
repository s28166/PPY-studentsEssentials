import core.database as database

def add_grade(student_id, subject_id, grade, grade_type, semester):
    database.cursor.execute('''
        INSERT INTO Grade (Student_Id, Subject_Id, Grade, GradeType, Semester) VALUES (?, ?, ?, ?, ?)
    ''', (student_id, subject_id, grade, grade_type, semester))
    database.conn.commit()

def get_grade(student_id):
    database.cursor.execute('''
        SELECT Subject.SubjectName, Grade, GradeType, Semester FROM Grade
        JOIN Subject ON Grade.Subject_Id = Subject.Subject_Id
        WHERE Grade.Student_Id = ?
    ''', (student_id,))
    return database.cursor.fetchall()

def get_stats(student_id):
    database.cursor.execute('''
        SELECT Semester, AVG(Grade) FROM Grade WHERE Student_Id = ? GROUP BY Semester ORDER BY Semester ASC
    ''', (student_id,))
    return database.cursor.fetchall()