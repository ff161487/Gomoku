import numpy as np
from pdb import set_trace


def str_pos(x, kind):
    if kind == 'to_str':
        rst = chr(65 + x[1]) + str(15 - x[0])
    elif kind == 'to_pos':
        rst = (15 - int(x[1:]), ord(x[0]) - 65)
    return rst


def heuristic(ptt):
    if ptt[0] > 0:
        return 100000
    elif (ptt[1] > 0) or (ptt[2] > 1):
        return 10000
    elif (ptt[2] > 0) and (ptt[3] > 0):
        return 7500
    elif ptt[3] > 1:
        return 2000
    elif (ptt[3] == 1) and (ptt[4] > 0):
        return 1000
    elif ptt[2] == 1:
        return 500
    elif ptt[3] == 1:
        return 200
    elif ptt[5] > 1:
        return 100
    elif ptt[4] == 1:
        return 50
    elif (ptt[5] == 1) and (ptt[6] > 0):
        return 10
    elif ptt[5] == 1:
        return 5
    elif ptt[6] == 1:
        return 3
    else:
        return 1


def find_seg(cond):
    scv = np.zeros(len(cond) + 2, dtype=bool)
    scv[0], scv[-1] = False, False
    scv[1:-1] = cond
    start = np.nonzero(cond & ~scv[:-2])[0]
    end = np.nonzero(cond & ~scv[2:])[0]
    return list(zip(start, end))


def ep_encode(ep):
    if ep == np.array([1]):
        return 0
    elif ep == np.array([0, 1]):
        return 1
    elif ep == np.array([0, 0, 1]):
        return 2
    elif ep == np.array([1, 0, 1]):
        return 3
    elif ep == np.array([0, 0, 0, 1]):
        return 4
    elif ep == np.array([0, 1, 0, 1]):
        return 5
    elif ep == np.array([1, 0, 0, 1]):
        return 6
    elif ep == np.array([1, 1, 0, 1]):
        return 7


