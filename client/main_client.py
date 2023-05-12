# Seção de Importações
import pygame
from client_stub import StubClient
from game_client import GameUI


# Inicialização do Pygame, cria uma instância StubClient e uma instância GameUI e executa a ‘interface’ do jogador.
def main():
    # Inicializa o Pygame
    pygame.init()
    # Cria uma instância nova da class StubClient
    stub = StubClient()
    # Cria uma instância da classe GameUI, passando o stub como parâmetro
    ui = GameUI(stub)
    # Inicia a User Interface
    ui.run()


if __name__ == "__main__":
    main()
