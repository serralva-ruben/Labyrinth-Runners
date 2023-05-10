import socket
from typing import Union
import const


# Stub do lado do cliente: como comunicar com o servidor...
class StubClient:
    def __init__(self):
        self.s: socket = socket.socket()
        self.s.connect((const.ADDRESS, const.PORT))

    def dimension_size(self):
        msg = const.X_MAX
        self.s.send(msg.encode(const.STRING_ENCODING))
        value = self.s.recv(const.N_BYTES)
        x_max = int.from_bytes(value, byteorder="big", signed=True)

        msg = const.Y_MAX
        self.s.send(msg.encode(const.STRING_ENCODING))
        value = self.s.recv(const.N_BYTES)
        y_max = int.from_bytes(value, byteorder="big", signed=True)
        return x_max, y_max
    
    def get_players(self):
        msg = "get Players"
        self.s.send(msg.encode(const.STRING_ENCODING))
        value = self.s.recv(const.N_BYTES)
        players = ""
        return players
        
    def get_nr_players(self):
        msg = "get nr Players"
        self.s.send(msg.encode(const.STRING_ENCODING))
        value = self.s.recv(const.N_BYTES)
        nr_players = int.from_bytes(value, byteorder="big", signed=True)
        return nr_players
    
    def get_obstacles(self):
        msg = "get obstacles"
        self.s.send(msg.encode(const.STRING_ENCODING))
        value = self.s.recv(const.N_BYTES)
        obstacles = ""
        return obstacles
    
    def get_nr_obstacles(self):
        msg = "get nr obstacles"
        self.s.send(msg.encode(const.STRING_ENCODING))
        value = self.s.recv(const.N_BYTES)
        nr_obstacles = int.from_bytes(value, byteorder="big", signed=True)
        return nr_obstacles