def scan_kb(arr, ptt):
    n_a = len(arr)
    seg_k = find_seg(arr > 0)
    scanned = []

    # Search for 'Five(or more) in a Row', if find it, just win
    for i, seg in enumerate(seg_k):
        if i not in scanned:
            scanned.append(i)
            # Endpoint Encoding
            vec_l, vec_r = arr[:(seg[0] + 1)][-4:], arr[seg[1]:][::-1][-4:]
            epe = (ep_encode(vec_l), ep_encode(vec_r))

            if seg[1] - seg[0] >= 4:
                # Win by connected 5 or more
                ptt[0] += 1
                return None
            elif seg[1] - seg[0] == 3:
                # Opened Four
                if seg[0] > 0 and seg[1] < n_a - 1:
                    ptt[1] += 1
                # Blocked Four
                else:
                    ptt[2] += 1
                if epe[0] in [3, 5, 7]:
                    scanned.append(i - 1)
                if epe[1] in [3, 5, 7]:
                    scanned.append(i + 1)
            elif seg[1] - seg[0] == 2:
                cond_l, cond_r = (epe[0] in [3, 5, 7]), (epe[1] in [3, 5, 7])
                if cond_l:
                    scanned.append(i - 1)
                if cond_r:
                    scanned.append(i + 1)
                # Opened Four
                if cond_l and cond_r:
                    ptt[1] += 1
                # Blocked Four
                elif cond_l + cond_r == 1:
                    ptt[2] += 1
                else:
                    # Blocked Three
                    if seg[0] == 0:
                        ptt[4] += 1
                        dp[2].append('-'.join((str_pos(pos[3], 'to_str'), str_pos(pos[4], 'to_str'))))
                    elif seg[1] == n_a - 1:
                        ptt[4] += 1
                        dp[2].append('-'.join((str_pos(pos[n_a - 4], 'to_str'), str_pos(pos[n_a - 5], 'to_str'))))
                    elif seg[0] == 1 and seg[1] == n_a - 2:
                        ptt[4] += 1
                        dp[2].append('-'.join((str_pos(pos[0], 'to_str'), str_pos(pos[n_a - 1], 'to_str'))))
                    # Opened Three
                    else:
                        ptt[3] += 1
                        p1, p2 = str_pos(pos[seg[0] - 1], 'to_str'), str_pos(pos[seg[0] + 3], 'to_str')
                        if seg[0] == 1 and seg[1] != n_a - 2:
                            dp[1].append(f'{p2}')
                            dp[2].append(f'{p1}')
                        elif seg[0] != 1 and seg[1] == n_a - 2:
                            dp[1].append(f'{p1}')
                            dp[2].append(f'{p2}')
                        else:
                            dp[1].append('{0}({1})-{1}({0})'.format(p1, p2))
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
                # Opened Three
                if epe == (3, 3):
                    ptt[3] += 1
                    p1, p2, p3, p4 = (str_pos(pos[seg[0] - 3], 'to_str'), str_pos(pos[seg[0] - 1], 'to_str'),
                                      str_pos(pos[seg[1] + 1], 'to_str'), str_pos(pos[seg[1] + 3], 'to_str'))
                    dp[1].append('{1}({2},{3})-{2}({0},{1})'.format(p1, p2, p3, p4))
                    scanned.extend([i - 1, i + 1])
                elif epe[0] == 3 and epe[1] not in [0, 4]:
                    ptt[3] += 1
                    p1, p2, p3 = (str_pos(pos[seg[0] - 3], 'to_str'), str_pos(pos[seg[0] - 1], 'to_str'),
                                  str_pos(pos[seg[1] + 1], 'to_str'))
                    dp[1].append('{1}-{0}({1},{2})-{2}({0},{1})'.format(p1, p2, p3))
                    scanned.append(i - 1)
                elif epe[1] == 3 and epe[0] not in [0, 4]:
                    ptt[3] += 1
                    p1, p2, p3 = (str_pos(pos[seg[0] - 1], 'to_str'), str_pos(pos[seg[1] + 1], 'to_str'),
                                  str_pos(pos[seg[1] + 3], 'to_str'))
                    dp[1].append('{1}-{0}({1},{2})-{2}({0},{1})'.format(p1, p2, p3))
                    scanned.append(i + 1)
                # Blocked Three
                if epe == (5, 5):
                    ptt[4] += 1
                    p1, p2, p3, p4 = (str_pos(pos[seg[0] - 2], 'to_str'), str_pos(pos[seg[0] - 1], 'to_str'),
                                      str_pos(pos[seg[1] + 1], 'to_str'), str_pos(pos[seg[1] + 2], 'to_str'))
                    dp[2].append('{0}-{1}_{2}-{3}'.format(p1, p2, p3, p4))
                    scanned.extend([i - 1, i + 1])
                elif epe in [(5, 0), (5, 1), (5, 6)]:
                    ptt[4] += 1
                    dp[2].append('-'.join((str_pos(pos[seg[0] - 1], 'to_str'), str_pos(pos[seg[0] - 2], 'to_str'))))
                    scanned.append(i - 1)
                elif epe in [(0, 5), (1, 5), (6, 5)]:
                    ptt[4] += 1
                    dp[2].append('-'.join((str_pos(pos[seg[1] + 1], 'to_str'), str_pos(pos[seg[1] + 2], 'to_str'))))
                    scanned.append(i + 1)
                elif epe == (5, 2):
                    ptt[4] += 1
                    p1, p2, p3 = (str_pos(pos[seg[0] - 2], 'to_str'), str_pos(pos[seg[0] - 1], 'to_str'),
                                  str_pos(pos[seg[1] + 1], 'to_str'))
                    dp[2].append('{1}-{0}({1},{2})-{2}({0},{1})'.format(p1, p2, p3))
                    scanned.extend([i - 1, i + 1])
                elif epe == (2, 5):
                    ptt[4] += 1
                    p1, p2, p3 = (str_pos(pos[seg[0] - 1], 'to_str'), str_pos(pos[seg[1] + 1], 'to_str'),
                                  str_pos(pos[seg[1] + 2], 'to_str'))
                    dp[2].append('{1}-{0}({1},{2})-{2}({0},{1})'.format(p1, p2, p3))
                    scanned.extend([i - 1, i + 1])
                elif epe in [(6, 2), (2, 2), (1, 2), (2, 1), (2, 6)]:
                    ptt[4] += 1
                    dp[2].append('-'.join((str_pos(pos[seg[0] - 1], 'to_str'), str_pos(pos[seg[1] + 1], 'to_str'))))
                    if epe == (2, 2):
                        scanned.extend([i - 1, i + 1])
                    elif epe in [(6, 2), (1, 2)]:
                        scanned.append(i + 1)
                    elif epe in [(2, 6), (2, 1)]:
                        scanned.append(i - 1)
                elif epe == (3, 0):
                    ptt[4] += 1
                    dp[2].append('-'.join((str_pos(pos[seg[0] - 3], 'to_str'), str_pos(pos[seg[0] - 1], 'to_str'))))
                    scanned.append(i - 1)
                elif epe == (0, 3):
                    ptt[4] += 1
                    dp[2].append('-'.join((str_pos(pos[seg[1] + 1], 'to_str'), str_pos(pos[seg[1] + 3], 'to_str'))))
                    scanned.append(i + 1)
                # Opened Two
                elif epe in [(1, 1), (1, 6), (6, 1), (6, 6)]:
                    ptt[5] += 1
                # Blocked Two
                elif epe in [(0, 1), (1, 0), (0, 6), (6, 0)]:
                    ptt[6] += 1

    # The 'leftover' will be 'single-stone segment'
    un_scanned = [j for j in range(len(seg_k)) if j not in scanned]
    while len(un_scanned) > 0:
        j = un_scanned.pop(0)  # Take the first element out of un_scanned
        scanned.append(j)  # Append this element to scanned

        # Define 'single-stone' pattern matrix
        ss = np.full((4, 2), -1, 'int8')
        ss[0] = [j, seg_k[j][0]]
        if len(un_scanned) > 0:
            ss[1] = [un_scanned[0], seg_k[un_scanned[0]][0]]
            if len(un_scanned) > 1:
                ss[2] = [un_scanned[1], seg_k[un_scanned[1]][0]]
                if len(un_scanned) > 2:
                    ss[3] = [un_scanned[2], seg_k[un_scanned[2]][0]]

        # Encode pattern and recognition
        ss_encode(ss, n_a, ptt, dp)
        set_trace()
        if (j + 1) in un_scanned:
            dis = seg_k[j + 1][0] - seg_k[j][0]
            if dis <= 4:
                un_scanned.pop(0)
                scanned.append(j + 1)
                if dis > 2:
                    if seg_k[j][0] > 0 and seg_k[j + 1][0] < n_a - 1:

                        ptt[5] += 1
                        set_trace()
                else:
                    set_trace()
            set_trace()


