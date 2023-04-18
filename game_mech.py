# GameMech
from maze import MazeGenerator
import time
from matplotlib import pyplot as plt

# Defining constants for the moves
M_UP = 0
M_RIGHT = 1
M_DOWN = 2
M_LEFT = 3
TIME_STEP = 7.5

class GameMech :
    def __init__(self, x_max:int= 20, y_max:int = 20) -> None:
        '''
        Create a dictionary where each position will keep the elements that are in each position and
        a dictionary with player information (name, nr. of points, etc.)
        :param x_max:
        :param y_max:
        '''
        self.x_max = x_max
        self.y_max = y_max
        # List of players
        self.players = dict()
        # List of players that changed position. It has the following struture:
        # [previous position, new_position] where the first position is the initial position when the key is created
        self.phanton_players = dict()
        # List of obstacles
        self.obstacles = dict()
        # Number of players and obstacles in the game
        self.nr_players = 0
        self.nr_obstacles = 0
        # Initializing each world's position with a list
        self.world = dict()
        for i in range(x_max):
            for j in range(y_max):
                self.world[(i, j)] = []
        # Add the obstacles to the world
        self.create_world()
        # TEST
        self.counting = 0

    def add_obstacle(self, type:str, x_pos:int, y_pos:int) -> bool:
        '''
        :param name:
        :param x_pos:
        :param y_pos:
        :return:
        '''
        nr_obstacle = self.nr_obstacles
        self.obstacles[nr_obstacle] = [type, (x_pos, y_pos)]
        self.world[(x_pos, y_pos)].append(['obstacle', type, nr_obstacle, (x_pos, y_pos)])
        self.nr_obstacles += 1
        return True
    
    def create_world(self):
        '''
        Define the initial world with the position of the obstacles

        :return:
        '''

        maze = MazeGenerator(self.x_max,self.y_max)
        grid = maze.generate_maze()

        plt.imshow(grid, cmap='gray', interpolation='nearest')
        plt.draw()
        plt.pause(0.0001)
                
        for x in range(self.x_max):
            print(f"{x}  {grid[x]}")
            for y in range(self.y_max):
                if grid[x][y] == 1:
                    self.add_obstacle("wall", y, x)

    def is_obstacle(self,type, x,y):
        for e in self.world[(x,y)]:
            if e[0] == 'obstacle' and e[1]==type:
                return True
        return False

    #
    # Getters
    #
    def get_players(self):
        return self.players

    def get_obstacles(self):
        return self.obstacles

    def get_nr_obstacles(self):
        return self.nr_obstacles

    def get_nr_players(self):
        return self.nr_players

    def remove_player(self, nr_player) -> int:
        if nr_player <= self.nr_players:
            name = self.players[nr_player][0]
            x_pos, y_pos = self.players[nr_player][1][0], self.players[nr_player][1][1]
            self.world[(x_pos, y_pos)].remove(['player',name,nr_player,(x_pos, y_pos)])
            self.players[nr_player]=[]
        return nr_player

    def print_players(self):
        for p in self.players:
            print("Nr. ",p)
            print("Value:",self.players[p])

    #
    # Each player has a specific time.
    #
    def add_player(self,name, x_pos:int, y_pos:int ) -> int:
        '''
        :param name: the name of the player
        :param x_pos:
        :param y_pos:
        :return: return the number of player
        '''
        nr_player = self.nr_players
        #
        # Collect the actual tick and keep it in the player
        # Each player has its own tick because we are using the tick increment
        # in each call is made to the game mechanics. This is something that is
        # going to change in the implementations with sockets where time is the
        # absolute value that comes from the server.
        #
        tick = int(time.time() )

        self.players[nr_player]=[ name, (x_pos, y_pos),tick]
        self.world[(x_pos, y_pos)].append(['player',name, nr_player,(x_pos, y_pos)])
        self.nr_players += 1

        return nr_player

    def execute(self,move: int, type:str, nr_player:int ) -> tuple:
        '''
        Execute the actions. Each new tic, the world execute the actions. The players must ask
        to print the actual world.
        :return:
        '''
        if type == "player":
            name = self.players[nr_player][0]
            pos_x, pos_y = self.players[nr_player][1][0], self.players[nr_player][1][1]
            tick = self.players[nr_player][2]
            if move == M_LEFT:
                # Get the atual position of the player
                # New position
                new_pos_x = pos_x - 1
                new_pos_y = pos_y
                # if there is an obstacle
                if self.is_obstacle('wall', new_pos_x, new_pos_y):
                    new_pos_x = pos_x
            elif move == M_RIGHT:
                # New position
                new_pos_x = pos_x + 1
                new_pos_y = pos_y
                if self.is_obstacle('wall', new_pos_x, new_pos_y):
                    new_pos_x = pos_x
            elif move == M_UP:
                # New position
                new_pos_y = pos_y - 1
                new_pos_x = pos_x
                if self.is_obstacle('wall', new_pos_x, new_pos_y):
                    new_pos_y = pos_y
            elif move == M_DOWN:
                # New position
                new_pos_y = pos_y + 1
                new_pos_x = pos_x
                if self.is_obstacle('wall', new_pos_x, new_pos_y):
                    new_pos_y = pos_y
            # Only after the tick the changes are performed (to coordinate among players)
            next_tick = int(time.time() * TIME_STEP)
            # Test
            #print("Tick:",self.tick)
            #print("Next tick:",next_tick)
            # End test
            if next_tick > tick:
                # Test
                self.counting +=1
                #print(self.counting)
                #print("Tick:",self.tick)
                #print("Next tick:",next_tick)
                tick = next_tick
                # Update world
                self.players[nr_player] =[name, (new_pos_x, new_pos_y), tick]
                # Previous objects in the initial position before phanton moves
                world_pos = self.world[(pos_x, pos_y)]
                # Test
                #print("Removing player in the position ", pos_x, ",", pos_y,":",world_pos)
                #print("Name:",name)
                #print("Nr_player:",nr_player)
                # Removing object player in the previous position
                world_pos.remove(['player',name,nr_player, (pos_x,pos_y)])
                # Update the world with objects remaining in the position
                self.world[(pos_x, pos_y)] = world_pos
                self.world[(new_pos_x, new_pos_y)].append(['player',name,nr_player,(new_pos_x, new_pos_y)])
            else:
                # Revert the changes because there was no movement...
                new_pos_x = pos_x
                new_pos_y = pos_y
            return (new_pos_x, new_pos_y)

    def print_pos(self, x: int, y:int):
        print("(x= ",x,", y=", y, ") =", self.world[(x, y)])


    def print_world(self):
        for i in range(self.x_max):
            for j in range(self.y_max):
                print("(", i, ",", j, ") =", self.world[(i, j)])
