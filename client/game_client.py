# Seção de Importações
import pygame
from wall import Wall
from player import Player
import client_stub


"""
A grelha agora é construída com base no número de quadrados em x e y.
Isso nos permite associar o tamanho do espaço a uma matriz ou a um dicionário
que manterá os dados sobre cada posição no ambiente.
Além disso, agora podemos controlar o movimento dos objetos.
Agora separamos o controlo do ambiente
"""


class GameUI(object):
    def __init__(self, stub: client_stub.StubClient, grid_size: int = 20):
        dim: tuple = stub.dimension_size()
        self.x_max = dim[0]
        self.y_max = dim[1]
        self.stub = stub

        self.player_nr = stub.add_player("Rub")
        
        self.width, self.height = self.x_max * grid_size, self.y_max * grid_size
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Labyrinth Runners")
        self.clock = pygame.time.Clock()
        # Cores RGB
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        # Grid
        self.grid_size = grid_size
        grid_colour = self.black
        # Cria o Fundo
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill(self.white)
        self.screen.blit(self.background, (0, 0))
        self.draw_grid(self.black)

        # Crie uma superfície para esconder tudo fora do raio do jogador
        self.hide_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.hide_surface.fill((255, 255, 255, 255))
        pygame.display.update()

    def draw_grid(self, colour: tuple):
        """
        Desenhe a grelha no ecrã.
        :param colour: A cor das linhas de grelha
        :return: None
        """
        for x in range(0, self.x_max):
            pygame.draw.line(self.screen, colour, (x * self.grid_size, 0), (x * self.grid_size, self.height))
        for y in range(0, self.y_max):
            pygame.draw.line(self.screen, colour, (0, y * self.grid_size), (self.width, y * self.grid_size))

    def set_players(self):
        """
        Coloca os jogadores no ecrã
        :return: None
        """
        self.pl = self.stub.get_players()
        self.players = pygame.sprite.LayeredDirty()
        nr_players = self.stub.get_nr_players()
        for nr in range(nr_players):
            if self.pl[nr] != []:
                p_x, p_y = self.pl[nr][1][0], self.pl[nr][1][1]
                player = Player(nr, self.pl[nr][0], p_x, p_y, self.grid_size, self.players)
                self.players.add(player)

    def draw_darkness(self):
        """
        Obscurece o mapa em redor do jogador
        :return: None
        """
        self.hide_surface.fill((0, 0, 0, 255))
        p = self.stub.get_players()
        for player in p:
            circle_pos = (p[player][1][0] + self.players.sprites()[player].rect.x, p[player][1][1] +
                          self.players.sprites()[player].rect.y)
            pygame.draw.circle(self.hide_surface, (255, 255, 255, 0), circle_pos, p[player][3])
            self.hide_surface.set_clip(None)
        self.screen.blit(self.hide_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)

    def set_walls(self, wall_size: int):
        """
        Desenha as paredes no ecrã
        :param wall_size: Tamanho das paredes
        :return: None
        """
        self.wl = self.stub.get_obstacles()
        # Cria as paredes (sprites) ao redor do mundo
        self.walls = pygame.sprite.Group()
        nr_obstacles = self.stub.get_nr_obstacles()
        for nr in range(nr_obstacles):
            if self.wl[nr]:
                w_x, w_y = self.wl[nr][1][0], self.wl[nr][1][1]
                wall = Wall(w_x, w_y, self.grid_size, self.walls)
                self.walls.add(wall)

    def run(self):
        """
        Inicializa o jogo
        :return: Verdadeiro se o jogo terminou com sucesso, falso caso contrário.
        """
        self.set_walls(self.grid_size)
        self.walls.draw(self.screen)
        self.set_players()
        end = False
        # previous_tick = self.stub.get_tick()

        # O mundo é atualizado constantemente
        world = dict()
        while not end:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # Enviar informação "desconectado"
                    # Se a resposta for ok, então end é verdadeiro
                    end = True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    # Enviar informação "desconectado"
                    # Se a resposta for ok, então end é verdadeiro
                    end = True

            self.walls.draw(self.screen)
            self.players.update(self.stub)
            self.players.draw(self.screen)
            self.draw_grid(self.black)
            self.draw_darkness()
            pygame.display.flip()
            self.players.clear(self.screen, self.background)
            self.screen.fill((255, 255, 255))
        return True
