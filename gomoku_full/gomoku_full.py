import numpy as np
import matplotlib.pyplot as plt
from easyAI import TwoPlayerGame
from gmk_score import str_pos, dsc, find_five
from pdb import set_trace

plt.ion()


class Gomoku(TwoPlayerGame):
    def __init__(self, players, moves=[], show=False):
        self.players = players
        self.board = np.zeros((15, 15), dtype='int8')
        if len(moves) > 0:
            for i in range(len(moves)):
                pos = str_pos(moves[i], 'to_pos')
                self.board[pos[0], pos[1]] = 1 - 2 * (i % 2)
        self.nplayer = 1  # player 1 starts.
        self.moves = moves  # Record players' moves.
        self.scores = []
        self.display = show

    def possible_moves(self):
        if len(self.moves) == 0:
            return ['H8']
        else:
            pm_l = []
            for pos in zip(*np.where(self.board != 0)):
                pm_l.extend(list((pos + oct_d)))
                pm_l.extend(list((pos + 2 * oct_d)))
            pm_l = [x for x in pm_l if legal(x)]
            pm_l = [x for x in pm_l if self.board[x[0], x[1]] == 0]
            pm_l = list(set([str_pos(x, 'to_str') for x in pm_l]))
            return pm_l

    def make_move(self, move):
        # Change board
        pos = str_pos(move, 'to_pos')
        self.board[pos[0], pos[1]] = self.nopponent - self.nplayer

        # Compute score
        sc_d = dsc(self.board, pos)
        self.scores.append(sc_d)

        # Append to move list
        self.moves.append(move)

    def unmake_move(self, move):
        # Change board
        pos = str_pos(move, 'to_pos')
        self.board[pos[0], pos[1]] = 0

        # Undo score change
        del self.scores[-1]

        # Undo move list change
        self.moves.remove(move)

    def ttentry(self):
        return "".join(self.moves)

    def show(self):
        if self.display:
            pos_l = np.array([(ord(x[0]) - 65, int(x[1:]) - 1) for x in self.moves])
            ann = np.arange(len(pos_l)) + 1
            c_s = [['w', 'k'][x] for x in ann % 2]
            c_t = [['k', 'w'][x] for x in ann % 2]
            fig, ax = plt.subplots(figsize=(16, 9))
            ax.set_aspect(1)
            ax.set_facecolor('bisque')
            ax.set_xlim(0, 14)
            ax.set_ylim(0, 14)
            ax.set_xticks(np.arange(15))
            ax.set_yticks(np.arange(15))
            ax.set_xticklabels([chr(65 + x) for x in range(15)])
            ax.set_yticklabels(np.arange(1, 16))
            ax.grid(b=True, which='both', c='k')
            ax.scatter(pos_l[:, 0], pos_l[:, 1], c=c_s, s=1000, zorder=2)
            for i, label in enumerate(ann):
                ax.text(pos_l[i, 0], pos_l[i, 1], label, c=c_t[i], ha='center', va='center', size='large')
            plt.show()

    def is_over(self):
        return (len(self.moves) >= 225) or find_five(self.board, self.nopponent)

    def scoring(self):
        sc = self.scores[-1]
        sc = sc[self.nplayer - 1] - sc[self.nopponent - 1]
        return sc

