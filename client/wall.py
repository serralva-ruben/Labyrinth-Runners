# Seção de Importações
import pygame
import os


class Wall(pygame.sprite.Sprite):
    def __init__(self, pos_x: int, pos_y: int, w_size: int, *groups):
        """
        Construtor para a classe Wall.
        :param pos_x: A coordenada x da parede
        :param pos_y: A coordenada y da parede
        :param w_size: O tamanho da parede
        :param groups: grupo(s) ao(s) qual(is) este sprite pertence
        """
        super().__init__(*groups)
        # Carrega a imagem da parede e dimensione-a conforme o tamanho da parede
        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_dir = os.path.join(current_dir, 'pictures', 'wall.jpg')
        self.image = pygame.image.load(image_dir)
        initial_size = self.image.get_size()
        size_rate = w_size / initial_size[0]
        self.new_size = (int(self.image.get_size()[0] * size_rate), int(self.image.get_size()[1] * size_rate))
        self.image = pygame.transform.scale(self.image, self.new_size)
        # Cria o retângulo 'sprite' com a posição e tamanho especificados
        self.rect = pygame.rect.Rect((pos_x * w_size, pos_y * w_size), self.image.get_size())

    def get_size(self):
        """
        Retorna o tamanho do 'sprite' Wall.
        :return: O tamanho do 'sprite' da parede
        """
        return self.new_size

    def update(self):
        # TODO document why this method is empty
        pass
