import sqlite3
conn = sqlite3.connect('.\world.db')
c = conn.cursor()
c.execute('''
    CREATE TABLE tile (xcoords, ycoords, elevation, terrain)
''')