def scan_kbw(arr, idx, ply_stone):
    # Copy array and set the given position to stone value
    arr_c = arr.copy()
    arr_c[idx] = ply_stone
    arr_c = ply_stone * arr_c  # Set ply = 1 and op = -1

    # Define 'pattern vector', 'defense point list' and 'black-blank segments'
    ptt = np.zeros(7, dtype='uint8')

    # Scan all segments separate by opponent's stone
    seg_kb = find_seg(arr > -1)
    for seg in seg_kb:
        # If the segment length is less than 5, we can ignore it
        if seg[1] - seg[0] >= 4:
            scan_kb(arr[seg[0]:(seg[1] + 1)], ptt)
    set_trace()
    return ptt


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
    ptt_h = scan_kbw(arr_h, idx_h, ply_stone)
    ptt_v = scan_kbw(arr_v, idx_v, ply_stone)
    ptt_d = scan_kbw(arr_d, idx_d, ply_stone)
    ptt_a = scan_kbw(arr_a, idx_a, ply_stone)
    ptt = ptt_h + ptt_v + ptt_d + ptt_a
    sc_a = heuristic(ptt)

    # Compute score for opponent's side if opponent places their stone at the given position (Defense score)
    ptt_hd = scan_kbw(arr_h, idx_h, -ply_stone)
    ptt_vd = scan_kbw(arr_v, idx_v, -ply_stone)
    ptt_dd = scan_kbw(arr_d, idx_d, -ply_stone)
    ptt_ad = scan_kbw(arr_a, idx_a, -ply_stone)
    ptt_d = ptt_hd + ptt_vd + ptt_dd + ptt_ad
    sc_d = heuristic(ptt_d)

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
