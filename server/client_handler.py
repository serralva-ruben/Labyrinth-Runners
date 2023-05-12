import pickle
import threading
import const
from game_mech import GameMech

class ClientHandler:

    def __init__(self, gm_obj: GameMech):
        self.gm = gm_obj
        self.lock = threading.Lock()

    def process_x_max(self, s_c):
        """
        Envia o valor da coordenada x máxima do tabuleiro de jogo para o cliente.
        :param s_c: Um objeto 'socket' que representa a conexão do cliente.
        """
        # pedir ao gm o tamanho do jogo
        x_max = self.gm.x_max
        print(x_max)
        # enviar a mensagem com esse valor
        s_c.send(x_max.to_bytes(const.N_BYTES, byteorder="big", signed=True))

    def process_y_max(self, s_c):
        """
        Envia o valor da coordenada y máxima do tabuleiro de jogo para o cliente.
        :param s_c: Um objeto 'socket' que representa a conexão do cliente.
        """
        # pedir ao gm o tamanho do jogo
        y_max = self.gm.y_max
        print(y_max)
        # enviar a mensagem com esse valor
        s_c.send(y_max.to_bytes(const.N_BYTES, byteorder="big", signed=True))
    
    def get_players(self, s_c):
        """
        Envia a lista de jogadores para o cliente
        :param s_c: Um objeto 'socket' que representa a conexão do cliente.
        """
        players = self.gm.get_players()
        data = pickle.dumps(players)

        # Envia o comprimento do fluxo de bytes para o cliente
        length_bytes = len(data).to_bytes(4, byteorder='big')
        s_c.sendall(length_bytes)

        # Envia os bytes para o cliente
        s_c.sendall(data)
    
    def get_nr_players(self, s_c):
        """
        Envia o número de jogadores para o cliente.
        :param s_c: Um objeto 'socket' que representa a conexão do cliente.
        """
        # pedir ao gm o nr de players
        nr_players = self.gm.get_nr_players()
        s_c.send(nr_players.to_bytes(const.N_BYTES, byteorder="big", signed=True))
    
    def get_obstacles(self, s_c):
        """
        Envia a lista de obstáculos para o cliente.
        :param s_c: Um objeto 'socket' que representa a conexão do cliente.
        """
        # pedir ao gm o nr de players
        obstacles = self.gm.get_obstacles()
        # print(f"walls: {obstacles}")
        data = pickle.dumps(obstacles)
        # enviar o comprimento da data
        length_bytes = len(data).to_bytes(4, byteorder='big')
        s_c.sendall(length_bytes)
        # enviar a data
        s_c.sendall(data)
    
    def get_nr_obstacles(self, s_c):
        """
        Envia o número de obstáculos para o cliente.
        :param s_c: Um objeto 'socket' que representa a conexão do cliente.
        """
        # pedir ao gm o nr de players
        nr_obstacles = self.gm.get_nr_obstacles()
        s_c.send(nr_obstacles.to_bytes(const.N_BYTES, byteorder="big", signed=True))

    def new_player(self, s_c, msg):
        """
        Adiciona um novo jogador ao jogo.
        :param s_c: Um objeto 'socket' que representa a conexão do cliente.
        :param msg: Uma mensagem contendo informações sobre o novo jogador.
        """
        name = msg[2:4]
        nr_player = self.gm.add_player(name, 1, 1, 100)
        s_c.send(nr_player.to_bytes(const.N_BYTES, byteorder="big", signed=True))

    def execute(self, s_c, msg):
        """
        Executa um movimento para um jogador.
        :param s_c: Um objeto 'socket' que representa a conexão do cliente.
        :param msg: Uma mensagem contendo informações sobre o movimento a ser executado.
        """
        move = int(msg[1])
        types = ""
        if msg[2] == "p":
            types = "player"
        number = int(msg[3])
        pos = self.gm.execute(move, types, number)
        print(f"The new position is : {pos}")
        data = pickle.dumps(pos)
        # Send the serialized data with a sentinel value
        s_c.sendall(data + b"<END>")
    
    def handle_client(self, socket_client, address):
        print(f"Cliente conectado: Player ID {address}", flush=True)

        try:
            while True:
                received_data = socket_client.recv(const.BUFFER_SIZE)
                if not received_data:
                    break

                msg = received_data.decode(const.STRING_ENCODING)
                print(f"Mensagem recebida: {msg}", flush=True)

                if len(msg) > 0:
                    if msg == const.X_MAX:
                        with self.lock:
                            self.process_x_max(socket_client)
                    elif msg == const.Y_MAX:
                        with self.lock:
                            self.process_y_max(socket_client)
                    elif msg == const.get_Players:
                        with self.lock:
                            self.get_players(socket_client)
                    elif msg == const.get_nr_Players:
                        with self.lock:
                            self.get_nr_players(socket_client)
                    elif msg == const.get_Obstacles:
                        with self.lock:
                            self.get_obstacles(socket_client)
                    elif msg == const.get_nr_Obstacles:
                        with self.lock:
                            self.get_nr_obstacles(socket_client)
                    elif msg[0] == const.execute:
                        with self.lock:
                            self.execute(socket_client, msg)
                    elif msg[0:2] == const.new_Player:
                        with self.lock:
                            self.new_player(socket_client, msg)
                    elif msg == const.END:
                        break

        except Exception as e:
            print(f"Erro ao lidar com o cliente: {e}", flush=True)

        # Limpeza de recursos e desconexão do cliente
        socket_client.close()
        print(f"Cliente desconectado: Player ID {address}", flush=True)