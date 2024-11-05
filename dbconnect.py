from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sqlite3

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

conn = sqlite3.connect('pokemons.db')
c = conn.cursor()
# c.execute('CREATE TABLE pokemons (id INTEGER PRIMARY KEY, name TEXT, type TEXT)')
c.execute('INSERT INTO pokemons (name, type) VALUES ("Pikachu", "Electric")')
c.execute('INSERT INTO pokemons (name, type) VALUES ("Zenigame", "Water")')
conn.commit()
conn.close()

@app.get("/")
def read_root():
    conn = sqlite3.connect('pokemons.db')
    c = conn.cursor()
    c.execute('SELECT * FROM pokemons')
    pokemons = c.fetchall()
    conn.close()
    return pokemons