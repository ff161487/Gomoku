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


def pattern_matching(l_kb, pos, ptt, dp):
    n_l = len(l_kb)
    if n_l == 3:
        if l_kb[1] == 1:
            if l_kb[0] > 2 and l_kb[2] > 2:
                ptt[5] += 1
            else:
                ptt[6] += 1
        elif l_kb[1] == 2:
            if l_kb[0] > 1 and l_kb[2] > 1:
                ptt[3] += 1
                dp[1].append('-'.join((str_pos(pos[l_kb[0] - 1], 'to_str'), str_pos(pos[l_kb[0] + 3], 'to_str'))))
            elif l_kb[0] == 0:
                ptt[4] += 1
                dp[2].append('-'.join((str_pos(pos[3], 'to_str'), str_pos(pos[4], 'to_str'))))
            elif l_kb[2] == 0:
                ptt[4] += 1
                dp[2].append('-'.join((str_pos(pos[l_kb[0] - 2], 'to_str'), str_pos(pos[l_kb[0] - 1], 'to_str'))))
        elif l_kb[1] == 3:
            if l_kb[0] > 0 and l_kb[2] > 0:
                ptt[1] += 1
                dp[0].append('-'.join((str_pos(pos[l_kb[0] - 1], 'to_str'), str_pos(pos[l_kb[0] + 4], 'to_str'))))
            elif l_kb[0] == 0:
                ptt[2] += 1
                dp[0].append('-'.join((str_pos(pos[4], 'to_str'), str_pos(pos[5], 'to_str'))))
            elif l_kb[2] == 0:
                ptt[2] += 1
                dp[0].append('-'.join((str_pos(pos[l_kb[0] - 2], 'to_str'), str_pos(pos[l_kb[0] - 1], 'to_str'))))
    elif n_l == 5:
        if l_kb[1] == 0 and l_kb[-2] == 0 and l_kb[2] in [2, 3]:
            if l_kb[0] > 0 and l_kb[-1] > 0:
                ptt[5] += 1
            else:
                ptt[6] += 1
        elif False:
            set_trace()
    elif n_l == 7:
        set_trace()
    elif n_l == 9:
        set_trace()


def scan_kb(arr, pos, ptt, dp):
    n_a = len(arr)
    seg_k = find_seg(arr > 0)
    l_kb = [0]

    # Search for 'Five(or more) in a Row', if find it, just win
    for seg in seg_k:
        l_kb.extend(seg)
        if seg[1] - seg[0] >= 4:
            ptt[0] += 1
            return None
    l_kb.append(n_a - 1)

    # Here, we focus on 4, 3, 2 after searching for 5(>5)
    # Exclude redundant blank point
    l_kb = [l_kb[i] - l_kb[i - 1] for i in range(1, len(l_kb))]
    pattern_matching(l_kb, pos, ptt, dp)
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
