from app.database import db_connection

class Caretaker:
    def __init__(self, id, name, password, area):
        self.id = id
        self.name = name
        self.password = password
        self.area = area

def view_caretakers():
    conn = db_connection()
    cur = conn.cursor()
    cur.execute('''
        SELECT c.id, c.name, c.password, a.name as area 
        FROM caretakers c 
        JOIN areas a ON c.area = a.id
    ''')
    db_caretakers = [{'id': id, 'name': name, 'password':password, 'area': area} for id, name, password, area in cur.fetchall()]

    caretakers = []
    for db_caretaker in db_caretakers:
        caretakers.append(Caretaker(db_caretaker['id'], db_caretaker['name'], db_caretaker['password'], db_caretaker['area']))
    conn.close()
    return caretakers

def insert_caretaker(name):
    conn = db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO caretakers (name) VALUES (%s) ON CONFLICT DO NOTHING', (name,))
    conn.commit()
    cur.close()
    conn.close()

class Pet:
    def __init__(self, id, name, age):
        self.id = id
        self.name = name
        self.age = age

def view_pets():
    conn = db_connection()
    cur = conn.cursor()
    cur.execute("""
                SELECT id, name, age FROM pets
                """)
    db_pets = cur.fetchall()

    pets = []
    for db_pet in db_pets:
        pets.append(Pet(db_pet[0], db_pet[1], db_pet[2]))
    conn.close()
    return pets

def insert_pet(name, age):
    conn = db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO pets (name, age) VALUES (%s, %s) ON CONFLICT DO NOTHING', (name, age))
    conn.commit()
    cur.close()
    conn.close()
