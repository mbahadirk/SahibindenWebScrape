import sqlite3

def create_database():
    conn = sqlite3.connect('temp/locations.db')
    c = conn.cursor()

    # Şehirler tablosunu oluştur
    c.execute('''CREATE TABLE IF NOT EXISTS Şehirler (
                id INTEGER PRIMARY KEY,
                name TEXT UNIQUE
                )''')

    # İlçeler tablosunu oluştur
    c.execute('''CREATE TABLE IF NOT EXISTS İlçeler (
                id INTEGER PRIMARY KEY,
                name TEXT UNIQUE,
                city_id INTEGER,
                FOREIGN KEY (city_id) REFERENCES Şehirler(id)
                )''')

    # Mahalleler tablosunu oluştur
    c.execute('''CREATE TABLE IF NOT EXISTS Mahalleler (
                id INTEGER PRIMARY KEY,
                name TEXT UNIQUE,
                district_id INTEGER,
                FOREIGN KEY (district_id) REFERENCES İlçeler(id)
                )''')

    # Sokaklar tablosunu oluştur
    c.execute('''CREATE TABLE IF NOT EXISTS Sokaklar (
                id INTEGER PRIMARY KEY,
                name TEXT UNIQUE,
                neighborhood_id INTEGER,
                FOREIGN KEY (neighborhood_id) REFERENCES Mahalleler(id)
                )''')

    conn.commit()

def add_city(city_name):
    conn = sqlite3.connect('temp/locations.db')
    c = conn.cursor()
    try:
        c.execute("INSERT OR IGNORE INTO Şehirler (name) VALUES (?)", (city_name,))
        conn.commit()
    except sqlite3.IntegrityError:
        print(f"Şehir '{city_name}' zaten var, eklenemedi.")

def add_district(district_name, city_name):
    conn = sqlite3.connect('temp/locations.db')
    c = conn.cursor()
    try:
        c.execute('''INSERT OR IGNORE INTO İlçeler (name, city_id)
                     SELECT ?, id FROM Şehirler WHERE name = ?''', (district_name, city_name))
        conn.commit()
    except sqlite3.IntegrityError:
        print(f"İlçe '{district_name}' zaten var, eklenemedi.")

def add_neighborhood(neighborhood_name, district_name):
    conn = sqlite3.connect('temp/locations.db')
    c = conn.cursor()
    try:
        c.execute('''INSERT OR IGNORE INTO Mahalleler (name, district_id)
                     SELECT ?, id FROM İlçeler WHERE name = ?''', (neighborhood_name, district_name))
        conn.commit()
    except sqlite3.IntegrityError:
        print(f"Mahalle '{neighborhood_name}' zaten var, eklenemedi.")

def add_street(street_name, neighborhood_name):
    conn = sqlite3.connect('temp/locations.db')
    c = conn.cursor()
    try:
        c.execute('''INSERT OR IGNORE INTO Sokaklar (name, neighborhood_id)
                     SELECT ?, id FROM Mahalleler WHERE name = ?''', (street_name, neighborhood_name))
        conn.commit()
    except sqlite3.IntegrityError:
        print(f"Sokak '{street_name}' zaten var, eklenemedi.")
