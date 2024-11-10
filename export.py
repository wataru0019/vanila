import sqlite3
import os

def yahoo():
    print('yahoo')

def create_table():
    db_path = 'user.db'

    if not os.path.exists(db_path):
        conn = sqlite3.connect('user.db')
        c = conn.cursor()
        c.execute('CREATE TABLE user (id INTEGER PRIMARY KEY, name TEXT, password TEXT)')
        conn.commit()
        conn.close()
        print(f'{db_path} created')
    else:
        print(f'{db_path} already exists')