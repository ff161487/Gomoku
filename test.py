import numpy as np
from gmk_score import compute_move, scan_kbw, dist2points
from random import sample
from pdb import set_trace


def make_board():
    pos_b = [(x, y) for x in range(15) for y in range(15)]
    pos_l = sample(pos_b, k=100)
    board = np.zeros((15, 15), dtype='int8')
    for i, pos in enumerate(pos_l):
        board[pos] = 1 - 2 * (i % 2)

    # Test scoring
    score, dp = compute_move(board, pos_l[-1])
    points = dist2points(board)
    set_trace()


def test_scan_kbw():
    arr = np.array([1, 1, 1, 1, 0, -1, 0, 1, 0, 1, 0, 0, -1], dtype='int8')
    pos = [(7, x) for x in range(len(arr))]
    scan_kbw(arr, pos)


if __name__ == '__main__':
    make_board()

