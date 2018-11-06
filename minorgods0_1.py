import sys, pygame, random, colors, math
pygame.init()

size = width, height = 1000,700

BLACK = ( 0, 0, 0)
WHITE = (255, 255, 255)
BLUE =  (0, 0, 255)
GREEN = (0, 255, 0)
RED =   (255, 0, 0)
BROWN = (139, 69, 19)
YELLOW = (255, 255, 0)
clock = pygame.time.Clock()
color_elevation = {0:colors.blue4, 1: colors.blue8, 2:colors.blue9, 3:colors.yellow8, 4:colors.yellow6,
                   5:colors.green9, 6: colors.green8, 7: colors.green7,8:colors.green6,
                   9:colors.green5, 10:colors.green4, 11:colors.green4,
                   12:colors.gray4, 13:colors.gray6, 14:colors.gray8, 15:colors.white}
screen = pygame.display.set_mode(size)

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
                self.cells[row/tile_size].append((Tile((row,col),BLACK)))
               
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
    grid.get_tile(row,col).change_elevation(random.randint(2,3)*change)
    for tile in grid.get_neighbors(row,col,8):
        grid.get_tile(tile[0], tile[1]).change_elevation(1*change)    
        #grid.get_tile(tile[0], tile[1]).change_elevation(random.randint(-1,1))
    for tile in grid.get_neighbors(row,col,4):
        
        #grid.get_tile(tile[0], tile[1]).change_elevation(random.randint(0,1))
        grid.get_tile(tile[0], tile[1]).change_elevation(1*change)
def elevation_random_walk(seeds):
    for island in seeds:
        walks = random.randint(5, 200)
        temploc = (island.get_loc()[0],island.get_loc()[1])
       
        for walk in range(walks):
            if random.choice([0,1,1,1]):
                bump_elvt(temploc[0],temploc[1],1)
            else:
                bump_elvt(temploc[0],temploc[1],-3)   
            temploc = random.choice(grid.get_neighbors(temploc[0],temploc[1],8))
            
def animate_water(grid, time):
    if time % 3 == 0:
        for x in grid.watergen():
            rand = random.random() 
            if  rand > .96:
                x.set_col(colors.blue8)
            elif rand >.85:
                x.set_col(colors.blue6)
            elif rand > .75:
                x.set_col(colors.blue7)

class Port:
    def __init__ (self, location):
        self. location = location
    def get_location(self):
        return self.location

class Boat:
    def __init__(self, location, vector = [0,0], image = "boat.bmp", heading = 135, ai = False):
        self.loc = location
        self.destinations = []
        self.heading = heading
        self.vect = vector
        self.pyimage = pygame.image.load(image)
        self.pyimage.set_colorkey((255,255,255))
        self.rect = self.pyimage.get_rect()
        self.rect.move(self.loc)
        self.ai = ai
    def move(self, vect):
        self.get_vector()

        if not grid.get_tile(self.loc[0] + self.vect[0], self.loc[1] +self.vect[1]).blocked():
            self.vect = [0,0]    
        self.loc[0] += self.vect[0]
        self.loc[1] += self.vect[1]
        self.rect.move(self.loc)
        self.get_vector()
    def get_loc(self):
        return self.loc
    def get_vect(self):
        return self.vect
    def get_vector(self):
        self.vect = [math.sin(math.radians(self.heading)), math.cos(math.radians(self.heading))]
    def get_destination(self):
        return self.destinations[0]
    def add_destination(self, port):
        self.destinations.append(port)
    def boat_ai(self, tile):
        
        if self.ai != False:
             pass
        if self.ai == "simpletravel":
            self.get_vector()
            if not grid.get_tile((self.loc[0] + self.vect[0]), (self.loc[1] +self.vect[1])).blocked():
                self.heading += 15
            elif not grid.get_tile((self.loc[0] + self.vect[0]*20) , (self.loc[1] +self.vect[1]*20)).blocked():
                self.heading += 10
            elif not grid.get_tile((self.loc[0] + self.vect[0]*30) , (self.loc[1] +self.vect[1]*30)).blocked():
                self.heading += 7
            else:
                print [self.get_destination().get_location().get_loc()[0] - self.loc[0],self.get_destination().get_location().get_loc()[1] - self.loc[1]]
  #              dest_vect =  [self.get_destination().get_location().get_loc[0] - self.loc[0],self.get_destination().get_location.get_loc()[1] - self.loc[1]]
                pass
    
