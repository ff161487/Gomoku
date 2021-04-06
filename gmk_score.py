import numpy as np
from pdb import set_trace


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


def scan_kb(arr, pos, ptt, dp):
    n_a = len(arr)
    seg_k = find_seg(arr > 0)
    scanned = []

    # Search for 'Five(or more) in a Row', if find it, just win
    for i, seg in enumerate(seg_k):
        if i not in scanned and seg[1] - seg[0] > 0:
            scanned.append(i)
            if seg[1] - seg[0] >= 4:
                ptt[0] += 1
                return None
            elif seg[1] - seg[0] == 3:
                if seg[0] > 0 and seg[1] < n_a - 1:
                    ptt[1] += 1
                    dp[0].append('_'.join((str_pos(pos[seg[0] - 1], 'to_str'), str_pos(pos[seg[1] + 1], 'to_str'))))
                elif seg[0] == 0:
                    ptt[2] += 1
                    dp[0].append(str_pos(pos[seg[1] + 1], 'to_str'))
                elif seg[1] == n_a - 1:
                    ptt[2] += 1
                    dp[0].append(str_pos(pos[seg[0] - 1], 'to_str'))
                if i > 0:
                    if seg[0] - seg_k[i - 1][1] == 2:
                        scanned.append(i - 1)
                if i < len(seg_k) - 1:
                    if seg_k[i + 1][0] - seg[1] == 2:
                        scanned.append(i + 1)
            elif seg[1] - seg[0] == 2:
                cond_l = False
                cond_r = False
                if i > 0:
                    if seg[0] - seg_k[i - 1][1] == 2:
                        scanned.append(i - 1)
                        cond_l = True
                if i < len(seg_k) - 1:
                    if seg_k[i + 1][0] - seg[1] == 2:
                        scanned.append(i + 1)
                        cond_r = True
                if cond_l and cond_r:
                    ptt[1] += 1
                    dp[0].append('_'.join((str_pos(pos[seg[0] - 1], 'to_str'), str_pos(pos[seg[1] + 1], 'to_str'))))
                elif cond_r and not cond_l:
                    ptt[2] += 1
                    dp[0].append(str_pos(pos[seg[1] + 1], 'to_str'))
                elif cond_l and not cond_r:
                    ptt[2] += 1
                    dp[0].append(str_pos(pos[seg[0] - 1], 'to_str'))
                else:
                    if seg[0] == 0:
                        ptt[4] += 1
                        dp[2].append('-'.join((str_pos(pos[3], 'to_str'), str_pos(pos[4], 'to_str'))))
                    elif seg[1] == n_a - 1:
                        ptt[4] += 1
                        dp[2].append('-'.join((str_pos(pos[n_a - 4], 'to_str'), str_pos(pos[n_a - 5], 'to_str'))))
                    else:
                        ptt[3] += 1
                        dp[1].append('-'.join((str_pos(pos[seg[0] - 1], 'to_str'), str_pos(pos[seg[0] + 3], 'to_str'))))
            elif seg[1] - seg[0] == 1:
                n_l, n_r = -1, -1
                set_trace()
    set_trace()


def scan_kbw(arr, pos):
    # Define 'pattern vector', 'defense point list' and 'black-blank segments'
    ptt = np.zeros(7, dtype='uint8')
    dp = [[], [], []]
    seg_kb = find_seg(arr > -1)
    for seg in seg_kb:
        if seg[1] - seg[0] >= 4:
            scan_kb(arr[seg[0]:(seg[1] + 1)], pos[seg[0]:(seg[1] + 1)], ptt, dp)
    set_trace()
    return ptt, dp


def compute_move(board, pos):
    # Get board array and position array
    ply = board[pos]
    pos_h = [(pos[0], x) for x in range(15)]
    pos_v = [(x, pos[1]) for x in range(15)]
    pos_d = [(pos[0] + x, pos[1] + x) for x in range(-min(pos), 15 - max(pos))]
    pos_a = [(pos[0] + x, pos[1] - x) for x in range(-min(pos[0], 14 - pos[1]), min(14 - pos[0], pos[1]) + 1)]
    idx_h, idx_v, idx_d, idx_a = pos[1], pos[0], pos_d.index(pos), pos_a.index(pos)
    arr_h, arr_v, arr_d, arr_a = (ply * board[pos[0]]).copy(), (ply * board[pos[1]]).copy(), (ply * board[tuple(zip(
        *pos_d))]).copy(), (ply * board[tuple(zip(*pos_a))]).copy()

    # Slice using 'board[tuple(zip(*pos))]'
    scan_kbw(arr_h, pos_h)
    set_trace()
    return pos
