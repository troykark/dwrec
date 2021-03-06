import sys, pygame, random, colors, math
pygame.init()
### ADDING A Comment 
size = width, height = 800,600
world = width, height = 3400,2000
clock = pygame.time.Clock()
color_elevation = {0:colors.blue4, 1: colors.blue8, 2:colors.blue9, 3:colors.green8, 4:colors.green8,
                   5:colors.green8, 6: colors.green8, 7: colors.green8,8:colors.green8,
                   9:colors.green8, 10:colors.green8, 11:colors.green8,
                   12:colors.yellow8, 13:colors.gray8, 14:colors.gray8, 15:colors.white}
screen = pygame.display.set_mode(size)
class Game: 
    def __init__(self, height, width, tile_size):
        self.runningstate = "WorldMap"
        self.grid   = Grid(height, width, tile_size)
        self.player = Player(self.grid)
        self.updateGrid = False

class Tile:
    '''
    Display information for the the tiles of he map screen.  Does not contain
    gameplay information just information required to correctly display info.
    '''
    def __init__(self, location, color, elevation=0, elevation_ceil =15):
        self.location = location
        self.color = color_elevation[elevation]
        self.elevation = elevation
        self.elevation_ceil = elevation_ceil
    def get_loc(self):
        return self.location
    def get_col(self):
        return self.color
    def set_col(self, colorset):
        self.color = colorset
    def change_elevation(self, delta):
        if self.elevation + delta <= self.elevation_ceil and self.elevation +delta >= 0:
            self.elevation += delta
            self.color = color_elevation[self.elevation]
    def blocked(self):
        if (grid.get_height()-grid.get_tile_size() > self.location[0] > 0)and (grid.get_width() -grid.get_tile_size() > self.location[1] > 0) and self.elevation < 3:
            return True
        else:
            return False
class Grid:
    '''
    Generic grid class based off row, col.  Has a generator to return all cells.
    Also can divide grid by tile squares.  Primarily used for the display object.
    '''
    def __init__(self, height, width, tile_size):
        self.height = height
        self.width = width
        self.tile_size = tile_size
        self.cells = []
        for row in range(0, self.height, tile_size):
            self.cells.append([])
            for col in range(0, self.width, tile_size):
                self.cells[row/tile_size].append((Tile((row,col),colors.black)))
               
    def tilegen(self):
        """
        Yields every cell in the self.cells lsit
        """
        for row in self.cells:
            for col in row:
                yield col
    def watergen(self):
        """
        Yields water tiles
        """
        for row in self.cells:
            for col in row:
                if col.elevation <  3:
                    yield col
    def get_tile_size(self):
        '''
        Returns tile size
        '''
        return int(self.tile_size)
    def get_height(self):
        return self.height
    def get_width(self):
        return self.width
            
    def get_tile(self, row, col):
        '''
        Returns a specific tile
        '''
        return self.cells[int(row/self.tile_size)][int(col/self.tile_size)]
    def get_neighbors(self, row, col, style=4):
        '''
        Return a list of the neighbors of the tile.  Either four, or eight.
        '''
        ans = []
        x = self.tile_size
        if style == 4:
            if row > 0:
                ans.append((row - x, col))
            if row < self.height - x:
                ans.append((row + x, col))
            if col > 0:
                ans.append((row, col - x))
            if col < self.width - x:
                ans.append((row, col + x))
        if style == 8:
            if row > 0:
                ans.append((row - x, col))
            if row < self.height - x:
                ans.append((row + x, col))
            if col > 0:
                ans.append((row, col - x))
            if col < self.width - x:
                ans.append((row, col + x))
            if (row > 0) and (col > 0):
                ans.append((row - x, col - x))
            if (row > 0) and (col < self.width - x):
                ans.append((row - x, col + x))
            if (row < self.height - x) and (col > 0):
                ans.append((row + x, col - x))
            if (row < self.height - x) and (col < self.width - x):
                ans.append((row + x, col + x))
        
        return ans
              

def bump_elvt(row, col, change):
    '''
    initial building block of map gen
    '''
    game.grid.get_tile(row,col).change_elevation(random.randint(2,3)*change)
    for tile in game.grid.get_neighbors(row,col,8):
        game.grid.get_tile(tile[0], tile[1]).change_elevation(1*change)    
        #game.grid.get_tile(tile[0], tile[1]).change_elevation(random.randint(-1,1))
    for tile in game.grid.get_neighbors(row,col,4):
        
        #game.grid.get_tile(tile[0], tile[1]).change_elevation(random.randint(0,1))
        game.grid.get_tile(tile[0], tile[1]).change_elevation(1*change)
