import pandas as pd
from joblib import Parallel, delayed
from easyAI import AI_Player, Negamax, TranspositionTable
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


def tt_s(idx, mv_i):
    table = TranspositionTable()
    ai_1 = AI_Player(Negamax(2, tt=table))
    ai_2 = AI_Player(Negamax(2, tt=table))
    game = Gomoku([ai_1, ai_2], moves=mv_i)
    game.play(verbose=False)
    table.to_file(f"{DIR}tt_{idx}.data")


def tt_para():
    mvs_v, mvs_d = n_moves(['H8', 'H7'], 4), n_moves(['H8', 'I7'], 4)
    mvs = mvs_v + mvs_d
    mvs_str = [tt_entry(x) for x in mvs]
    mvs_df = pd.DataFrame({'moves': mvs, 'str': mvs_str}).drop_duplicates('str')
    mvs = mvs_df['moves'].tolist()
    Parallel(n_jobs=-1, verbose=10)(delayed(tt_s)(i, mv) for i, mv in enumerate(mvs))


if __name__ == '__main__':
    tt_para()
