from joblib import Parallel, delayed
from easyAI import TranspositionTable
from pdb import set_trace

DIR = "/data/home/frankf/code_1/GMK_TT/"


def ext_s(depth, idx):
    table = TranspositionTable()
    table.from_file(f"{DIR}tt_{idx}.data")
    rst = {key: value for key, value in table.d.items() if value['depth'] == depth}
    return rst


def gtt(depth, n):
    tt_g = Parallel(n_jobs=-1, verbose=10)(delayed(ext_s)(depth, idx) for idx in range(n))
    rst = {}
    for tt in tt_g:
        for key, value in tt.items():
            rst[key] = value
    table_g = TranspositionTable(own_dict=rst)
    table_g.to_file(f"{DIR}gtt.data")


if __name__ == '__main__':
    gtt(4, 129)