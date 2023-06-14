# Seção de Importações
from game_mech import GameMech
from server_skeleton import SkeletonServer


# Função que cria uma instância GameMech, cria uma instância SkeletonServer com a instância anterior como parâmetro e
# executa o servidor.
def main():
    # Cria uma instância da classe GameMech com tamanho de tabuleiro 30x30 quadrículas
    gm = GameMech(31, 31)
    # Cria uma instância da classe SkeletonServer, passando a instância GameMech como parâmetro
    skeleton = SkeletonServer(gm)
    # Inicia o servidor
    skeleton.run()


if __name__ == "__main__":
    main()
