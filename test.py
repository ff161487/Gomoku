import numpy as np
from gmk_score import compute_move
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


if __name__ == '__main__':
    make_board()

