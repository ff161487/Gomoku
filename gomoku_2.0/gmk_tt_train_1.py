from joblib import Parallel, delayed
from easyAI import AI_Player, Negamax, TranspositionTable
from gomoku_2 import Gomoku
from pdb import set_trace

DIR = "/data/home/frankf/code_1/GMK_TT/"


def check_pm():
    mv = ['H8', 'H7', 'I7', 'K5', 'G9', 'F10', 'I8']
    game = Gomoku([AI_Player(Negamax(1)), AI_Player(Negamax(1))], moves=mv)
    next_move = game.possible_moves()
    set_trace()


def check_bug():
    table = TranspositionTable()
    table.from_file(f"{DIR}gtt.data")
    Parallel(n_jobs=1, verbose=10)(delayed(check_pm)(key, value) for key, value in table.d.items())


if __name__ == '__main__':
    check_pm()