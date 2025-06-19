import core.database as database

def register_user(first_name, last_name, login, password):
    database.cursor.execute('''
        INSERT INTO Student (FirstName, LastName, Login, PasswordHash) VALUES (?, ?, ?, ?)
    ''', (first_name, last_name, login, password))
    database.conn.commit()
    return f"{first_name} {last_name} registered successfully"

def login_user(login, password):
    database.cursor.execute('''
        SELECT * FROM Student
            WHERE Login = ? AND PasswordHash = ?
    ''', (login, password))
    return database.cursor.fetchone()

def password_change(login, old_password, new_password):
    database.cursor.execute('''
        UPDATE Student SET PasswordHash = ? WHERE Login = ? AND Password = ?
    ''', (new_password, login, old_password))
    return "Password changed successfully"