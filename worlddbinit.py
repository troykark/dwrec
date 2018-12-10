import sqlite3
conn = sqlite3.connect('.\world.db')
c = conn.cursor()
#c.execute('''CREATE TABLE tile (xcoords, ycoords, elevation, terrain)''')
c.execute('''INSERT INTO tile (xcoords, ycoords, elevation, terrain) VALUES (2,3,12,"Mountain")''')
for row in c.execute("SELECT * FROM tile"):
    print row
conn.commit()
conn.close()