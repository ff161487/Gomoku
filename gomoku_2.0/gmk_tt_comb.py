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
    rst = {key: value for key, value in table.d.items() if value['depth'] == 3}
    return rst


def gtt():
    tt_g = Parallel(n_jobs=-1, verbose=10)(delayed(ext_s)(idx) for idx in range(106))
    rst = {}
    for tt in tt_g:
        for key, value in tt.items():
            rst[key] = value
    table_g = TranspositionTable(own_dict=rst)
    table_g.to_file(f"{DIR}tt_g.data")


if __name__ == '__main__':
    gtt()