def populate_boats(num, boats):
    for x in range(num):
        blocation = [random.randint(1,grid.get_height() -grid.get_tile_size()), random.randint(1, grid.get_width()-grid.get_tile_size())]
        while not grid.get_tile(blocation[0], blocation[1]).blocked():
            blocation = [random.randint(1, grid.get_height()-grid.get_tile_size()), random.randint(1,grid.get_width()-grid.get_tile_size())]

        boats.append(Boat(blocation, heading = random.randint(0, 360), ai = 'simpletravel'))
    return boats            

def populate_ports(num, ports):
    for x in range(num):
        found = False
        while not found:
            ptile = random.choice([x for x in grid.tilegen()])
            if not ptile.blocked():
                for x in grid.get_neighbors(ptile.get_loc()[0],ptile.get_loc()[1],4):
                    if grid.get_tile(x[0],x[1]).blocked():
                        ports.append(Port(ptile))
                        ptile.set_col(RED)
                        found = True

    return ports    





####################SEEDS and SHIP and PORT BUILDIN###########################    
aboat = Boat([100,100])
bboat = Boat([150,150], heading = 100, ai = 'simpletravel')
##boat = pygame.image.load("boat.bmp")
##boat.set_colorkey((255,255,255))
##boatrect = boat.get_rect()



grid = Grid(int(size[0]-size[0]*0.24), size[1],10)
seed = random.sample([x for x in grid.tilegen()],10)
time = 0
#boats = [aboat, bboat]
#boats = [bboat]
boats = []
ports = []
for island in seed:
    pass
elevation_random_walk(seed)
boats = populate_boats(10, boats)
ports = populate_ports(4, ports)

for b in boats:
    b.add_destination(random.choice(ports))




###################MAIN LOOP#####################
while 1:
    clock.tick(1000)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
          
        elif event.type == pygame.KEYDOWN:
##            if event.key == pygame.K_UP:
##                boatrect = boatrect.move([0,-1])
##            if event.key == pygame.K_DOWN:
##                boatrect = boatrect.move([0,1])
            if event.key == pygame.K_LEFT:
                boats[0].heading += 3
                
            if event.key == pygame.K_RIGHT:
                boats[0].heading -= 3
                
    screen.fill(BLACK)
            
    for cell in grid.tilegen():
            
        

        pygame.draw.rect(screen, cell.get_col(), [cell.get_loc()[0], cell.get_loc()[1],
                                        grid.get_tile_size(),
                                        grid.get_tile_size()],
                        0)

    
    #animate_water(grid, time)
    if time%5 == 0:
        for boat in boats:
            boat.boat_ai(grid.get_tile(int(boat.loc[0]), int(boat.loc[1])))
            boat.move(boat.vect)
            
            pygame.draw.lines(screen, (255, 255, 255), False, 
                      [(boat.get_loc()[0], boat.get_loc()[1]), ((boat.get_vect()[0]*12) + boat.get_loc()[0],
                                    (boat.get_vect()[1]*12)+boat.get_loc()[1])], 2)
            screen.blit(boat.pyimage, boat.loc)
            
    else:
        for boat in boats:
            pygame.draw.lines(screen, (255, 255, 255), False, 
                      [(boat.get_loc()[0], boat.get_loc()[1]), ((boat.get_vect()[0]*12) + boat.get_loc()[0],
                                    (boat.get_vect()[1]*12)+boat.get_loc()[1])], 2)
            screen.blit(boat.pyimage, boat.loc)
        pygame.draw.lines(screen, (255, 255, 255), False,
                      [(875, 100), ((boats[0].vect[0]*60) + 875,
                                    (boats[0].vect[1]*60)+100)], 2)
#    screen.blit(boat, boatrect)
    pygame.draw.lines(screen, (255, 255, 255), False,
                      [(875, 100), ((boats[0].vect[0]*60) + 875,
                                    (boats[0].vect[1]*60)+100)], 2)
    pygame.display.flip()
    time +=1

            
    
