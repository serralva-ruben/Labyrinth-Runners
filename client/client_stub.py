# Seção de Importações
import socket
import const
import pickle


# Stub do lado do cliente: como comunicar com o servidor...
class StubClient:
    def __init__(self):
        self.s: socket = socket.socket()
        self.s.connect((const.ADDRESS, const.PORT))

    def dimension_size(self):
        """
        Envia uma mensagem ao servidor para obter o tamanho das dimensões do jogo e retornar os valores recebidos.
        :return: Valores x_max e y_max recebidos do servidor
        """
        print("getting dimensions")
        msg = const.X_MAX
        self.s.send(msg.encode(const.STRING_ENCODING))
        value = self.s.recv(const.N_BYTES)
        x_max = int.from_bytes(value, byteorder="big", signed=True)
        print(x_max)
        msg = const.Y_MAX
        self.s.send(msg.encode(const.STRING_ENCODING))
        value = self.s.recv(const.N_BYTES)
        y_max = int.from_bytes(value, byteorder="big", signed=True)
        print(y_max)
        return x_max, y_max
    
    def get_players(self):
        """
        Envia uma mensagem ao servidor para obter os jogadores e retorne a lista de jogadores recebidos.
        :return: Lista de jogadores recebida do servidor
        """
        msg = const.get_Players
        self.s.send(msg.encode(const.STRING_ENCODING))
        length_bytes = self.s.recv(4)
        length = int.from_bytes(length_bytes, byteorder='big')
        # Recebe os bytes do servidor
        data_bytes = bytearray()
        print("Received Data Length:", len(data_bytes))  # Imprime o comprimento dos dados recebidos para 'debug'
        print("Received Data:", data_bytes)  # Imprime os dados recebidos para 'debug'
        while len(data_bytes) < length:
            chunk = self.s.recv(min(4096, length - len(data_bytes)))
            if not chunk:
                break
            data_bytes.extend(chunk)
        # Desserializa os dados recebidos e retorna-os
        players = pickle.loads(data_bytes)
        print(players)
        return players
        
    def get_nr_players(self):
        """
        Envia uma mensagem para o servidor para obter o número de jogadores e retornar o valor recebido.
        :return: Número de jogadores recebidos do servidor
        """
        msg = const.get_nr_Players
        self.s.send(msg.encode(const.STRING_ENCODING))
        value = self.s.recv(const.N_BYTES)
        nr_players = int.from_bytes(value, byteorder="big", signed=True)
        return nr_players
    
    def get_obstacles(self):
        """
        Envia uma mensagem ao servidor para obter os obstáculos e retornar a lista de obstáculos recebidos.
        :return: Lista de obstáculos recebida do servidor
        """
        msg = const.get_Obstacles
        self.s.send(msg.encode(const.STRING_ENCODING))

        # Recebe o comprimento do fluxo de bytes do servidor
        length_bytes = self.s.recv(4)
        length = int.from_bytes(length_bytes, byteorder='big')

        # Recebe os bytes do servidor
        data_bytes = b''
        while len(data_bytes) < length:
            chunk = self.s.recv(length - len(data_bytes))
            if not chunk:
                break
            data_bytes += chunk
        # Desserializa os dados recebidos e retorna-os
        obstacles = pickle.loads(data_bytes)
        print(obstacles)
        return obstacles
    
    def get_nr_obstacles(self):
        """
        Envia uma mensagem ao servidor para obter o número de obstáculos e retornar o valor recebido.
        :return: Número de obstáculos recebidos do servidor
        """
        msg = const.get_nr_Obstacles
        self.s.send(msg.encode(const.STRING_ENCODING))
        value = self.s.recv(const.N_BYTES)
        nr_obstacles = int.from_bytes(value, byteorder="big", signed=True)
        return nr_obstacles
    
    def get_finish(self):
        msg = const.get_finish
        self.s.send(msg.encode(const.STRING_ENCODING))
        data = self.s.recv(const.N_BYTES)
        finish = pickle.loads(data)  # Deserializing the received data
        return finish
    
    def get_game_status(self):
        msg = const.get_status
        self.s.send(msg.encode(const.STRING_ENCODING))
        data = self.s.recv(const.N_BYTES)
        finish = pickle.loads(data)  # Deserializing the received data
        return finish

    def execute(self, move: int, types: str, nr_player: int):
        """
        Executa uma jogada para o jogo
        :param move: Um número inteiro representando o movimento
        :param types: Uma 'string' que é do jogador ou obstáculos.
        :param nr_player: Um inteiro representando o número do jogador
        :return: Um tuplo que representa a nova posição do jogador ou dos obstáculos.
        """
        msg = const.execute
        msg += str(move)
        if types == "player":
            msg += "p"
        self.s.send(msg.encode(const.STRING_ENCODING))

        # Recebe os dados serializados
        received_data = bytearray()
        while True:
            chunk = self.s.recv(4096)
            if not chunk:
                break
            received_data.extend(chunk)
            print("Received Chunk:", chunk)  # Imprime o chunk recebido para 'debug'
            if b"<END>" in received_data:
                break

        if len(received_data) > 0:
            # Remove o valor sentinela dos dados recebidos
            received_data = received_data.replace(b"<END>", b"")
            # Desserializa os dados
            decoded_data = pickle.loads(received_data)
            print(decoded_data)
            if decoded_data is not None:
                return decoded_data
        # Retorna uma posição padrão se nenhum dado for recebido ou se decoded_data for None
        return 0, 0
    
    def add_player(self, name) -> int:
        """
        Adiciona um jogador ao jogo.
        :param name: Uma ‘string’ representando o nome do jogador.
        :return: Um inteiro representando o número do jogador.
        """
        msg = const.new_Player
        if len(name) < 3:
            msg += name
        print(msg)
        print(msg[0:2])
        self.s.send(msg.encode(const.STRING_ENCODING))
        value = self.s.recv(const.N_BYTES)
        nr_player = int.from_bytes(value, byteorder="big", signed=True)
        return nr_player
