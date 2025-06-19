import core.database as database

def init_db():
    database.cursor.execute('''
    CREATE TABLE IF NOT EXISTS Student (
        Student_Id INTEGER PRIMARY KEY AUTOINCREMENT,
        FirstName TEXT NOT NULL,
        LastName TEXT NOT NULL,
        Login TEXT NOT NULL UNIQUE,
        PasswordHash TEXT NOT NULL
    )
    ''')

    database.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Team (
            Team_Id INTEGER PRIMARY KEY AUTOINCREMENT,
            TeamName TEXT NOT NULL
        )    
    ''')

    database.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Student_Team (
            Student_Id INTEGER NOT NULL,
            Team_Id INTEGER NOT NULL,
            FOREIGN KEY (Student_Id) REFERENCES Student(Student_Id),
            FOREIGN KEY (Team_Id) REFERENCES Team(Team_Id)
            )    
    ''')

    database.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Subject (
            Subject_Id INTEGER PRIMARY KEY AUTOINCREMENT,
            SubjectName TEXT NOT NULL
        )     
    ''')

    database.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Subject_Team (
                Subject_Id INTEGER NOT NULL,
                Team_Id INTEGER NOT NULL,
                FOREIGN KEY (Subject_Id) REFERENCES Subject(Subject_Id),
                FOREIGN KEY (Team_Id) REFERENCES Team(Team_Id)
            )  
    ''')

    database.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Grade (
            Student_Id INTEGER NOT NULL,
            Subject_Id INTEGER NOT NULL,
            Grade INTEGER NOT NULL,
            GradeType TEXT CHECK(GradeType in ('Practical Part','Exam')) NOT NULL DEFAULT 'Practical Part',
            Semester INTEGER NOT NULL,
            FOREIGN KEY (Student_Id) REFERENCES Student(Student_Id),
            FOREIGN KEY (Subject_Id) REFERENCES Subject(Subject_Id)
        )     
    ''')

    database.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Schedule (
            Schedule_Id INTEGER PRIMARY KEY AUTOINCREMENT,
            Subject_Id INTEGER NOT NULL,
            Team_Id INTEGER NOT NULL,
            DayOfWeek TEXT CHECK(DayOfWeek in ('Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday')) NOT NULL DEFAULT 'Monday',
            StartTime TIME NOT NULL,
            EndTime TIME NOT NULL,
            Classroom TEXT NOT NULL,
            FOREIGN KEY (Subject_Id) REFERENCES Subject(Subject_Id),
            FOREIGN KEY (Team_Id) REFERENCES Team(Team_Id)
        )    
    ''')