import numpy as np
import pandas as pd
from itertools import product
from pdb import set_trace


def mox(x):
    if len(x) < 5:
        return False
    else:
        n_x = 0
        n_seg = int((len(x) - 1) / 2)
        scanned = []
        for seg_idx in range(n_seg):
            # Keep a record of which segment has been scanned
            if seg_idx not in scanned:
                i = 2 * seg_idx + 1
                # An edge case: the last segment
                if (seg_idx == (n_seg - 1)) and (x[i] == 3):
                    n_x += 1
                    scanned.append(seg_idx)
                else:
                    cond_of2 = (x[i] + x[i + 2] > 1) and (x[i + 1] == 2)
                    cond_ot1 = (x[i] == 2) and (x[i - 1] > 0) and (x[i + 1] > 0)
                    cond_ot2 = (x[i] + x[i + 2] == 1) and (x[i + 1] == 2) and (x[i - 1] > 0) and (x[i + 3] > 0)
                    if cond_of2 or cond_ot2:
                        n_x += 1
                        scanned.append(seg_idx)
                        scanned.append(seg_idx + 1)
                    elif cond_ot1:
                        n_x += 1
                        scanned.append(seg_idx)
        return n_x >= 2


def to_arr(lst):
    rst = np.empty(4 * len(lst), dtype='uint8')
    rst[:] = 0
    start = 0
    end = 0
    for idx, val in enumerate(lst):
        end = start + val
        if idx % 2 == 1:
            rst[start:(end + 1)] = 1
        start = end
    rst = rst[:(end + 1)]
    return rst


def gen_ptt(n):
    if n == 1:
        end_p = [0, 1, 2]
    else:
        end_p = [0, 1]
    itr_p = [0, 1, 2, 3]
    seg_p = [2, 3, 4]
    comb = [end_p, itr_p]
    if n > 1:
        for i in range(n - 1):
            comb.append(seg_p)
            comb.append(itr_p)
    comb.append(end_p)
    rst = list(product(*comb))
    ex = [x for x in rst if mox(x)]
    temp = [to_arr(x) for x in ex]
    set_trace()
    rst = [x for x in rst if sum(x) >= 4 and not mox(x)]
    return rst


def ptt_df():
    ptt_s = []
    df = []
    for n in range(1, 5):
        ptt_s.extend(gen_ptt(n))
    for x in ptt_s:
        core = [str(elm) for elm in x[1:-1]]
        code = str(len(core)) + '-' + '-'.join(core)
        df.append({'code': code, 'pattern': x, 'array': to_arr(x)})
    df = pd.DataFrame.from_records(df).set_index('code').sort_index()
    set_trace()


if __name__ == '__main__':
    ptt_df()
