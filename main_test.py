import pygame
import game_mech
import game


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    pygame.init()
    # Create game mechanics with walls and other stuff
    gmech = game_mech.GameMech(30, 30)

# Add a player (myself)
    nr = gmech.add_player('jose', 1, 1, 100)
    nr = gmech.add_player('joao', 10, 10, 100)

    # Start the visual part and the rest...
    gm = game.Game(gmech, 30)
    gm.run()
