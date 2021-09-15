import numpy as np
from pdb import set_trace

slash = np.array([[x, -x] for x in range(-14, 15)])

oct_d = np.array([[1, 0], [1, 1], [0, 1], [-1, 1], [-1, 0], [-1, -1], [0, -1], [1, -1]])


def str_pos(x, kind):
    if kind == 'to_str':
        rst = chr(65 + x[1]) + str(15 - x[0])
    elif kind == 'to_pos':
        rst = (15 - int(x[1:]), ord(x[0]) - 65)
    return rst


def find_seg(cond):
    scv = np.zeros(len(cond) + 2, dtype=bool)
    scv[0], scv[-1] = False, False
    scv[1:-1] = cond
    start = np.nonzero(cond & ~scv[:-2])[0]
    end = np.nonzero(cond & ~scv[2:])[0]
    return list(zip(start, end))


def pattern_matching(arr, pos, seg_k, ptt, dp):
    n_a = len(arr)
    if n_a == 3:
        if arr in [np.array([1, 1, 0]), np.array([0, 1, 1])]:
            ptt[6] += 1
    elif n_a == 4:
        set_trace()


def find_hot(arr, pos, seg_k):
    dp_hot = []
    set_trace()
    return dp_hot


def scan_kb(arr, pos, ptt, dp, only_hot):
    n_a = len(arr)
    seg_k = find_seg(arr > 0)

    # Search for 'Five(or more) in a Row', if find it, just win
    for seg in seg_k:
        if seg[1] - seg[0] >= 4:
            ptt[0] += 1
            return None

    # Here, we focus on 4, 3, 2 after searching for 5(>5)
    # Exclude redundant blank point
    start, end = 0, (n_a - 1)
    for start in range(n_a):
        if arr[start] == 0:
            start += 1
        else:
            break
    for end in range(n_a - 1, -1, -1):
        if arr[end] == 0:
            end -= 1
        else:
            break
    if start > 0:
        start -= 1
    if end < (n_a - 1):
        end += 1
    arr = arr[start:(end + 1)]
    pos = pos[start:(end + 1)]
    seg_k = [(seg[0] - start, seg[1] - start) for seg in seg_k]

    # Check for pattern
    if len(arr) >= 3:
        if only_hot:
            dp_hot = find_hot(arr, pos, seg_k)
            return dp_hot
        else:
            pattern_matching(arr, pos, seg_k, ptt, dp)


def scan_kbw(arr, pos, only_hot=False):
    # Define 'pattern vector', 'defense point list' and 'black-blank segments'
    ptt = np.zeros(7, dtype='uint8')
    dp = [[], []]
    seg_kb = find_seg(arr > -1)
    rst = []
    for seg in seg_kb:
        if seg[1] - seg[0] >= 4:
            rst.extend(scan_kb(arr[seg[0]:(seg[1] + 1)], pos[seg[0]:(seg[1] + 1)], ptt, dp, only_hot))
    set_trace()
    return ptt, dp


"""
def dsc_arr(arr, idx):
    arr_o = arr.copy()
    arr_o[idx] = 0
    sc_b = pattern_matching(arr)
    sc_w = pattern_matching(-arr)
    sc_bo = pattern_matching(arr_o)
    sc_wo = pattern_matching(arr_o)
    dsc_a = np.array([sc_b - sc_bo, sc_w - sc_wo])
    return dsc_a


def dsc(board, pos):
    offset = pos[1] - pos[0]

    # Get anti-diagonal
    ad = np.array([board[x[0], x[1]] for x in pos + slash if legal(x)], dtype='int8')

    # Compute 'delta score'
    dsc_hz = dsc_arr(board[pos[0]], pos[1])
    dsc_vt = dsc_arr(board[:, pos[1]], pos[0])
    dsc_da = dsc_arr(board.diagonal(offset), min(pos[0], pos[1]))
    dsc_ad = dsc_arr(ad, 14 - max(14 - pos[0], pos[1]))
    dsc_t = dsc_hz + dsc_vt + dsc_da + dsc_ad
    return dsc_t


def find_five(board, nplayer):
    ply_s = (board == (3 - 2 * nplayer))
    ply_s_lr = np.fliplr(ply_s)
    col_sum = ply_s.sum(0)
    row_sum = ply_s.sum(1)
    win = False

    # Check rows and columns
    for i in range(15):
        # Check row
        if row_sum[i] >= 5:
            win = has_five_array(ply_s[i])
            if win:
                break

        # Check column
        if col_sum[i] >= 5:
            win = has_five_array(ply_s[:, i])
            if win:
                break

    # Check diagonals and anti-diagonals if no five in rows and columns
    if not win:
        for j in range(-10, 11):
            # Check diagonal
            vec = np.diag(ply_s, j)
            if vec.sum() >= 5:
                win = has_five_array(vec)
                if win:
                    break

            # Check anti-diagonal
            vec = np.diag(ply_s_lr, j)
            if vec.sum() >= 5:
                win = has_five_array(vec)
                if win:
                    break
    return win
"""


def compute_move(board, pos):
    # Get board array and position array
    pos_h = [(pos[0], x) for x in range(15)]
    pos_v = [(x, pos[1]) for x in range(15)]
    pos_d = [(pos[0] + x, pos[1] + x) for x in range(-min(pos), 15 - max(pos))]
    pos_a = [(pos[0] + x, pos[1] - x) for x in range(-min(pos[0], 14 - pos[1]), min(14 - pos[0], pos[1]) + 1)]

    # Slice using 'board[tuple(zip(*pos))]'
    scan_kbw(board[pos[0]], pos_h)
    set_trace()
    return pos


if __name__ == '__main__':
    bd = np.random.randint(low=-12, high=12, size=(15, 15))
    bd = np.round(bd / 10).astype('int8')
    rs = compute_move(bd, (7, 8))
    set_trace()
