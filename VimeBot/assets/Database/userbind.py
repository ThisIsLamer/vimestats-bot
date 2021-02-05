import sqlite3

def start():
    db = sqlite3.connect('assets/Database/database.db')
    sql = db.cursor()

    sql.execute('''CREATE TABLE IF NOT EXISTS userbind (
        id INT,
        nick TEXT
    )''')

    db.commit()
    return db, sql

def add(sql, db, id, nick):
    sql.execute(f"SELECT id FROM userbind WHERE id = '{id}'")
    if sql.fetchone() is None:
        sql.execute(f"INSERT INTO userbind VALUES (?,?)", (id, nick))
    else:
        sql.execute(f"UPDATE userbind SET nick = '{nick}' WHERE id = '{id}'")
    db.commit()

def remove(sql, db, id):
    sql.execute(f"SELECT id FROM userbind WHERE id = '{id}'")
    if sql.fetchone() != None:
        sql.execute(f"DELETE FROM userbind WHERE id = '{id}'")
        db.commit()

def getNick(sql, db, id):
    sql.execute(f"SELECT nick FROM userbind WHERE id = '{id}'")
    return sql.fetchone()