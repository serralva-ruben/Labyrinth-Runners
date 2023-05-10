import numpy as np
import random


class MazeGenerator:
    def __init__(self, nr_max_x: int, nr_max_y: int):
        self.width = nr_max_x
        self.height = nr_max_y
        self.grid = [[1 for i in range(self.height)] for i in range(self.width)]

    def generate_maze(self):
        # set with all the frontiers
        s = set()
        # random starting point and set it to not wall
        # x, y = (random.randint(1, self.width - 2), random.randint(1, self.height - 2))
        x = 1
        y = 1
        self.grid[x][y] = 0
        # frontiers of current cell
        fs = self.frontier(x, y)
        # add them to the set with all the frontiers
        for f in fs:
            s.add(f)
        # will run while there are frontiers in the set
        while s:
            # chose random frontier and remove it from the set of all frontiers
            x, y = random.choice(tuple(s))
            s.remove((x, y))
            # neighbours of the random frontier
            ns = self.neighbours(x, y)
            # if the random chosen frontier had neighbours
            if ns:
                # chose a random neighbour and connect them
                nx, ny = random.choice(tuple(ns))
                self.connect(x, y, nx, ny)
            fs = self.frontier(x, y)
            for f in fs:
                s.add(f)
        return self.grid
        
    def frontier(self, x, y):
        n = set()
        if 1 <= x < self.width-1 and 1 <= y < self.height - 1:
            if x > 1 and self.is_wall(self.grid[x - 2][y]):
                n.add((x-2, y))
            if x < self.width-3 and self.is_wall(self.grid[x + 2][y]):
                n.add((x+2, y))
            if y > 1 and self.is_wall(self.grid[x][y - 2]):
                n.add((x, y-2))
            if y < self.height-3 and self.is_wall(self.grid[x][y + 2]):
                n.add((x, y+2))
        return n

    def neighbours(self, x, y):
        n = set()
        if 1 <= x < self.width-1 and 1 <= y < self.height - 1:
            if x > 1 and not self.is_wall(self.grid[x - 2][y]):
                n.add((x-2, y))
            if x < self.width-3 and not self.is_wall(self.grid[x + 2][y]):
                n.add((x+2, y))
            if y > 1 and not self.is_wall(self.grid[x][y - 2]):
                n.add((x, y-2))
            if y < self.height-3 and not self.is_wall(self.grid[x][y + 2]):
                n.add((x, y+2))
        return n

    def is_wall(self, cell):
        if cell == 1:
            return True
        elif cell == 0:
            return False
        else:
            return None

    def connect(self, x1, y1, x2, y2):
        x = (x1 + x2) // 2
        y = (y1 + y2) // 2
        self.grid[x1][y1] = 0
        self.grid[x][y] = 0

   
    
