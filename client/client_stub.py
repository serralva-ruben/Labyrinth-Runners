import socket
import const
import pickle
import struct

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
        msg = const.get_Players
        self.s.send(msg.encode(const.STRING_ENCODING))
        length_bytes = self.s.recv(4)
        length = int.from_bytes(length_bytes, byteorder='big')
        # Receive the bytes from the server
        data_bytes = bytearray()
        while len(data_bytes) < length:
            chunk = self.s.recv(min(4096, length - len(data_bytes)))
            if not chunk:
                break
            data_bytes.extend(chunk)
        players = pickle.loads(data_bytes)
        return players
        
    def get_nr_players(self):
        msg = const.get_nr_Players
        self.s.send(msg.encode(const.STRING_ENCODING))
        value = self.s.recv(const.N_BYTES)
        nr_players = int.from_bytes(value, byteorder="big", signed=True)
        return nr_players
    
    def get_obstacles(self):
        msg = const.get_Obstacles
        self.s.send(msg.encode(const.STRING_ENCODING))

        # Receive the length of the byte stream from the server
        length_bytes = self.s.recv(4)
        length = int.from_bytes(length_bytes, byteorder='big')

        # Receive the bytes from the server
        data_bytes = b''
        while len(data_bytes) < length:
            chunk = self.s.recv(length - len(data_bytes))
            if not chunk:
                break
            data_bytes += chunk

        obstacles = pickle.loads(data_bytes)
        return obstacles
    
    def get_nr_obstacles(self):
        msg = const.get_nr_Obstacles
        self.s.send(msg.encode(const.STRING_ENCODING))
        value = self.s.recv(const.N_BYTES)
        nr_obstacles = int.from_bytes(value, byteorder="big", signed=True)
        return nr_obstacles

    def execute(self, move: int, types: str, nr_player: int):
        msg = const.execute
        msg += str(move)
        if types == "player":
            msg += "p"
        if nr_player <= 9:
            msg += str(nr_player)
        self.s.send(msg.encode(const.STRING_ENCODING))

        # Receive the serialized data
        received_data = bytearray()
        while True:
            chunk = self.s.recv(4096)
            if not chunk:
                break
            received_data.extend(chunk)
            print("Received Chunk:", chunk)  # Print the received chunk for debugging

        print("Received Data Length:", len(received_data))  # Print the received data length for debugging
        print("Received Data:", received_data)  # Print the received data for debugging

        if len(received_data) > 0:
            # Deserialize the data
            decoded_data = pickle.loads(received_data)
            print(decoded_data)
            return decoded_data
        else:
            # Return a default position if no data received
            return (0, 0)
    
    def addPlayer(self, name) -> int:
        msg = const.new_Player
        if len(name)<3:
            msg += name
        print(msg)
        print(msg[0:2])
        self.s.send(msg.encode(const.STRING_ENCODING))
        value = self.s.recv(const.N_BYTES)
        nr_player = int.from_bytes(value, byteorder="big", signed=True)
        return nr_player