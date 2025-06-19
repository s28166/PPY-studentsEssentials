import core.database as database

def add_team(team_name):
    database.cursor.execute('''
        INSERT INTO Team (TeamName) VALUES (?)
    ''', (team_name,))
    database.conn.commit()

def get_team(team_id):
    database.cursor.execute('''
        SELECT * FROM Team WHERE Team_Id = ?
    ''', (team_id,))
    return database.cursor.fetchall()