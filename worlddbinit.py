import sqlite3, random
conn = sqlite3.connect('.\world.db')
c = conn.cursor()

def createDB():
    c.execute('''CREATE TABLE tile (xcoords, ycoords, elevation, terrain, chunk)''')
def inserttile(xcord, ycord, elevation, terrain, chunk):
    c.execute('INSERT INTO tile (xcoords, ycoords, elevation, terrain, chunk) VALUES ('+ str(xcord) +','+ str(ycord) + ','+ str(elevation) + ',"' + terrain + '",' +  chunk+ ')')
createDB()
for cx in range(0,300):
    for cy in range(0,300):
         inserttile(cx,cy,random.randrange(0,30),random.choice(["mountain","plains","ocean"]),str(1))
for row in c.execute("SELECT * FROM tile"):
    print row
conn.commit()
conn.close()