import pygame
import client_stub

###################################################
# CLASS JOGADOR                                   #
#  self.numeber - number os players               #
#  self.name - nome do jogador                    #
#  self.picture - gif with the player             #
###################################################


# Defining constants for the moves
M_UP = 0
M_RIGHT = 1
M_DOWN = 2
M_LEFT = 3


class Player(pygame.sprite.DirtySprite):
    def __init__(self, number: int, name: str, pos_x: int, pos_y: int, sq_size: int, *groups):
        super().__init__(*groups)
        self.number = number
        self.name = name
        self.image = pygame.image.load('client/pictures/player.gif')
        initial_size = self.image.get_size()
        self.sq_size = sq_size
        size_rate = sq_size / initial_size[0]
        self.new_size = (int(self.image.get_size()[0] * size_rate), int(self.image.get_size()[1] * size_rate))
        self.image = pygame.transform.scale(self.image, self.new_size)
        self.rect = pygame.rect.Rect((pos_x * sq_size, pos_y * sq_size), self.image.get_size())

    def get_size(self):
        return self.new_size

    def moveto(self, new_x: int, new_y: int):
        self.rect.x = new_x * self.sq_size
        self.rect.y = new_y * self.sq_size
        # Keep visible
        self.dirty = 1

    def update(self, stub: client_stub.StubClient):
        # last = self.rect.copy()
        print("Updating player ", self.name, " with the number ", self.number)
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            pos = stub.execute(M_LEFT, "player", self.number)
            if self.rect.x != pos[0]:
                self.rect.x = pos[0] * self.sq_size
        if key[pygame.K_RIGHT]:
            pos = stub.execute(M_RIGHT, "player", self.number)
            if self.rect.x != pos[0]:
                self.rect.x = pos[0] * self.sq_size
        if key[pygame.K_UP]:
            pos = stub.execute(M_UP, "player", self.number)
            if self.rect.y != pos[1]:
                self.rect.y = pos[1] * self.sq_size
        if key[pygame.K_DOWN]:
            pos = stub.execute(M_DOWN, "player", self.number)
            if self.rect.y != pos[1]:
                self.rect.y = pos[1] * self.sq_size

        # Keep visible
        self.dirty = 1
