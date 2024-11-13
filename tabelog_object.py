import sqlite3
import os

def create_table():
    db_path = 'tabelog.db'

    if not os.path.exists(db_path):
        conn = sqlite3.connect('tabelog.db')
        c = conn.cursor()
        c.execute('''
            CREATE TABLE tabelog (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                url TEXT,
                eat_type TEXT,
                score REAL
            )
        ''')
        conn.commit()
        conn.close()

class Tenpo():
    def __init__(self, name, url, eat_type, score):
        self.name = name
        self.url = url
        self.eat_type = eat_type
        self.score = score
    
    def __str__(self):
        return f'{self.name} {self.url} {self.eat_type} {self.score}'
    
    def save(self):
        conn = sqlite3.connect('tabelog.db')
        c = conn.cursor()
        c.execute('''
            INSERT INTO tabelog (name, url, eat_type, score) VALUES (?, ?, ?, ?)
        ''', (self.name, self.url, self.eat_type, self.score))
        conn.commit()
        conn.close()

def find_all():
    conn = sqlite3.connect('tabelog.db')
    c = conn.cursor()
    c.execute('SELECT * FROM tabelog')
    results = c.fetchall()
    conn.close()

    data = []
    for row in results:
        data.append({
            'name': row[1],
            'url': row[2],
            'eat_type': row[3],
            'score': row[4]
        })
    
    return data