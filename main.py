import pygame
import player
import wall
import game_mechanics
import random
from maze import MazeGenerator


# ---------------------
# The grid now is built based on the number of squares in x and y.
# This allows us to associate the size of the space to a matrix or to a dictionary
# that will keep data about each position in the environment.
# Moreover, we now can control the movement of the objects.
class Game(object):
    def __init__(self, x_nr_sq:int = 20, y_nr_sq:int = 20, grid_size:int  = 20):
        self.x_max = x_nr_sq
        self.y_max = y_nr_sq
        self.width, self.height = x_nr_sq * grid_size, y_nr_sq * grid_size
        self.screen = pygame.display.set_mode((self.width, self.height))
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
        # Atenção: O Game deveria pedir dimensões do jogo ao GameMech e
        # não o contrário. Portanto, GameMech deverá ser gerado fora do
        # Game.
        self.gm = game_mechanics.GameMech(self.x_max, self.y_max)
        pygame.display.update()


    # Drawing a square grid
    def draw_grid(self, colour:tuple):

        for x in range(0, self.x_max):
            pygame.draw.line(self.screen, colour, (x * self.grid_size,0), ( x * self.grid_size, self.height))
        for y in range(0,self.y_max):
            pygame.draw.line(self.screen, colour, (0, y * self.grid_size), (self.width, y * self.grid_size))

    def create_players(self,size:int) -> None:
        #self.players = pygame.sprite.Group()
        self.players = pygame.sprite.LayeredDirty()
        # Atenção, os jogadores têm de ser criados pelo GameMech e só depois
        # gerados aqui pelo Game
        #self.playerA = player.Player(0, 1,1,size,self.players)
        #self.playerB = player.Player(1, 2,2,size,self.players)
        #self.players.add(self.playerA)
        #self.players.add(self.playerB)

    def create_walls(self, wall_size: int):
        # Create Wall (sprites) around world
        self.walls = pygame.sprite.Group()

        # Initialize grid with walls
        grid = [[1 for i in range(self.y_max)] for i in range(self.x_max)]

        ##generate grid for maze
        maze = MazeGenerator(self.x_max,self.y_max,grid)
        maze.generate_maze()
        grid = maze.grid


        # Convert grid to walls
        for x in range(self.x_max):
            for y in range(self.y_max):
                if grid[x][y] == 1:
                    w = wall.Wall(x, y, wall_size, self.walls)
                    self.walls.add(w)

    def run(self):
        #Create Sprites
        self.create_walls(self.grid_size)
        self.walls.draw(self.screen)
        self.create_players(self.grid_size)
        end = False
        while end == False:
            dt = self.clock.tick(10)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    end = True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    end = True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_m:
                    self.playerB.moveto(1,1)
            self.players.update(self, self.gm)
            #self.walls.update(dt / 1000.)
            #self.screen.fill((200,200,200))
            rects = self.players.draw(self.screen)
            #self.walls.draw(self.screen)
            #pygame.display.flip()
            self.draw_grid(self.black)
            pygame.display.update(rects)
            self.players.clear(self.screen,self.background)

        return


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    w = 31
    h = 31
    pygame.init()
    gm = Game(w, h,20)
    gm.run()

