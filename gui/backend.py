import gradio

import core.database as database
import core.auth as auth
import core.grades as grades
import core.schedule as schedule
import core.team as team
import core.export as export
from core.hasher import hash_password

# ---------------------- LOGIKA ---------------------- #
def login(login, password):
    if login == "admin" and password == "admin":
        return (
            "Zalogowano jako Administrator", -1, "admin",
            gradio.update(visible=False), gradio.update(visible=True), gradio.update(visible=False)
        )

    user = auth.login_user(login, hash_password(password))
    if user:
        return (
            f"Zalogowano jako {user[1]} {user[2]}", user[0], user[1],
            gradio.update(visible=True), gradio.update(visible=False), gradio.update(visible=False)
        )
    return "Nieprawidłowy login lub hasło", None, None, gradio.update(visible=False), gradio.update(visible=False), gradio.update(visible=True)

# ---------------------- FUNKCJE STUDENTA ---------------------- #
def show_grades(student_id):
    return grades.get_grade(student_id)

def show_schedule(student_id):
    return schedule.get_schedule(student_id)

def show_stats(student_id):
    return grades.get_stats(student_id)

def export_grades(student_id):
    name = export.export_to_csv(grades.get_grade(student_id), ["Przedmiot", "Ocena", "Typ", "Semestr"])
    return f"Oceny zapisane do pliku {name}"

def export_schedule(student_id):
    name = export.export_to_csv(schedule.get_schedule(student_id), ["Dzień", "Przedmiot", "Od", "Do", "Sala"])
    return f"Plan zajęć zapisany do pliku {name}"

def export_stats(student_id):
    name = export.export_to_csv(grades.get_stats(student_id), ["Semestr", "Średnia"])
    return f"Statystyki zapisane do pliku {name}"

def change_password(student_id, old_pass, new_pass, repeat_new_pass):
    user = database.cursor.execute(
        """
        SELECT FirstName, LastName FROM Student
        WHERE Student_Id = ? AND PasswordHash = ?
        """, (student_id, hash_password(old_pass))
    ).fetchone()

    if user:
        if new_pass == repeat_new_pass and len(new_pass) >= 8:
            database.cursor.execute(
                "UPDATE Student SET PasswordHash = ? WHERE Student_Id = ?",
                (hash_password(new_pass), student_id)
            )
            database.conn.commit()
            return "Hasło zmienione pozytywnie"
        else:
            return "Nowe hasło jest niepoprawne"
    return "Obecne hasło jest niepoprawne"

# ---------------------- FUNKCJE ADMINISTRATORA ---------------------- #
def get_all_students():
    return database.cursor.execute("SELECT * FROM Student").fetchall()

def get_all_subjects():
    return database.cursor.execute("SELECT * FROM Subject").fetchall()

def get_all_teams():
    return database.cursor.execute("SELECT * FROM Team").fetchall()

def add_subject(subject_name):
    if len(subject_name) > 3:
        database.cursor.execute("INSERT INTO Subject (SubjectName) VALUES (?)", (subject_name,))
        database.conn.commit()
        return f"Dodano przedmiot: {subject_name}", gradio.update(choices=get_subject_choices()), gradio.update(choices=get_subject_choices())
    return "Nazwa przedmiotu musi mieć więcej niż 3 znaki", gradio.update(choices=get_subject_choices()), gradio.update(choices=get_subject_choices())

def add_team(team_name):
    if len(team_name) >= 2:
        team.add_team(team_name)
        return f"Dodano zespół: {team_name}", gradio.update(choices=get_team_choices()), gradio.update(choices=get_team_choices())
    return "Nazwa zespołu musi mieć przynajmniej 2 znaki", gradio.update(choices=get_team_choices()), gradio.update(choices=get_team_choices())

def add_student(first, last, login, password):
    if all(len(x) >= 3 for x in [first, last, login]) and len(password) >= 8:
        result = auth.register_user(first, last, login, hash_password(password))
        choices = get_student_choices()
        return result, gradio.update(choices=choices), gradio.update(choices=choices)
    return "Niepoprawne dane", gradio.update(choices=get_student_choices()), gradio.update(choices=get_student_choices())

def add_student_team(student_id, team_id):
    database.cursor.execute("INSERT INTO Student_Team (Student_Id, Team_Id) VALUES (?, ?)", (student_id, team_id))
    database.conn.commit()
    return f"Dodano studenta {student_id} do teamu {team_id}"

def add_grade(student_id, subject_id, grade, gtype, semester):
    grades.add_grade(student_id, subject_id, grade, gtype, semester)
    return f"Dodano ocenę: {grade} ({gtype}) dla studenta {student_id} z przedmiotu {subject_id}, semestr {semester}"

# ---------------------- POMOCNICZE ---------------------- #
def get_student_choices():
    return [f"{i[0]}: {i[1]} {i[2]}" for i in get_all_students()]

def get_subject_choices():
    return [f"{i[0]}: {i[1]}" for i in get_all_subjects()]

def get_team_choices():
    return [f"{i[0]}: {i[1]}" for i in get_all_teams()]

def split_id(label):
    return int(label.split(":")[0])
