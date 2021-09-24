import pandas as pd
from joblib import Parallel, delayed
from easyAI import AI_Player, Negamax, TranspositionTable
from gomoku_2 import Gomoku
from pdb import set_trace

DIR = "/data/home/frankf/code_1/GMK_TT/"


def tt_s(depth, mv_i):
    table = TranspositionTable()
    table.from_file(f"{DIR}gtt_1.data")
    ai_1 = AI_Player(Negamax(depth, tt=table))
    ai_2 = AI_Player(Negamax(depth, tt=table))
    game = Gomoku([ai_1, ai_2], moves=mv_i.tolist())
    game.play(nmoves=1, verbose=False)
    rst = {key: value for key, value in table.d.items() if value['depth'] == depth}
    return rst


def tt_para(depth):
    mvs_df = pd.read_parquet(f"{DIR}mvs.pqt")
    tt_g = Parallel(n_jobs=-1, verbose=10)(delayed(tt_s)(depth, mv) for mv in mvs_df['moves'])
    dic_tt = {}
    for tt in tt_g:
        for key, value in tt.items():
            dic_tt[key] = value
    table = TranspositionTable(own_dict=dic_tt)
    table.to_file(f"{DIR}gtt.data")


if __name__ == '__main__':
    tt_para(4)
