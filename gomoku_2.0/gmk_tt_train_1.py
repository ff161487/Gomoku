import numpy as np
import pandas as pd
from joblib import Parallel, delayed
from pickle import load
from pdb import set_trace

DIR = "/data/home/frankf/code_1/GMK_TT/"


def heuristic(ptt):
    num_l = [ptt.count(x) for x in range(8, 2, -1)]
    num_l = [ptt.count(10)] + num_l
    if num_l[0] > 0:
        return 12
    elif (num_l[1] > 0) or (num_l[2] > 1):
        return 11
    elif (num_l[2] > 0) and (num_l[3] > 0):
        return 10
    elif num_l[3] > 1:
        return 9
    elif (num_l[3] == 1) and (num_l[4] > 0):
        return 8
    elif num_l[2] == 1:
        return 7
    elif num_l[3] == 1:
        return 6
    elif num_l[5] > 1:
        return 5
    elif num_l[4] == 1:
        return 4
    elif (num_l[5] == 1) and (num_l[6] > 0):
        return 3
    elif num_l[5] == 1:
        return 2
    elif num_l[6] == 1:
        return 1
    else:
        return 0


def fx_arr(arr):
    if arr[1] == -1 or arr[2] == -1 or arr[3] == -1 or (arr[0] == -1 and arr[4] == -1):
        return 0
    else:
        a_min, a_max = min(arr), max(arr)
        c1 = arr.count(1)
        if a_max < 1:
            return 0
        elif a_min == -1:
            return 2 * c1 - 1
        elif a_min > -1:
            return 2 * c1


def fx_4(mat, i, j):
    # Extract arrays from all directions
    arr_h = [mat[i, j + x] for x in range(-2, 3)]
    arr_v = [mat[i + x, j] for x in range(-2, 3)]
    arr_d = [mat[i + x, j + x] for x in range(-2, 3)]
    arr_a = [mat[i + x, j - x] for x in range(-2, 3)]
    ptt_k = [fx_arr(arr_h), fx_arr(arr_v), fx_arr(arr_d), fx_arr(arr_a)]

    # Get same pattern matching for white
    arr_hw, arr_vw, arr_dw, arr_aw = [-x for x in arr_h], [-x for x in arr_v], [-x for x in arr_d], [-x for x in arr_a]
    ptt_w = [fx_arr(arr_hw), fx_arr(arr_vw), fx_arr(arr_dw), fx_arr(arr_aw)]
    h_k, h_w = heuristic(ptt_k), heuristic(ptt_w)
    return h_k, h_w


def fx_mat(mat):
    x_k, x_w = np.zeros((11, 11), dtype='uint8'), np.zeros((11, 11), dtype='uint8')
    for i in range(11):
        for j in range(11):
            x_k[i, j], x_w[i, j] = fx_4(mat, i, j)
    v_k, n_k = np.unique(x_k, return_counts=True)
    v_w, n_w = np.unique(x_w, return_counts=True)
    rst = np.array([v_k[-1], n_k[-1], v_w[-1], n_w[-1]])
    return rst


def train():
    with open(f"{DIR}train.data", 'rb') as f:
        y_tr, x_tr = load(f)
    rst = Parallel(n_jobs=-1, verbose=10)(delayed(fx_mat)(mat) for mat in x_tr)
    rst = pd.DataFrame(np.array(rst), columns=['v_k_max', 'n_k_max', 'v_w_max', 'n_w_max'])
    rst['y'] = y_tr
    rst['n_ply'] = (x_tr != 0).sum(axis=(1, 2))
    set_trace()


if __name__ == '__main__':
    train()