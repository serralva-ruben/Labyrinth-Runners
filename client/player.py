# Seção de Importações
import pygame
import client_stub
import const as co
import os


class Player(pygame.sprite.DirtySprite):
    def __init__(self, number: int, name: str, pos_x: int, pos_y: int, sq_size: int, *groups):
        """
        Construtor da classe 'Player'
        :param number: O número do jogador
        :param name: O nome do jogador
        :param pos_x: A posição x do jogador na grelha
        :param pos_y: A posição y do jogador na grelha
        :param sq_size: O tamanho do quadrado na grelha
        :param groups: Os grupos aos quais o jogador pertence
        """
        super().__init__(*groups)
        self.number = number
        self.name = name
        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_dir = os.path.join(current_dir, 'pictures', 'player.gif')
        self.image = pygame.image.load(image_dir)
        initial_size = self.image.get_size()
        self.sq_size = sq_size
        size_rate = sq_size / initial_size[0]
        self.new_size = (int(self.image.get_size()[0] * size_rate), int(self.image.get_size()[1] * size_rate))
        self.image = pygame.transform.scale(self.image, self.new_size)
        self.rect = pygame.rect.Rect((pos_x * sq_size, pos_y * sq_size), self.image.get_size())

    def get_size(self):
        """
        Obtém o tamanho do jogador.
        :return: O tamanho do jogador
        """
        return self.new_size
    
    def get_nr(self):
        return self.number

    def moveto(self, new_x: int, new_y: int):
        """
        Move o jogador para a posição especificada.
        :param new_x:
        :param new_y:
        :return:
        """
        self.rect.x = new_x * self.sq_size
        self.rect.y = new_y * self.sq_size
        # Keep visible
        self.dirty = 1

    def update(self, stub: client_stub.StubClient):
        """
        Atualiza a posição do jogador.
        :param stub: O stub do cliente para se comunicar com o servidor
        :return: None
        """
        # last = self.rect.copy()
        print("Updating player ", self.name, " with the number ", self.number)
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            pos = stub.execute(co.M_LEFT, "player", self.number)
            if self.rect.x != pos[0]:
                self.rect.x = pos[0] * self.sq_size
        if key[pygame.K_RIGHT]:
            pos = stub.execute(co.M_RIGHT, "player", self.number)
            if self.rect.x != pos[0]:
                self.rect.x = pos[0] * self.sq_size
        if key[pygame.K_UP]:
            pos = stub.execute(co.M_UP, "player", self.number)
            if self.rect.y != pos[1]:
                self.rect.y = pos[1] * self.sq_size
        if key[pygame.K_DOWN]:
            pos = stub.execute(co.M_DOWN, "player", self.number)
            if self.rect.y != pos[1]:
                self.rect.y = pos[1] * self.sq_size

        # Keep visible
        self.dirty = 1
