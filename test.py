import numpy as np
from gmk_score_1 import compute_move, ptt_row, str_pos, sort_moves
from random import sample
from pdb import set_trace


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


def test_ptt_row():
    row = np.array([1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1])
    ptt_row(row, 0, 1)


def test_sort():
    mvs = ['H8', 'I7', 'G7', 'H7', 'I9', 'F6', 'J10']
    pos_l = [str_pos(x, 'to_pos') for x in mvs]
    board = np.zeros((15, 15), dtype='int8')
    for i, pos in enumerate(pos_l):
        board[pos] = 1 - 2 * (i % 2)

    # Test sorting
    pm_l_a = sort_moves(board, -1, 10)
    set_trace()


if __name__ == '__main__':
    # make_board()
    test_sort()
    # test_ptt_row()