def elevation_random_walk(seeds):
    for island in seeds:
        walks = random.randint(5, 200)
        temploc = (island.get_loc()[0],island.get_loc()[1])
       
        for walk in range(walks):
            if random.choice([0,1,1,1]):
                bump_elvt(temploc[0],temploc[1],1)
            else:
                bump_elvt(temploc[0],temploc[1],-3)  
            temploc = random.choice(game.grid.get_neighbors(temploc[0],temploc[1],8))
            
def animate_water(grid, time, mod):
    if time % mod == 0:
        for x in grid.watergen():
            rand = random.random() 
            if  rand > .96:
                x.set_col(colors.blue8)
            elif rand >.85:
                x.set_col(colors.blue6)
            elif rand > .75:
                x.set_col(colors.blue7)

class Player:
    '''
    Display information for the the tiles of he map screen.  Does not contain
    gameplay information just information required to correctly display info.
    '''
    def __init__(self, gridobject):
        self.location = x, y = (size[0]/2), (size[1]/2)
        self.currentCell = gridobject.cells[self.location[0]/gridobject.get_tile_size()][self.location[1]/gridobject.get_tile_size()]
        self.gridobject = gridobject
    def updateCurrentCell(self):
        self.currentCell = self.gridobject.cells[self.location[0]/self.gridobject.get_tile_size()][self.location[1]/self.gridobject.get_tile_size()]
    def updateLocation(self, vector, gameObj):
        self.location = self.location[0] + (vector[0] * self.gridobject.get_tile_size()), self.location[1] + (vector[1] * self.gridobject.get_tile_size()) 
        gameObj.updateGrid = True   
        self.updateCurrentCell()



#grid = Grid(int(world[0]), world[1],20)
#player = Player(grid)
game = Game(int(world[0]), world[1],20)

seed = random.sample([x for x in game.grid.tilegen()],random.randint(5, 200))
time = 0


elevation_random_walk(seed)
print game.player.location, game.player.currentCell.get_loc()

while 1:
    clock.tick(30)
    game.player.updateCurrentCell
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN and game.runningstate == "WorldMap":
            if event.key == pygame.K_UP:
                game.player.updateLocation((0, -1), game)
            if event.key == pygame.K_DOWN:
                game.player.updateLocation((0, 1), game)
            if event.key == pygame.K_LEFT:
                game.player.updateLocation((-1, 0), game)      
            if event.key == pygame.K_RIGHT:
                game.player.updateLocation((1,0), game)
            if event.key == pygame.K_RIGHT and event.key == pygame.K_DOWN:
                game.player.updateLocation((1, 1), game)
            if event.key == pygame.K_ESCAPE: 
                game.runningstate = "Menu"
        elif event.type == pygame.KEYDOWN and game.runningstate == "Menu":
            if event.key == pygame.K_ESCAPE: 
                game.runningstate = "WorldMap"        
    #screen.fill(BLACK)
    #calculations for current screen

    cellminx = (game.player.location[0] - size[0]/2)
    cellmaxx = (game.player.location[0] + size[0]/2)
    cellminy = (game.player.location[1] - size[1]/2)
    cellmaxy = (game.player.location[1] + size[1]/2)  
    xoffset  = (game.player.location[0] - size[0]/2)
    yoffset  = (game.player.location[1] - size[1]/2)
    if(game.runningstate == "WorldMap"): 
        if(game.updateGrid == True):
            for cell in game.grid.tilegen():
                    
                if((cellminx <= cell.get_loc()[0] <= cellmaxx) and (cellminy <= cell.get_loc()[1] <= cellmaxy)):
                    pygame.draw.rect(screen, cell.get_col(), [cell.get_loc()[0] - xoffset, cell.get_loc()[1] - yoffset,
                                                    game.grid.get_tile_size(),
                                                    game.grid.get_tile_size()],
                                    0)
            game.updateGrid = False
        #animate_water(game.grid, time, 15)     
        pygame.draw.rect(screen, colors.red4, [game.player.location[0] - xoffset, game.player.location[1] - yoffset,
                                            game.grid.get_tile_size(), 
                                            game.grid.get_tile_size()],
                                            0) 
    if(game.runningstate == "Menu"):
            pygame.draw.rect(screen, colors.black, [100,100,300,300],
                                        0) 
            pygame.draw.rect(screen, colors.white, [102,102,296,296],
                                        4) 
    pygame.display.flip() 
    time +=1
    
    