import numpy as np
from pdb import set_trace

oct_d = np.array([[1, 0], [1, 1], [0, 1], [-1, 1], [-1, 0], [-1, -1], [0, -1], [1, -1]])


def legal(ind):
    return (ind[0] > -1) and (ind[0] < 15) and (ind[1] > -1) and (ind[1] < 15)


def str_pos(x, kind):
    if kind == 'to_str':
        rst = chr(65 + x[1]) + str(15 - x[0])
    elif kind == 'to_pos':
        rst = (15 - int(x[1:]), ord(x[0]) - 65)
    return rst


def dist2points(board):
    pm_l = []
    for pos in zip(*np.where(board != 0)):
        pm_l.extend(list((pos + oct_d)))
        pm_l.extend(list((pos + 2 * oct_d)))
    pm_l = [x for x in pm_l if legal(x)]
    pm_l = [x for x in pm_l if board[x[0], x[1]] == 0]
    pm_l = list(set([str_pos(x, 'to_str') for x in pm_l]))
    return pm_l


def find_seg(cond):
    scv = np.zeros(len(cond) + 2, dtype=bool)
    scv[0], scv[-1] = False, False
    scv[1:-1] = cond
    start = np.nonzero(cond & ~scv[:-2])[0]
    end = np.nonzero(cond & ~scv[2:])[0]
    return list(zip(start, end))


def ep_encode(ep):
    if ep == [-1, -1, 0]:
        return 0
    elif ep[:2] == [-1, -1] and ep[2] > 0:
        return 1
    elif ep == [2, 0, 0]:
        return 2
    elif ep[:2] == [2, 0] and ep[2] > 0:
        return 3
    elif ep[0] == 2 and ep[1] > 0:
        return 4
    elif ep[0] == 3:
        return 5
    elif ep[0] > 3:
        return 6


def scan_kb(arr, pos, ptt, dp):
    n_a = len(arr)
    seg_k = find_seg(arr > 0)
    scanned = []

    # Search for 'Five(or more) in a Row', if find it, just win
    for i, seg in enumerate(seg_k):
        if i not in scanned and seg[1] - seg[0] > 0:
            scanned.append(i)
            if seg[1] - seg[0] >= 4:
                # Win by connected 5 or more
                ptt[0] += 1
                return None
            elif seg[1] - seg[0] == 3:
                # Opened Four
                if seg[0] > 0 and seg[1] < n_a - 1:
                    ptt[1] += 1
                    dp[0].append('_'.join((str_pos(pos[seg[0] - 1], 'to_str'), str_pos(pos[seg[1] + 1], 'to_str'))))
                # Blocked Four
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
                # Opened Four
                if cond_l and cond_r:
                    ptt[1] += 1
                    dp[0].append('_'.join((str_pos(pos[seg[0] - 1], 'to_str'), str_pos(pos[seg[1] + 1], 'to_str'))))
                # Blocked Four
                elif cond_r and not cond_l:
                    ptt[2] += 1
                    dp[0].append(str_pos(pos[seg[1] + 1], 'to_str'))
                elif cond_l and not cond_r:
                    ptt[2] += 1
                    dp[0].append(str_pos(pos[seg[0] - 1], 'to_str'))
            elif seg[1] - seg[0] == 1:
                ep_l, ep_r = [-1, -1, 0], [-1, -1, 0]
                if i > 0:
                    ep_l = [seg[0] - seg_k[i - 1][1], seg_k[i - 1][1] - seg_k[i - 1][0], seg_k[i - 1][0]]
                else:
                    ep_l[2] = seg[0]
                if i < len(seg_k) - 1:
                    ep_r = [seg_k[i + 1][0] - seg[1], seg_k[i + 1][1] - seg_k[i + 1][0], n_a - 1 - seg_k[i + 1][1]]
                else:
                    ep_r[2] = n_a - 1 - seg[1]
                epe = (ep_encode(ep_l), ep_encode(ep_r))

                # Opened Four
                if epe == (4, 4):
                    ptt[1] += 1
                    dp[0].append('_'.join((str_pos(pos[seg[0] - 1], 'to_str'), str_pos(pos[seg[1] + 1], 'to_str'))))
                    scanned.extend([i - 1, i + 1])
                # Blocked Four
                elif epe[0] == 4 and epe[1] != 4:
                    ptt[2] += 1
                    dp[0].append(str_pos(pos[seg[0] - 1], 'to_str'))
                    scanned.append(i - 1)
                elif epe[1] == 4 and epe[0] != 4:
                    ptt[2] += 1
                    dp[0].append(str_pos(pos[seg[1] + 1], 'to_str'))
                    scanned.append(i + 1)


def scan_kbw(arr, pos):
    # Define 'pattern vector', 'defense point list' and 'black-blank segments'
    ptt = np.zeros(3, dtype='uint8')
    dp = [[], []]
    seg_kb = find_seg(arr > -1)
    for seg in seg_kb:
        if seg[1] - seg[0] >= 4:
            scan_kb(arr[seg[0]:(seg[1] + 1)], pos[seg[0]:(seg[1] + 1)], ptt, dp)
    dp[0] = '|'.join(dp[0])
    dp[1] = '|'.join(dp[1])
    return ptt, dp


def compute_move(board, pos):
    # Get board array and position array
    ply = board[pos]
    pos_h = [(pos[0], x) for x in range(15)]
    pos_v = [(x, pos[1]) for x in range(15)]
    pos_d = [(pos[0] + x, pos[1] + x) for x in range(-min(pos), 15 - max(pos))]
    pos_a = [(pos[0] + x, pos[1] - x) for x in range(-min(pos[0], 14 - pos[1]), min(14 - pos[0], pos[1]) + 1)]
    arr_h, arr_v, arr_d, arr_a = (ply * board[pos[0]]).copy(), (ply * board[pos[1]]).copy(), (ply * board[tuple(zip(
        *pos_d))]).copy(), (ply * board[tuple(zip(*pos_a))]).copy()

    # Slice using 'board[tuple(zip(*pos))]'
    ptt_h, dp_h = scan_kbw(arr_h, pos_h)
    ptt_v, dp_v = scan_kbw(arr_v, pos_v)
    ptt_d, dp_d = scan_kbw(arr_d, pos_d)
    ptt_a, dp_a = scan_kbw(arr_a, pos_a)

    # Combine pattern and defence points
    ptt = ptt_h + ptt_v + ptt_d + ptt_a
    dp = '|'.join(['_'.join(x) for x in zip(dp_h, dp_v, dp_d, dp_a)])

    # Compute score
    score = 0
    if ptt[0] > 0:
        score = 100000
    elif ptt[1] > 0 or ptt[2] > 1:
        score = 10000
    elif ptt[2] == 1:
        score = 500
    return score, dp
