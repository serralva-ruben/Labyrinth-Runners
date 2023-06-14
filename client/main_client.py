# Seção de Importações
import pygame
from client_stub import StubClient
from game_client import GameUI


# Inicialização do Pygame, cria uma instância StubClient e uma instância GameUI e executa a ‘interface’ do jogador.
def main():
    player_name = input("Please enter your name: ")
    # Inicializa o Pygame
    pygame.init()
    pygame.display.set_mode((800, 600), pygame.RESIZABLE)
    # Cria uma instância nova da class StubClient
    stub = StubClient()
    player_id = stub.add_player(player_name)
    # Cria uma instância da classe GameUI, passando o stub como parâmetro
    ui = GameUI(stub, player_id,player_name)
    # Inicia a User Interface
    ui.run()


if __name__ == "__main__":
    main()
