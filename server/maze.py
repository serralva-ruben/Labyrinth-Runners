import random


class MazeGenerator:
    def __init__(self, nr_max_x: int, nr_max_y: int):
        """
        Construtor da classe "MazeGenerator"
        :param nr_max_x: A largura máxima do labirinto
        :param nr_max_y: A altura máxima do labirinto
        """
        self.width = nr_max_x
        self.height = nr_max_y
        # Cria uma matriz 2D de paredes com as dimensões de largura x altura
        self.grid = [[1 for i in range(self.height)] for i in range(self.width)]

    def generate_maze(self):
        """
        Gera o labirinto usando o algoritmo backtracker recursivo.
        :return: Uma matriz 2D representando o labirinto
        """
        # Define todas as fronteiras
        s = set()
        # Ponto de partida aleatório e definir-lo para não ser uma parede
        # x, y = (random.randint(1, self.width - 2), random.randint(1, self.height - 2))
        x = 1
        y = 1
        self.grid[x][y] = 0
        # Fronteiras da célula atual
        fs = self.frontier(x, y)
        # Adicionar-los ao conjunto com todas as fronteiras
        for f in fs:
            s.add(f)
        # Irá correr enquanto houver fronteiras no conjunto
        while s:
            # Escolhe uma fronteira aleatória e remove-a do conjunto de todas as fronteiras
            x, y = random.choice(tuple(s))
            s.remove((x, y))
            # Vizinhança da fronteira aleatória
            ns = self.neighbours(x, y)
            # Se a fronteira escolhida aleatoriamente tiver vizinhos
            if ns:
                # Escolha de um vizinho aleatório e conexão
                nx, ny = random.choice(tuple(ns))
                self.connect(x, y, nx, ny)
            fs = self.frontier(x, y)
            for f in fs:
                s.add(f)
        return self.grid
        
    def frontier(self, x, y):
        """
        Encontra todas as fronteiras da célula dada.
        :param x: Coordenada x da célula
        :param y: Coordenada y da célula
        :return: Um conjunto contendo todas as fronteiras da célula
        """
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
        """
        Encontrar toda a vizinhança de uma dada célula
        :param x: Coordenada x da célula
        :param y: Coordenada x da célula
        :return: Um conjunto contendo todos os vizinhos da célula
        """
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
        """
        Determina se uma célula é parede ou não
        :param cell: Valor da célula a ser verificada
        :return: V se a célula for uma parede (1), F se não for uma parede (0) ou None se o valor for inválido
        """
        if cell == 1:
            return True
        elif cell == 0:
            return False
        else:
            return None

    def connect(self, x1, y1, x2, y2):
        """
        Conecta duas células juntas, removendo a parede entre elas.
        :param x1: A coordenada x da primeira célula
        :param y1: A coordenada y da primeira célula
        :param x2: A coordenada x da segunda célula
        :param y2: A coordenada Y da segunda célula
        :return: None
        """
        x = (x1 + x2) // 2
        y = (y1 + y2) // 2
        self.grid[x1][y1] = 0
        self.grid[x][y] = 0
