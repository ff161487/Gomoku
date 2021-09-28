import numpy as np
from pickle import dump
from joblib import Parallel, delayed
from easyAI import TranspositionTable
from pdb import set_trace

DIR = "/data/home/frankf/code_1/GMK_TT/"


def str_pos(x, kind):
    if kind == 'to_str':
        rst = chr(65 + x[1]) + str(15 - x[0])
    elif kind == 'to_pos':
        rst = (15 - int(x[1:]), ord(x[0]) - 65)
    return rst


def obs_s(key, value):
    mv_k, mv_w = tuple(key.split('_'))
    mv_k, mv_w = mv_k.split('-'), mv_w.split('-')
    n_mvs = len(mv_k) + len(mv_w)
    last = 2 * (n_mvs % 2) - 1
    board = np.zeros((15, 15), dtype='int8')
    for black_stone in mv_k:
        board[str_pos(black_stone, 'to_pos')] = 1
    for white_stone in mv_w:
        board[str_pos(white_stone, 'to_pos')] = -1
    board = last * board
    return float(value['value']), board


def gen_train():
    table = TranspositionTable()
    table.from_file(f"{DIR}gtt.data")
    rst = Parallel(n_jobs=-1, batch_size=1000, verbose=10)(
        delayed(obs_s)(key, value) for key, value in table.d.items())
    n_tt = len(table.d)
    x_tr, y_tr = np.empty((n_tt, 15, 15), dtype='int8'), np.empty(n_tt, dtype='float64')
    for i in range(n_tt):
        y_tr[i], x_tr[i] = rst[i]
    tr = (y_tr, x_tr)
    with open(f"{DIR}train.data", 'wb') as f:
        dump(tr, f)


if __name__ == '__main__':
    gen_train()
