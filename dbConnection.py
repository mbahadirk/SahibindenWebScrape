import sqlite3

name = "Elektrik & Enerji"

# Veritabanı bağlantısını oluştur
conn = sqlite3.connect(f'temp/{name}.db')
c = conn.cursor()

# Tabloları oluştur (Eğer henüz yoksa)
c.execute('''CREATE TABLE IF NOT EXISTS root_categories
             (title TEXT, slug TEXT)''')

c.execute('''CREATE TABLE IF NOT EXISTS parent1_categories
             (id INTEGER, title TEXT, slug TEXT PRIMARY KEY, root_title TEXT,
             FOREIGN KEY (root_title) REFERENCES root_categories(title))''')

c.execute('''CREATE TABLE IF NOT EXISTS parent2_categories
             (id INTEGER, title TEXT, slug TEXT PRIMARY KEY, parent1_title TEXT,
             FOREIGN KEY (parent1_title) REFERENCES parent1_categories(title))''')

c.execute('''CREATE TABLE IF NOT EXISTS parent3_categories
             (id INTEGER, title TEXT, slug TEXT PRIMARY KEY, parent2_title TEXT,
             FOREIGN KEY (parent2_title) REFERENCES parent2_categories(title))''')

c.execute('''CREATE TABLE IF NOT EXISTS parent4_categories
             (id INTEGER, title TEXT, slug TEXT PRIMARY KEY, parent3_title TEXT,
             FOREIGN KEY (parent3_title) REFERENCES parent3_categories(title))''')

c.execute('''CREATE TABLE IF NOT EXISTS parent5_categories
             (id INTEGER, title TEXT, slug TEXT PRIMARY KEY, parent4_title TEXT,
             FOREIGN KEY (parent4_title) REFERENCES parent4_categories(title))''')

c.execute('''CREATE TABLE IF NOT EXISTS parent6_categories
             (id INTEGER, title TEXT, slug TEXT PRIMARY KEY, parent5_title TEXT,
             FOREIGN KEY (parent5_title) REFERENCES parent5_categories(title))''')

# Veritabanına ekleme fonksiyonları
def add_root_category(title, slug):
    try:
        c.execute("INSERT OR IGNORE INTO root_categories (title, slug) VALUES (?, ?)", (title, slug))
        conn.commit()
    except sqlite3.IntegrityError:
        print(f"                                                            {title} kategorisi zaten var, eklenmedi.")

def add_parent1_category(title, slug, root_title):
    try:
        c.execute("INSERT INTO parent1_categories (title, slug, root_title) VALUES (?, ?, ?)",
                  (title, slug, root_title))
        conn.commit()
    except sqlite3.IntegrityError:
        print(f"                                                            {title} kategorisi zaten var, eklenmedi.")

def add_parent2_category(title, slug, parent1_title):
    try:
        c.execute("INSERT INTO parent2_categories (title, slug, parent1_title) VALUES (?, ?, ?)",
              (title, slug, parent1_title))
        conn.commit()
    except sqlite3.IntegrityError:
        print(f"                                                            {title} kategorisi zaten var, eklenmedi.")

def add_parent3_category(title, slug, parent2_title):
    try:
        c.execute("INSERT INTO parent3_categories (title, slug, parent2_title) VALUES (?, ?, ?)",
                  (title, slug, parent2_title))
        conn.commit()
    except sqlite3.IntegrityError:
        print(f"                                                            {title} kategorisi zaten var, eklenmedi.")
def add_parent4_category(title, slug, parent3_title):
    try:
        c.execute("INSERT INTO parent4_categories (title, slug, parent3_title) VALUES (?, ?, ?)",
                  (title, slug, parent3_title))
        conn.commit()
    except sqlite3.IntegrityError:
        print(f"                                                            {title} kategorisi zaten var, eklenmedi.")
def add_parent5_category(title, slug, parent4_title):
    try:
        c.execute("INSERT INTO parent5_categories (title, slug, parent4_title) VALUES (?, ?, ?)",
                  (title, slug, parent4_title))
        conn.commit()

    except sqlite3.IntegrityError:
        print(f"                                                            {title} kategorisi zaten var, eklenmedi.")

def add_parent6_category(title, slug, parent5_title):
    try:
        c.execute("INSERT INTO parent6_categories (title, slug, parent5_title) VALUES (?, ?, ?)",
                  (title, slug, parent5_title))
        conn.commit()
    except sqlite3.IntegrityError:
        print(f"                                                            {title} kategorisi zaten var, eklenmedi.")


# Veri silme işlemi
def delete_categories_by_slug(slug):
    try:
        c.execute("DELETE FROM parent2_categories WHERE slug=?", (slug,))
        conn.commit()

        # Diğer tablolardaki ilgili verileri silmek için CASCADE kısıtlamasını kullanabilirsiniz.
        # Örneğin:
        c.execute("DELETE FROM parent2_categories WHERE parent1_title=?", (slug,))
        c.execute(
            "DELETE FROM parent3_categories WHERE parent2_title IN (SELECT slug FROM parent2_categories WHERE parent1_title=?)",
            (slug,))
        c.execute(
            "DELETE FROM parent4_categories WHERE parent3_title IN (SELECT slug FROM parent3_categories WHERE parent2_title IN (SELECT slug FROM parent2_categories WHERE parent1_title=?))",
            (slug,))
        c.execute(
            "DELETE FROM parent5_categories WHERE parent4_title IN (SELECT slug FROM parent4_categories WHERE parent3_title IN (SELECT slug FROM parent3_categories WHERE parent2_title IN (SELECT slug FROM parent2_categories WHERE parent1_title=?)))",
            (slug,))
        c.execute(
            "DELETE FROM parent6_categories WHERE parent5_title IN (SELECT slug FROM parent5_categories WHERE parent4_title IN (SELECT slug FROM parent4_categories WHERE parent3_title IN (SELECT slug FROM parent3_categories WHERE parent2_title IN (SELECT slug FROM parent2_categories WHERE parent1_title=?))))",
            (slug,))

        conn.commit()

        print("Veri başarıyla silindi.")
    except sqlite3.IntegrityError as e:
        print("Veri silme işlemi sırasında bir hata oluştu:", e)


# # Silmek istediğiniz slug değeri
# slug_degeri = "/karavan-motokaravan"
#
# # Silme işlemini çağırma
# delete_categories_by_slug(slug_degeri)