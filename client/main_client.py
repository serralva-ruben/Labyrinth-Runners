import pygame
from client_stub import StubClient
from game_client import GameUI



#Starts the client calling gm and skeleton classes with the port + address he connects 
def main():
    pygame.init()
    stub = StubClient()
    ui = GameUI(stub)
    ui.run()

main()
