import sqlite3


def create_table():
    conn = sqlite3.connect('veritabani.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS veriler (
                id INTEGER PRIMARY KEY,
                link TEXT,
                text TEXT
                )''')
    conn.commit()
    conn.close()

create_table()

def add_data(link, text):
    conn = sqlite3.connect('veritabani.db')
    c = conn.cursor()
    c.execute("INSERT INTO veriler (link, text) VALUES (?, ?)", (link, text))
    conn.commit()
    conn.close()

add_data("örnek_link", "örnek_metin")