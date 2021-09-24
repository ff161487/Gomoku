import os
from joblib import Parallel, delayed
from easyAI import TranspositionTable
from pdb import set_trace

DIR = "/data/home/frankf/code_1/GMK_TT/"


def ext_s(idx):
    if os.path.exists(f"{DIR}tt_{idx}.data"):
        table = TranspositionTable()
        table.from_file(f"{DIR}tt_{idx}.data")
        return table.d


def gtt(n):
    tt_g = Parallel(n_jobs=1, verbose=10)(delayed(ext_s)(idx) for idx in range(n))
    rst = {}
    for tt in tt_g:
        if tt is not None:
            for key, value in tt.items():
                rst[key] = value
    table_g = TranspositionTable(own_dict=rst)
    table_g.to_file(f"{DIR}gtt_1.data")


if __name__ == '__main__':
    gtt(129)