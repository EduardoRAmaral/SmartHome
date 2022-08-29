import sqlite3
import os.path

# Create db instance
connection = sqlite3.connect('database.db')

# Create tables
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
schema_path = os.path.join(BASE_DIR, 'schema.sql')

with open(schema_path) as f:
    connection.executescript(f.read())

cur = connection.cursor()

# Table Rooms
insert_rooms = "INSERT INTO rooms (room_name) VALUES "
insert_rooms += "('room_a'), "
insert_rooms += "('room_b'), "
insert_rooms += "('room_c'), "
insert_rooms += "('room_d'), "
insert_rooms += "('room_e')"
cur.execute(insert_rooms)

# Table configs
insert_configs = "INSERT INTO configs (id) VALUES (1)"
cur.execute(insert_configs)

connection.commit()
connection.close()
