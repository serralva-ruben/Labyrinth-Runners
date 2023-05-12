from game_mech import GameMech
from server_skeleton import SkeletonServer



#Starts the server calling gm and skeleton classes with the port + address he connects 
def main():
    gm = GameMech(20,20)
    skeleton = SkeletonServer(gm)
    skeleton.run()
main()
