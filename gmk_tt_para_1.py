from joblib import Parallel, delayed
from easyAI import AI_Player, Negamax, TranspositionTable
from gomoku_2 import Gomoku
from pdb import set_trace

DIR = "/data/home/frankf/code_1/GMK_TT/"


def get_pm(moves):
    game = Gomoku([AI_Player(Negamax(1)), AI_Player(Negamax(1))], moves=moves)
    next_move = game.possible_moves()
    nml = [moves + [x] for x in next_move]
    return nml


def get_pm2(moves):
    nml = get_pm(moves)
    rst = []
    for mv in nml:
        rst.extend(get_pm(mv))
    return rst


def tt_s(idx, mv_i):
    table = TranspositionTable()
    ai_1 = AI_Player(Negamax(3, tt=table))
    ai_2 = AI_Player(Negamax(3, tt=table))
    game = Gomoku([ai_1, ai_2], moves=mv_i)
    game.play(verbose=False)
    table.to_file(f"{DIR}tt_{idx}.data")


def tt_para():
    pm_2 = get_pm2(['H8', 'I7', 'G7', 'I9'])
    Parallel(n_jobs=-1, verbose=10)(delayed(tt_s)(i, mv) for i, mv in enumerate(pm_2))


if __name__ == '__main__':
    tt_para()
