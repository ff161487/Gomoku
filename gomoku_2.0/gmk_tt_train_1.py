import numpy as np
import pandas as pd
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


def ext_s(idx):
    table = TranspositionTable()
    table.from_file(f"{DIR}tt_{idx}.data")
    rst = []
    for key, value in table.d.items():
        if value['depth'] == 3:
            # Transform key to list format
            mv_s = key.split('-')
            mv_s.append(value['move'])

            # Compute stone value for current player
            ply_stone = 2 * (len(mv_s) % 2) - 1

            # Make board
            pos_l = [str_pos(x, 'to_pos') for x in mv_s]
            board = np.zeros((15, 15), dtype='int8')
            for i, pos in enumerate(pos_l):
                board[pos] = 1 - 2 * (i % 2)

            # Perform FFT2 on board
            board = np.abs(np.fft.rfft2(board))

            # Append to result list
            rst += [{'Y': value['value'], 'P': ply_stone, 'X': board.flatten()}]

    # Transfer to DataFrame
    rst = pd.DataFrame.from_records(rst)
    return rst


def gen_train():
    tr = Parallel(n_jobs=-1, verbose=10)(delayed(ext_s)(idx) for idx in range(106))
    tr = pd.concat(tr).reset_index(drop=True)

    # From training set dataframe to numpy array
    mat_tr = np.zeros((len(tr), 122))
    mat_tr[:, 0] = tr['Y'].to_numpy()
    mat_tr[:, 1] = tr['P'].to_numpy()
    for i in range(len(tr)):
        mat_tr[i, 2:] = tr.loc[i, 'X']

    # Save training set to local file
    with open(f"{DIR}training.data", 'wb') as f:
        dump(mat_tr, f)


if __name__ == '__main__':
    gen_train()
    # ext_s(0)