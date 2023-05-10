import pygame
from client_stub import StubClient
from game_client import GameUI


def main():
    pygame.init()
    stub = StubClient()
    ui = GameUI(stub)
    ui.run()


main()
