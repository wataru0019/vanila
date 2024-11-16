import sqlite3

import csv
import os

def create_table():
    db_path = 'stocklist.db'

    if not os.path.exists(db_path):
        conn = sqlite3.connect('stocklist.db')
        c = conn.cursor()
        c.execute('''
            CREATE TABLE stocklist (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                stockid TEXT,
                name TEXT,
                market TEXT,
                type1 TEXT,
                type2 TEXT
            )
        ''')
        conn.commit()
        conn.close()

class Stock():
    def __init__(self, stockid, name, market, type1, type2):
        self.stockid = stockid
        self.name = name
        self.market = market
        self.type1 = type1
        self.type2 = type2
    
    def __str__(self):
        return f'{self.stockid} {self.name} {self.market} {self.type1} {self.type2}'
    
    def save(self):
        conn = sqlite3.connect('stocklist.db')
        c = conn.cursor()
        c.execute('''
            INSERT INTO stocklist (stockid, name, market, type1, type2) VALUES (?, ?, ?, ?, ?)
        ''', (self.stockid, self.name, self.market, self.type1, self.type2))
        conn.commit()
        conn.close()
    
    def find(str):
        conn = sqlite3.connect('stocklist.db')
        c = conn.cursor()
        c.execute('SELECT * FROM stocklist WHERE stockid = ?', (str,))
        c.execute('SELECT * FROM stocklist WHERE stockid LIKE ?', ('%' + str + '%',))
        results = c.fetchall()
        conn.close()
        
        data = []
        for row in results:
            data.append({
                'stockid': row[1],
                'name': row[2],
                'market': row[3],
                'type1': row[4],
                'type2': row[5]
            })
        
        return data
    
    def find_any(str):
        conn = sqlite3.connect('stocklist.db')
        c = conn.cursor()
        c.execute('SELECT * FROM stocklist WHERE stockid LIKE ? OR name LIKE ?', ('%' + str + '%', '%' + str + '%'))
        results = c.fetchall()
        conn.close()
        
        data = []
        for row in results:
            data.append({
                'stockid': row[1],
                'name': row[2],
                'market': row[3],
                'type1': row[4],
                'type2': row[5]
            })
        
        return data
    
def read_csv():
    create_table()
    with open('data_j.csv', mode='r', encoding='utf-8') as f:
        reader = csv.reader(f)
        
        for row in reader:
            stock = Stock(row[1], row[2], row[3], row[5], row[7])
            print(stock)
            stock.save()

def find_stock(str):
    # data = Stock.find(str)
    data = Stock.find_any(str)
    print(data[0:5])

if __name__ == "__main__":
    find_stock('関西')