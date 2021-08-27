import numpy as np
from gmk_score import compute_move, scan_kb
from random import choices
from pdb import set_trace


def make_board():
    pos_b = [(x, y) for x in range(15) for y in range(15)]
    pos_l = choices(pos_b, k=100)
    board = np.zeros((15, 15), dtype='int8')
    for i, pos in enumerate(pos_l):
        board[pos] = 1 - 2 * (i % 2)

    # Test scoring
    compute_move(board, pos_l[-1])
    set_trace()


def test_scan_kb():
    ptt = np.zeros(7, dtype='uint8')
    dp = [[], [], []]
    arr = np.array([1, 1, 0, 1, 0, 1, 0, 0, 1, 0], dtype='int8')
    pos = [(7, x) for x in range(len(arr))]
    scan_kb(arr, pos, ptt, dp)


if __name__ == '__main__':
    test_scan_kb()

