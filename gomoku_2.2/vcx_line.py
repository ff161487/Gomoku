import numpy as np
from pdb import set_trace


def make_line(ln_pat, pt_loc, pt_idx, drc):
    ln_pat_split = ln_pat.split('|')
    n_ln = len(ln_pat_split)
    rst = []
    for i in range(n_ln):
        dic = {'player': ln_pat_split[i][0], 'coordinate': pt_loc + (i - pt_idx) * drc}
        if len(ln_pat_split[i]) == 1:
            dic['order'] = 0
        elif len(ln_pat_split[i]) == 2:
            dic['order'] = int(ln_pat_split[i][1])
        rst.append(dic)
    return rst


if __name__ == '__main__':
    make_line('W0|B0|B0|B0|B1|W2', np.array([10000, 10000]), 1, np.array([1, 1]))
