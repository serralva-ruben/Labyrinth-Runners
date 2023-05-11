from game_mech import GameMech
from server_skeleton import SkeletonServer


def main():
    gm = GameMech(20,20)
    skeleton = SkeletonServer(gm)
    skeleton.run()

main()
