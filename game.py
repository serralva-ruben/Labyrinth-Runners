import pygame
from wall import Wall
from player import Player
import game_mech


# ---------------------
# The grid now is built based on the number of squares in x and y.
# This allows us to associate the size of the space to a matrix or to a dictionary
# that will keep data about each position in the environment.
# Moreover, we now can control the movement of the objects.
# We now separate the control of the environment

class Game(object):
    def __init__(self, gm: game_mech.GameMech, grid_size:int  = 20):
        self.x_max = gm.x_max
        self.y_max = gm.y_max
        self.gm = gm
        self.width, self.height = self.x_max * grid_size, self.y_max * grid_size
        self.screen = pygame.display.set_mode((self.width,self.height))
        pygame.display.set_caption("first game")
        self.clock = pygame.time.Clock()
        # RGB colours
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        # Grid
        self.grid_size = grid_size
        grid_colour = self.black
        # Create The Backgound
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill(self.white)
        self.screen.blit(self.background,(0,0))
        self.draw_grid(self.black)
        pygame.display.update()


    # Drawing a square grid
    def draw_grid(self, colour:tuple):
        for x in range(0, self.x_max):
            pygame.draw.line(self.screen, colour, (x * self.grid_size,0), ( x * self.grid_size, self.height))
        for y in range(0,self.y_max):
            pygame.draw.line(self.screen, colour, (0, y * self.grid_size), (self.width, y * self.grid_size))



    def set_players(self):
        self.pl = self.gm.get_players()
        self.players = pygame.sprite.LayeredDirty()
        nr_players = self.gm.get_nr_players()
        # Test
        print("Game2, Nr. of players:", nr_players)
        print("Game2, Players:", self.pl)
        for nr in range(nr_players):
            if self.pl[nr] != []:
                    # Test
                    print("Game2, Player added:", nr)
                    p_x, p_y  = self.pl[nr][1][0], self.pl[nr][1][1]
                    player = Player(nr, self.pl[nr][0], p_x, p_y, self.grid_size, self.players)
                    self.players.add(player)


    def set_walls(self, wall_size:int):
        self.wl = self.gm.get_obstacles()
        # Create Wall (sprites) around world
        self.walls = pygame.sprite.Group()
        nr_obstacles = self.gm.get_nr_obstacles()
        for nr in range(nr_obstacles):
            if self.wl[nr] != []:
                w_x, w_y = self.wl[nr][1][0], self.wl[nr][1][1]
                wall = Wall(w_x, w_y, self.grid_size, self.walls)
                self.walls.add(wall)

    def run(self):
        #Create Sprites
        self.set_walls(self.grid_size)
        self.walls.draw(self.screen)
        self.set_players()
        end = False
        # previous_tick = self.gm.get_tick()
        # World is updated every time
        world = dict()
        while end == False:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # send information "disconnected"
                    # if answer is ok, then end is true
                    end = True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    # send information "disconnected"
                    # if answer is ok, them end is true
                    end = True
            self.walls.update()
            self.players.update(self.gm)
            rects = self.players.draw(self.screen)
            self.draw_grid(self.black)
            pygame.display.update(rects)
            self.players.clear(self.screen,self.background)
        return True
