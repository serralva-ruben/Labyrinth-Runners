import socket
import logging
from game_mech import GameMech
import const

# Está no lado do servidor: Skeleton to user interface 
# (permite ter informação de como comunicar com o cliente)
class SkeletonServer:

    def __init__(self, gm_obj: GameMech):
        self.gm = gm_obj
        self.s = socket.socket()
        self.s.bind((const.ADDRESS, const.PORT))
        self.s.listen()

    def process_x_max(self, s_c):
        # pedir ao gm o tamanho do jogo
        x_max = self.gm.x_max
        # enviar a mensagem com esse valor
        s_c.send(x_max.to_bytes(const.N_BYTES, byteorder="big", signed=True))

    def process_y_max(self, s_c):
        # pedir ao gm o tamanho do jogo
        y_max = self.gm.y_max
        # enviar a mensagem com esse valor
        s_c.send(y_max.to_bytes(const.N_BYTES, byteorder="big", signed=True))
    
    def get_Players(self, s_c):
        # pedir ao gm os players
        players = self.gm.get_players()
        s_c.send(players.to_bytes(const.N_BYTES, byteorder="big", signed=True))
        return
    
    def get_nr_Players(self, s_c):
        # pedir ao gm o nr de players
        nr_players = self.gm.get_nr_players()
        s_c.send(nr_players.to_bytes(const.N_BYTES, byteorder="big", signed=True))
        return
    
    def get_obstacles(self, s_c):
        # pedir ao gm o nr de players
        obstacles = self.gm.get_obstacles()
        s_c.send(obstacles.to_bytes(const.N_BYTES, byteorder="big", signed=True))
        return
    
    def get_nr_obstacles(self, s_c):
        # pedir ao gm o nr de players
        nr_obstacles = self.gm.get_nr_obstacles()
        s_c.send(nr_obstacles.to_bytes(const.N_BYTES, byteorder="big", signed=True))
        return

    def run(self):
        logging.info("a escutar na porta " + str(const.PORT))
        socket_client, address = self.s.accept()
        logging.info("o cliente com o endereço " + str(address) + " ligou-se!")

        msg: str = ""
        end = False
        while end == False:
            received_data: bytes = socket_client.recv(const.COMMAND_SIZE)
            msg = received_data.decode(const.STRING_ENCODING)
            #logging.debug("o cliente enviou: \"" + msg + "\"")

            if msg == const.X_MAX:
                self.process_x_max(socket_client)
            elif msg == const.Y_MAX:
                self.process_y_max(socket_client)
            elif msg == const.get_Players :
                self.get_Players(socket_client)
            elif msg == const.get_nr_Players :
                self.get_nr_Players(socket_client)
            elif msg == const.get_Obstacles :
                self.get_obstacles(socket_client)
            elif msg == const.get_nr_Obstacles :
                self.get_nr_obstacles(socket_client)
            elif msg == const.END:
                end = True
        socket_client.close()
        logging.info("o cliente com endereço o " + str(address) + " desligou-se!")

        self.s.close()