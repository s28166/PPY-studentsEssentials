import core.database as database

def get_schedule(student_id):
    database.cursor.execute('''
        SELECT s.DayOfWeek, sub.SubjectName, s.StartTime, s.EndTime, s.Classroom, t.TeamName
        FROM Schedule s
        JOIN Subject sub ON s.Subject_Id = sub.Subject_Id
        JOIN Team t ON s.Team_Id = t.Team_Id
        JOIN Student_Team st ON t.Team_Id = st.Team_Id
        WHERE st.Student_Id = ?
        ORDER BY 
            CASE s.DayOfWeek 
                WHEN 'Monday' THEN 1
                WHEN 'Tuesday' THEN 2
                WHEN 'Wednesday' THEN 3
                WHEN 'Thursday' THEN 4
                WHEN 'Friday' THEN 5
                WHEN 'Saturday' THEN 6
                WHEN 'Sunday' THEN 7
            END,
            s.StartTime
    ''', (student_id,))
    return database.cursor.fetchall()


def add_schedule(subject_id, team_id, day, start_time, end_time, classroom):
    database.cursor.execute('''
        INSERT INTO Schedule (Subject_Id, Team_Id, DayOfWeek, StartTime, EndTime, Classroom) 
            VALUES (?, ?, ?, ?, ?, ?)
    ''', (subject_id, team_id, day, start_time, end_time, classroom))
    database.conn.commit()