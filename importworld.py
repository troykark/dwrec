def importGrid(worldfile):

    with open(worldfile) as readfile:
        worldimport = readfile.read()

    return worldimport




worldfile =  importGrid('worldtest')

world = []
for line in (worldfile.split('\n')[:-1]):
    world += [list(line)]
for row in world: 
    for col in row:
        col = int(col)
print world