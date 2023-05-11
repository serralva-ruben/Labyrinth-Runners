from game_mech import GameMech
from server_skeleton import SkeletonServer


def main():
    gm = GameMech()
    gm.add_player('jose', 1, 1, 100)
    skeleton = SkeletonServer(gm)
    skeleton.run()

main()
