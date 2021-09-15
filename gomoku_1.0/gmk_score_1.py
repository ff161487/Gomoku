import numpy as np
from pdb import set_trace


def str_pos(x, kind):
    if kind == 'to_str':
        rst = chr(65 + x[1]) + str(15 - x[0])
    elif kind == 'to_pos':
        rst = (15 - int(x[1:]), ord(x[0]) - 65)
    return rst


def ptt_row(arr, pos, stone):
    # Copy array and set the given position to stone value
    arr_c = arr.copy()
    arr_c[pos] = stone
    
    # Compute shifted matches
    arr_c = (arr_c == stone)
    num_cfv = (arr_c[:-4] * arr_c[1:-3] * arr_c[2:-2] * arr_c[3:-1] * arr_c[4:]).sum()
    num_cfr = (arr_c[:-3] * arr_c[1:-2] * arr_c[2:-1] * arr_c[3:]).sum()
    num_cth = (arr_c[:-2] * arr_c[1:-1] * arr_c[2:]).sum()
    num_ctw = (arr_c[:-1] * arr_c[1:]).sum()
    ptt = np.array([num_cfv, num_cfr, num_cth, num_ctw])
    return ptt


def eval_ptt(ptt):
    if ptt[0] > 0:
        return 100000
    elif ptt[1] > 1:
        return 10000
    elif ptt[1] == 1 and ptt[2] > 2:
        return 2000
    elif ptt[1] == 1 and ptt[2] <= 2:
        return 500
    elif ptt[2] > 2:
        return 5000
    elif ptt[2] == 2:
        return 200
    elif ptt[2] <= 2 and ptt[3] >= 3:
        return 100
    elif 0 < ptt[3] < 3:
        return 20
    else:
        return 0


def compute_move(board, pos, ply_stone):
    # Here, the position must be blank
    assert board[pos] == 0

    # Get board array and position array
    pos_h = [(pos[0], x) for x in range(15)]
    pos_v = [(x, pos[1]) for x in range(15)]
    pos_d = [(pos[0] + x, pos[1] + x) for x in range(-min(pos), 15 - max(pos))]
    pos_a = [(pos[0] + x, pos[1] - x) for x in range(-min(pos[0], 14 - pos[1]), min(14 - pos[0], pos[1]) + 1)]
    idx_h, idx_v, idx_d, idx_a = pos[1], pos[0], pos_d.index(pos), pos_a.index(pos)
    arr_h, arr_v, arr_d, arr_a = (board[pos[0]].copy(), board[:, pos[1]].copy(), board[tuple(zip(*pos_d))].copy(),
                                  board[tuple(zip(*pos_a))].copy())

    # Compute score for player's side (Attack score)
    ptt_h = ptt_row(arr_h, idx_h, ply_stone)
    ptt_v = ptt_row(arr_v, idx_v, ply_stone)
    ptt_d = ptt_row(arr_d, idx_d, ply_stone)
    ptt_a = ptt_row(arr_a, idx_a, ply_stone)
    ptt = ptt_h + ptt_v + ptt_d + ptt_a
    sc_a = eval_ptt(ptt)

    # Compute score for opponent's side if opponent places their stone at the given position (Defense score)
    ptt_hd = ptt_row(arr_h, idx_h, -ply_stone)
    ptt_vd = ptt_row(arr_v, idx_v, -ply_stone)
    ptt_dd = ptt_row(arr_d, idx_d, -ply_stone)
    ptt_ad = ptt_row(arr_a, idx_a, -ply_stone)
    ptt_d = ptt_hd + ptt_vd + ptt_dd + ptt_ad
    sc_d = eval_ptt(ptt_d)

    # We give a weight of 0.5 to defense
    score = sc_a + sc_d / 2
    return score


def sort_moves(board, ply_stone, n_top=None):
    # Generate list of blank positions
    pos_l = [tuple(x) for x in np.transpose((board == 0).nonzero())]

    # Translate into string format positions
    mv_s = [str_pos(x, 'to_str') for x in pos_l]

    # Compute scores for each move
    sc_l = [compute_move(board, pos, ply_stone) for pos in pos_l]
    sc_order = np.argsort(sc_l)[::-1]

    # Sort moves according to order
    if n_top is None:
        pm_l = [mv_s[i] for i in sc_order]
    else:
        pm_l = [mv_s[i] for i in sc_order[:n_top]]
    return pm_l
