import numpy as np
from gmk_score_2 import find_seg, compute_move, str_pos, sort_moves, scan_kb, scan_kbw
from gmk_tt_para_1 import get_pm
from random import sample
from pdb import set_trace


def fs_l(cond):
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


def test_find_seg():
    cond_arr = np.array([True, True, False, True, True, True, False, True])
    seg_l = find_seg(cond_arr)
    seg_l1 = fs_l(cond_arr)
    set_trace()


def make_board():
    pos_b = [(x, y) for x in range(15) for y in range(15)]
    pos_l = sample(pos_b, k=100)
    board = np.zeros((15, 15), dtype='int8')
    for i, pos in enumerate(pos_l):
        board[pos] = 1 - 2 * (i % 2)

    # Test scoring
    pos = tuple(np.transpose((board == 0).nonzero())[0])
    score = compute_move(board, pos, 1)
    set_trace()


def test_score():
    mvs = ['H8', 'I7', 'G7', 'F10', 'I9', 'G10', 'J10', 'K11', 'F6']
    pos_l = [str_pos(x, 'to_pos') for x in mvs[:-1]]
    board = np.zeros((15, 15), dtype='int8')
    for i, pos in enumerate(pos_l):
        board[pos] = 1 - 2 * (i % 2)

    # Test scoring
    pos = str_pos('F6', 'to_pos')
    score = compute_move(board, pos, 1)
    set_trace()


def test_sort():
    mvs = ['H8', 'I7', 'G7', 'H7', 'I9', 'F6', 'J10']
    pos_l = [str_pos(x, 'to_pos') for x in mvs]
    board = np.zeros((15, 15), dtype='int8')
    for i, pos in enumerate(pos_l):
        board[pos] = 1 - 2 * (i % 2)

    # Test sorting
    pm_l_a = sort_moves(board, -1, 'AI')
    set_trace()


def test_sort_1():
    # mvs = ['H8', 'I7', 'G7', 'H7', 'I9', 'F6', 'J10']
    mvs = ['H8', 'I7']
    pos_l = [str_pos(x, 'to_pos') for x in mvs]
    board = np.zeros((15, 15), dtype='int8')
    for i, pos in enumerate(pos_l):
        board[pos] = 1 - 2 * (i % 2)

    # Test sorting
    pm_l_a = sort_moves(board, 1, 'AI')
    set_trace()


def test_scan_kb():
    # Define 'pattern vector', 'defense point list' and 'black-blank segments'
    ptt = np.zeros(7, dtype='uint8')
    arr = np.array([1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1])
    scan_kb(arr, ptt)
    set_trace()


def test_scan_kbw():
    # Define 'pattern vector', 'defense point list' and 'black-blank segments'
    arr = np.array([0, 0, 0, 0, -1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0])
    ptt = scan_kbw(arr, 9, 1)
    set_trace()


def test_pm():
    mv = ['H8', 'H7', 'I7', 'K5', 'G9', 'F10', 'I8']

    set_trace()


if __name__ == '__main__':
    test_pm()
    # make_board()
    # test_ptt_row()

