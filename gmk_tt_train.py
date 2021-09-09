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
    for key, value in table.d.items():
        if value['depth'] == 3:
            # Transform key to list format
            mv_s = [key[i: (i + 2)] for i in range(0, len(key), 2)]
            mv_s.append(value['move'])

            #
            set_trace()


if __name__ == '__main__':
    ext_s(0)