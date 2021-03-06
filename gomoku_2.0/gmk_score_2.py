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
    n = len(cond)
    rst = []
    start, end = None, None
    for i in range(n):
        if i < (n - 1):
            if cond[i] and not cond[i + 1]:
                end = i
        else:
            if cond[i]:
                end = i
        if i > 0:
            if cond[i] and not cond[i - 1]:
                start = i
        else:
            if cond[i]:
                start = i

        # Collect (start, end) pair and reset them to None
        if start is not None and end is not None:
            rst += [(start, end)]
            start, end = None, None
    return rst


def ep_encode(ep):
    n_ep = len(ep)
    rst = n_ep - 1
    if n_ep == 3:
        rst += ep[0]
    elif n_ep == 4:
        rst += 1 + 2 * ep[0] + ep[1]
    return rst


def scan_kb(arr, ptt):
    n_a = len(arr)
    seg_k = find_seg(arr > 0)
    neg_len_seg = [seg[0] - seg[1] for seg in seg_k]
    itr = [(idx, seg_k[idx]) for idx in np.argsort(neg_len_seg)]
    scanned = []

    # Search for 'Five(or more) in a Row', if find it, just win
    for i, seg in itr:
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
                    if epe[0] == 0 or epe[1] == 0 or epe == (1, 1):
                        ptt[4] += 1
                    # Opened Three
                    else:
                        ptt[3] += 1
            elif seg[1] - seg[0] == 1:
                # Opened Four
                if epe == (7, 7):
                    ptt[1] += 1
                    scanned.extend([i - 1, i + 1])
                # Blocked Four
                elif epe[0] == 7 and epe[1] != 7:
                    ptt[2] += 1
                    scanned.append(i - 1)
                elif epe[1] == 7 and epe[0] != 7:
                    ptt[2] += 1
                    scanned.append(i + 1)
                # Opened Three
                if epe == (5, 5):
                    ptt[3] += 1
                    scanned.extend([i - 1, i + 1])
                elif epe[0] == 5 and epe[1] != 5 and 1 <= epe[1] <= 6 or epe == (3, 6):
                    ptt[3] += 1
                    scanned.append(i - 1)
                elif epe[1] == 5 and epe[0] != 5 and 1 <= epe[0] <= 6 or epe == (6, 3):
                    ptt[3] += 1
                    scanned.append(i + 1)
                # Blocked Three
                if epe in [(3, 3), (6, 6)]:
                    ptt[4] += 1
                    scanned.extend([i - 1, i + 1])
                elif epe[0] in [3, 6] and epe[1] in [0, 1, 2, 4]:
                    ptt[4] += 1
                    scanned.append(i - 1)
                elif epe[1] in [3, 6] and epe[0] in [0, 1, 2, 4]:
                    ptt[4] += 1
                    scanned.append(i + 1)

                # Opened Two
                elif epe in [(2, 2), (1, 4), (4, 1), (4, 4), (2, 4), (4, 2)]:
                    ptt[5] += 1
                # Blocked Two
                elif epe in [(0, 4), (4, 0), (2, 1), (1, 2)]:
                    ptt[6] += 1


def scan_kbw(arr, idx, ply_stone):
    # Copy array and set the given position to stone value
    arr_c = arr.copy()
    arr_c[idx] = ply_stone
    arr_c = ply_stone * arr_c  # Set ply = 1 and op = -1

    # Define 'pattern vector', 'defense point list' and 'black-blank segments'
    ptt = np.zeros(7, dtype='uint8')

    # Scan all segments separate by opponent's stone
    seg_kb = find_seg(arr_c > -1)
    for seg in seg_kb:
        # If the segment length is less than 5, we can ignore it
        if seg[1] - seg[0] >= 4:
            scan_kb(arr_c[seg[0]:(seg[1] + 1)], ptt)
    return ptt


def compute_move(board, pos, ply_stone):
    # Here, the position must be blank
    assert board[pos] == 0

    # Get board array and position array
    # pos_h = [(pos[0], x) for x in range(15)]
    # pos_v = [(x, pos[1]) for x in range(15)]
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
    return sc_a, sc_d


def sort_moves(board, ply_stone, name):
    # Generate list of blank positions
    pos_l = [tuple(x) for x in np.transpose((board == 0).nonzero())]

    # For Human Player, return all moves
    if name == 'Human':
        # Translate all positions into string format
        mv_s = [str_pos(x, 'to_str') for x in pos_l]

    # For AI Player, we prune some moves by first-layer evaluation
    elif name == 'AI':
        # Compute score for all moves
        n_pos = len(pos_l)
        sc_a, sc_d = np.ones(n_pos), np.ones(n_pos)
        for i, pos in enumerate(pos_l):
            sc_a[i], sc_d[i] = compute_move(board, pos, ply_stone)
        sc = sc_a + 0.5 * sc_d
        sca_max, scd_max = sc_a.max(), sc_d.max()

        # Return moves with pruning
        if sca_max == 100000:
            idx_l = [i for i in range(n_pos) if sc_a[i] == 100000]
        elif scd_max == 100000:
            idx_l = [i for i in range(n_pos) if sc_d[i] == 100000]
        elif sca_max == 10000:
            idx_l = [i for i in range(n_pos) if sc_a[i] == 10000]
        elif scd_max == 10000:
            idx_l = [i for i in range(n_pos) if sc_d[i] == 10000 or sc_a[i] in [7500, 500]]
        elif sca_max == 7500:
            cond_l = [i for i in range(n_pos) if sc_a[i] in [7500, 500] and sc_d[i] in [7500, 500]]
            if len(cond_l) > 0:
                idx_l = [i for i in range(n_pos) if sc[i] >= 3.5]
            else:
                idx_l = [i for i in range(n_pos) if sc_a[i] == 7500]
        elif scd_max == 7500:
            cond_l = [i for i in range(n_pos) if sc_a[i] == 500 and sc_d[i] in [7500, 500]]
            if len(cond_l) > 0:
                idx_l = [i for i in range(n_pos) if sc[i] >= 3.5]
            else:
                idx_l = [i for i in range(n_pos) if sc_d[i] == 7500]
        elif 20 <= sca_max <= 2000 or 20 <= scd_max <= 2000:
            idx_l = [i for i in range(n_pos) if sc[i] >= 11]
        elif 3 <= sca_max < 20 or 3 <= scd_max < 20:
            idx_l = [i for i in range(n_pos) if sc[i] >= 2.5]
        else:
            idx_l = list(range(n_pos))

        # Sort positions by scores
        sc_l = [sc[i] for i in idx_l]
        sc_order = np.argsort(sc_l)[::-1]
        mv_s = [str_pos(pos_l[idx_l[x]], 'to_str') for x in sc_order]

    return mv_s
