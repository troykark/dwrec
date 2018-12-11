import sqlite3, random
conn = sqlite3.connect('.\world.db')
c = conn.cursor()
c.execute('''CREATE TABLE tile (xcoords, ycoords, elevation, terrain)''')
c.execute('''INSERT INTO tile (xcoords, ycoords, elevation, terrain) VALUES (2,3,12,"Beach")''')
for cx in range(0,300):
    for cy in range(0,300):
         c.execute('INSERT INTO tile (xcoords, ycoords, elevation, terrain) VALUES ('+ str(cx) +','+ str(cy) + ','+ str(random.random() *10) + ',"null")')
for row in c.execute("SELECT * FROM tile"):
    print row
conn.commit()
conn.close()