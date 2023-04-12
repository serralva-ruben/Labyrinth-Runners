import pygame
# Player 7 is part of the test example 7
# It defines a sprite with size rate

# Constantes
import game_mechanics

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3


class Player(pygame.sprite.DirtySprite):
    def __init__(self, number: int, pos_x:int, pos_y:int, sq_size:int, *groups ):
        super().__init__(*groups)
        self.image = pygame.image.load('intro_ball.gif')
        initial_size = self.image.get_size()
        self.sq_size = sq_size
        size_rate = sq_size / initial_size[0]
        self.new_size = (int(self.image.get_size()[0] * size_rate), int(self.image.get_size()[1] * size_rate))
        self.image = pygame.transform.scale(self.image, self.new_size)
        self.rect = pygame.rect.Rect((pos_x * sq_size, pos_y * sq_size), self.image.get_size())
        self.number = number

    def get_size(self):
        return self.new_size

    def moveto(self,new_x:int, new_y:int):
        self.rect.x = new_x * self.sq_size
        self.rect.y = new_y * self.sq_size
        # Keep visible
        self.dirty = 1

    def update(self, game: object, gm: game_mechanics.GameMech):
        last = self.rect.copy()
        key = pygame.key.get_pressed()

        # Move the player according to the key pressed
        if key[pygame.K_LEFT]:
            self.rect.x -= self.sq_size
        if key[pygame.K_RIGHT]:
            self.rect.x += self.sq_size
        if key[pygame.K_UP]:
            self.rect.y -= self.sq_size
        if key[pygame.K_DOWN]:
            self.rect.y += self.sq_size

        # Check for collisions with walls
        collisions = pygame.sprite.spritecollide(self, game.walls, False)
        if collisions:
            # If there is a collision, revert to the previous position
            self.rect = last

            # Move the player to the edge of the wall they collided with
            for wall in collisions:
                if self.rect.right > wall.rect.left and last.right <= wall.rect.left:
                    self.rect.right = wall.rect.left
                elif self.rect.left < wall.rect.right and last.left >= wall.rect.right:
                    self.rect.left = wall.rect.right
                elif self.rect.bottom > wall.rect.top and last.bottom <= wall.rect.top:
                    self.rect.bottom = wall.rect.top
                elif self.rect.top < wall.rect.bottom and last.top >= wall.rect.bottom:
                    self.rect.top = wall.rect.bottom
        # Keep visible
        self.dirty = 1