# Constantes
UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3


class GameMech:
    def __init__(self,nr_max_x:int, nr_max_y:int):
        self.world = dict()
        self.players = dict()
        self.walls = dict()
        self.x_max = nr_max_x
        self.y_max = nr_max_y
        for x in range(nr_max_x):
            for y in range(nr_max_y):
                self.world[(x,y)]=[]
                self.players[(x,y)] = []
                self.walls[(x,y)] = []
        # Criar paredes à volta do mundo
        nr_walls = 0
        for x in range(0,self.x_max):
            for y in range(0,self.y_max):
                if x in (0,self.x_max - 1) or y in (0, self.y_max - 1):
                    self.walls[nr_walls]=["wall",(x,y)]
                    self.world[(x,y)].append(["obst","wall",nr_walls])
                    nr_walls += 1
        # Criar jogador
        self.players[0] =["jose",(1,1)]
        self.world[(1,1)].append(["player","jose",0])
        self.players[1] = ["manuel",(2,2)]
        self.world[(2,2)].append(["player","manuel",1])
    # nr_jogador, direcao,
    def execute(self,nr_player:int , direction:int) -> tuple:
        x, y = self.players[nr_player][1][0], self.players[nr_player][1][1]
        #print("initial position:",x,",",y)
        name = self.players[nr_player][0]
        if direction == UP:
            new_x = x
            new_y = y - 1
        elif direction == DOWN:
            new_x = x
            new_y = y + 1
        elif direction == LEFT:
            new_x = x - 1
            new_y = y
        elif direction == RIGHT:
            new_x = x + 1
            new_y = y
        # Alterar o mundo - retirar o jogador em posição anterior
        # e colocá-lo na nova posição
        # Atenção: Há que verificar que a nova posição não é um
        # obstáculo. Se for, o jogador fica na mesma posição.
        self.world[(x,y)].remove(["player",name,nr_player])
        if 0 <= new_x < self.width and 0 <= new_y < self.height:
            self.world[(new_x, new_y)].append(["player", name, nr_player])
        # Alterar o jogador: colocar o jogador na nova posição
        self.players[nr_player] =[name,(new_x,new_y)]
        return (new_x, new_y)

    def print_position(self, x:int ,y:int ):
        print("Position (",x,",",y,"):",self.world[(x,y)])

    def print_world(self):
        for x in range(0,self.x_max):
            for y in range(0,self.y_max):
                print("(",x,",",y,")=",self.world[(x,y)])


# Test
if __name__ == '__main__':
    gm = GameMech(20,20)
    gm.print_world()
    gm.execute(0,LEFT)
    gm.print_position(1,1)
    gm.print_position(0,1)


    #gm.execute(1,UP)