import pandas as pd
from joblib import Parallel, delayed
from easyAI import AI_Player, Negamax
from gomoku_2 import Gomoku
from pdb import set_trace

DIR = "/data/home/frankf/code_1/GMK_TT/"


def tt_entry(moves):
    return "-".join(sorted(moves[0::2])) + '_' + "-".join(sorted(moves[1::2]))


def get_pm(moves):
    game = Gomoku([AI_Player(Negamax(1)), AI_Player(Negamax(1))], moves=moves)
    next_move = game.possible_moves()
    nml = [moves + [x] for x in next_move]
    return nml


def n_moves(moves, n):
    if n == 0:
        return moves
    else:
        nml = get_pm(moves)
        n -= 1
        while n > 0:
            rst = []
            for mv in nml:
                rst.extend(get_pm(mv))
            nml = rst
            n -= 1
        return nml


def n_moves_df(moves, n):
    mvs = n_moves(moves, n)
    mvs_str = [tt_entry(x) for x in mvs]
    mvs_df = pd.DataFrame({'moves': mvs, 'str': mvs_str}).drop_duplicates('str')
    return mvs_df


def n_moves_para():
    mvs_i = []
    mvs_v, mvs_d = n_moves(['H8', 'H7'], 4), n_moves(['H8', 'I7'], 4)
    mvs = mvs_v + mvs_d
    mvs_str = [tt_entry(x) for x in mvs]
    mvs_df = pd.DataFrame({'moves': mvs, 'str': mvs_str}).drop_duplicates('str')
    rst = Parallel(n_jobs=-1, verbose=10)(delayed(n_moves_df)(mv, 4) for mv in mvs_df['moves'])
    rst = pd.concat(rst).drop_duplicates('str').reset_index(drop=True)
    set_trace()


if __name__ == '__main__':
    n_moves_para()
