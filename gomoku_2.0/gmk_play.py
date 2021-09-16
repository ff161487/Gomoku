from easyAI import AI_Player, Negamax, Human_Player, TranspositionTable
from gomoku_2 import Gomoku
from pdb import set_trace

DIR = "/data/home/frankf/code_1/GMK_TT/"


def play_gomoku():
    # Load transposition table
    table = TranspositionTable()
    table.from_file(f"{DIR}gtt.data")
    set_trace()
    ply_1 = Human_Player()
    ply_2 = AI_Player(Negamax(3, tt=table))
    game = Gomoku([ply_1, ply_2], moves=['H8', 'I7'], show='test')
    game.play()
    set_trace()


if __name__ == '__main__':
    play_gomoku()
