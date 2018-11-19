def importGrid(worldfile):

    with open(worldfile) as readfile:
        worldimport = readfile.read()
    return worldimport

print importGrid('worldtest')

