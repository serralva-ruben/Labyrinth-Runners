# Seção de Importações
import random
from maze import MazeGenerator
import time
import const as co


class GameMech:
    def __init__(self, x_max: int = 20, y_max: int = 20) -> None:
        """
        Cria um dicionário onde cada posição manterá os elementos que estão em cada posição e um dicionário com
        informações do jogador (nome, nr. de pontos, etc.)
        :param x_max: Recebe um valor 'int' no eixo x que determinará o comprimento do tabuleiro nesse mesmo eixo.
        :param y_max: Recebe um valor 'int' no eixo y que determinará o comprimento do tabuleiro nesse mesmo eixo.
        """
        self.x_max = x_max
        self.y_max = y_max
        # Lista de Jogadores
        self.players = dict()
        # Lista de jogadores que mudaram de posição. Possui a seguinte estrutura:
        # [posição anterior, nova_posição] onde a primeira posição é a posição inicial quando a chave é criada
        self.phantom_players = dict()
        # Lista de Obstáculos
        self.obstacles = dict()
        # Número de jogadores e obstáculos no jogo
        self.nr_players = 0
        self.nr_obstacles = 0
        # Inicialização de cada posição no mundo com uma lista
        self.world = dict()
        for i in range(x_max):
            for j in range(y_max):
                self.world[(i, j)] = []
        # Adição de obstáculos no mundo
        self.create_world()
        # Teste
        self.counting = 0
        self.game_over = False
        self.winner = None

    def add_obstacle(self, types: str, x_pos: int, y_pos: int) -> bool:
        """
        Função que adiciona um novo obstáculo no mundo
        :param types: uma 'string' representando o tipo de obstáculo adicionado
        :param x_pos: um valor 'int' representando a coordenada x da localização do obstáculo
        :param y_pos: um valor 'int' representando a coordenada y da localização do obstáculo
        :return: Retorna um valor booleano indicando se o obstáculo foi adicionado com sucesso
        """
        nr_obstacle = self.nr_obstacles
        self.obstacles[nr_obstacle] = [types, (x_pos, y_pos)]
        self.world[(x_pos, y_pos)].append(['obstacle', types, nr_obstacle, (x_pos, y_pos)])
        self.nr_obstacles += 1
        return True
    
    def add_obstacle_powerup(self, types: str, x_pos: int, y_pos: int, image_path: str) -> bool:
        """
        Function that adds a new obstacle to the world
        :param types: a 'str' representing the type of obstacle being added
        :param x_pos: an 'int' value representing the x-coordinate of the obstacle's location
        :param y_pos: an 'int' value representing the y-coordinate of the obstacle's location
        :param image_path: a 'str' representing the file path or reference to the obstacle's image
        :return: Returns a boolean value indicating whether the obstacle was successfully added
        """
        nr_obstacle = self.nr_obstacles
        self.obstacles[nr_obstacle] = [types, (x_pos, y_pos), image_path]
        self.world[(x_pos, y_pos)].append(['obstacle', types, nr_obstacle, (x_pos, y_pos), image_path])
        self.nr_obstacles += 1
        return True
        
    def create_world(self):
        """
        Define o mundo inicial com a posição dos obstáculos
        :return: None
        """
        maze = MazeGenerator(self.x_max, self.y_max)
        grid = maze.generate_maze()

        last_row = []
        last_column = []
                
        for x in range(self.x_max):
            for y in range(self.y_max):
                if grid[x][y] == 1:
                    self.add_obstacle("wall", y, x)
                if x == self.x_max - 2:  # Last row
                    last_row.append((y, x))
                if y == self.y_max - 2:  # Last column
                    last_column.append((y, x))

        # Choose a random cell from the last row or column that isn't a wall
        potential_finish_cells = last_row + last_column
        potential_finish_cells = [cell for cell in potential_finish_cells if not self.is_obstacle("wall", *cell)]
        
        self.finish = random.choice(potential_finish_cells) if potential_finish_cells else None

        print(self.finish)

    def is_obstacle(self, types, x, y):
        """
        Verifica se há um obstáculo de um determinado tipo numa determinada posição
        :param types:
        :param x: Valor de x a verificar
        :param y: Valor de y a verificar
        :return: Verdadeiro se houver um obstáculo do tipo dado na posição dada, Falso caso contrário
        """
        for e in self.world[(x, y)]:
            if e[0] == 'obstacle' and e[1] == types:
                return True
        return False

    # Getters
    def get_players(self):
        """
        Retorna a lista de jogadores
        :return: Lista de jogadores
        """
        return self.players

    def get_obstacles(self):
        """
        Retorna a lista de obstáculos
        :return: lista de obstáculos
        """
        return self.obstacles

    def get_nr_obstacles(self):
        """
        Retorna o número de obstáculos no mundo
        :return: número de obstáculos
        """
        return self.nr_obstacles

    def get_nr_players(self):
        """
        Retorna o número de jogadores no mundo
        :return: número de jogadores no mundo
        """
        return self.nr_players

    def remove_player(self, nr_player) -> int:
        """
        Remove um jogador do mundo conforme o seu índice.
        :param nr_player: Índice do jogador a remover
        :return: Índice do jogador removido
        """
        if nr_player in self.players:
            name = self.players[nr_player][0]
            x_pos, y_pos = self.players[nr_player][1][0], self.players[nr_player][1][1]
            self.world[(x_pos, y_pos)].remove(['player', name, nr_player, (x_pos, y_pos)])
            self.players.pop(nr_player)
        return nr_player

    def print_players(self):
        """
        Imprime as informações de todos os jogadores
        :return: None
        """
        for p in self.players:
            print("Nr. ", p)
            print("Value:", self.players[p])

    # Cada jogador tem um tempo específico.
    def add_player(self, name, x_pos: int, y_pos: int, radius: int) -> int:
        """
        Adiciona um jogador ao jogo com o nome, posição e raio fornecidos
        :param name: Nome do Jogador
        :param x_pos: a coordenada x da posição do jogador
        :param y_pos: a coordenada y da posição do jogador
        :param radius: o raio do jogador
        :return: o número do jogador
        """
        nr_player = self.nr_players

        # Coleta o tick real e mantenha-o no jogador. Cada jogador tem o seu próprio tick porque usamos o
        # incremento de tick em cada chamada é feita a mecânica do jogo.
        # Isso é vai mudar nas implementações com ‘sockets’ onde o tempo é o valor absoluto que vem do servidor.

        tick = int(time.time())

        self.players[nr_player] = [name, (x_pos, y_pos), tick, radius]
        self.world[(x_pos, y_pos)].append(['player', name, nr_player, (x_pos, y_pos)])
        self.nr_players += 1
        return nr_player

    def execute(self, move: int, types: str, nr_player: int) -> tuple:
        """
        Esta função executa um movimento de um jogador no jogo, atualizando a posição do jogador no mundo
         e retornando as novas coordenadas de posição.
        :param move: Movimento a ser executado
        :param types: O tipo de objeto a ser movido (por exemplo, jogador, item, etc.)
        :param nr_player: O número do jogador a ser movido
        :return: um tuplo com as novas coordenadas de posição x e y do jogador
        """
        print(f"The movement is going to be: {move}")
        print(f"The nr of the player is {nr_player}")
        print(f" the players are: {self.players}")
        print(self.get_players())

        if types == "player":
            print(f"if nr player in players : {(nr_player in self.players)}")
            print(f"nr_player type: {type(nr_player)}, value: {nr_player}")
            print(f"players keys: {self.players.keys()}")

            if nr_player in self.players:
                name = self.players[nr_player][0]
                pos_x, pos_y = self.players[nr_player][1][0], self.players[nr_player][1][1]
                tick = self.players[nr_player][2]
                print(f"tick : {tick}")
                radius = self.players[nr_player][3]

                new_pos_x = pos_x
                new_pos_y = pos_y

                if self.players[nr_player][1] == self.finish:
                    self.game_over = True
                    self.winner = nr_player
                    return new_pos_x, new_pos_y                 

                # Movimenta o Jogador à Esquerda
                if move == co.M_LEFT:
                    # Adquire a posição atual do jogador
                    # Nova posição do jogador
                    new_pos_x = pos_x - 1
                    new_pos_y = pos_y
                    # Se houver um obstáculo
                    print(f"is obstacle: {self.is_obstacle('wall',new_pos_x,new_pos_y)}")
                    if self.is_obstacle('wall', new_pos_x, new_pos_y):
                        new_pos_x = pos_x

                # Movimenta o Jogador à Direita
                elif move == co.M_RIGHT:
                    # Nova Posição
                    new_pos_x = pos_x + 1
                    new_pos_y = pos_y
                    print(f"is obstacle: {self.is_obstacle('wall',new_pos_x,new_pos_y)}")
                    if self.is_obstacle('wall', new_pos_x, new_pos_y):
                        new_pos_x = pos_x

                # Movimenta o Jogador para Cima
                elif move == co.M_UP:
                    # Nova Posição
                    new_pos_y = pos_y - 1
                    new_pos_x = pos_x
                    print(f"is obstacle: {self.is_obstacle('wall',new_pos_x,new_pos_y)}")
                    if self.is_obstacle('wall', new_pos_x, new_pos_y):
                        new_pos_y = pos_y

                # Movimenta o Jogador para Baixo
                elif move == co.M_DOWN:
                    # Nova Posição
                    new_pos_y = pos_y + 1
                    new_pos_x = pos_x
                    print(f"is obstacle: {self.is_obstacle('wall',new_pos_x,new_pos_y)}")
                    if self.is_obstacle('wall', new_pos_x, new_pos_y):
                        new_pos_y = pos_y

                # Somente após o tick as alterações são realizadas (para coordenar entre os jogadores)
                next_tick = int(time.time() * co.TIME_STEP)
                print(f"next tick: {next_tick}")
                if next_tick > tick:
                    tick = next_tick
                    # Update world
                    self.players[nr_player] = [name, (new_pos_x, new_pos_y), tick, radius]
                    # Previous objects in the initial position before phantom moves
                    world_pos = self.world[(pos_x, pos_y)]
                    # Removing object player in the previous position
                    world_pos.remove(['player', name, nr_player, (pos_x, pos_y)])
                    # Update the world with objects remaining in the position
                    self.world[(pos_x, pos_y)] = world_pos
                    self.world[(new_pos_x, new_pos_y)].append(['player', name, nr_player, (new_pos_x, new_pos_y)])
                else:
                    # Reverte as alterações, pois não houve movimentação...
                    new_pos_x = pos_x
                    new_pos_y = pos_y
                print(f"{new_pos_x}, {new_pos_y}")
                return new_pos_x, new_pos_y
                
    def print_pos(self, x: int, y: int):
        """
        Imprime o conteúdo de uma posição específica no mundo
        :param x: Coordenada x da posição
        :param y: Coordenada y da posição
        :return: None
        """
        print("(x= ", x, ", y=", y, ") =", self.world[(x, y)])

    def print_world(self):
        """
        Imprime o mundo inteiro, com o respetivo conteúdo de cada posição.
        :return: None
        """
        for i in range(self.x_max):
            for j in range(self.y_max):
                print("(", i, ",", j, ") =", self.world[(i, j)])

    def get_finish(self):
        return self.finish

    def get_game_status(self):
        return self.game_over, self.winner
