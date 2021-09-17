import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from easyAI import TwoPlayerGame
from gmk_score_2 import str_pos, compute_move, sort_moves
from pdb import set_trace

plt.ion()


class Gomoku(TwoPlayerGame):
    def __init__(self, players, moves=[], show="invisible"):
        self.players = players
        self.board = np.zeros((15, 15), dtype='int8')
        if len(moves) > 0:
            for i in range(len(moves)):
                pos = str_pos(moves[i], 'to_pos')
                self.board[pos[0], pos[1]] = 1 - 2 * (i % 2)
        self.current_player = 1 + len(moves) % 2  # which player starts depends on the length of moves.
        self.moves = moves  # Record players' moves.
        self.scores = []
        self.display = show

    def possible_moves(self):
        if len(self.moves) == 0:
            return ['H8']
        else:
            ply_stone = self.opponent_index - self.current_player
            pm_l = sort_moves(self.board, ply_stone, self.player.name)
            return pm_l

    def make_move(self, move):
        # Compute score and change board
        ply_stone = self.opponent_index - self.current_player
        pos = str_pos(move, 'to_pos')
        sc_a, sc_d = compute_move(self.board, pos, ply_stone)
        sc = sc_a + 0.5 * sc_d
        self.scores.append(sc)
        self.board[pos[0], pos[1]] = ply_stone

        # Append to move list
        self.moves.append(move)

    def unmake_move(self, move):
        # Change board
        pos = str_pos(move, 'to_pos')
        self.board[pos[0], pos[1]] = 0

        # Delete the latest score added
        del self.scores[-1]

        # Delete the move added
        self.moves.remove(move)

    def ttentry(self):
        return "-".join(sorted(self.moves[0::2])) + '_' + "-".join(sorted(self.moves[1::2]))

    def show(self):
        if self.display == "play":
            pos_l = np.array([(ord(x[0]) - 65, int(x[1:]) - 1) for x in self.moves])
            ann = np.arange(len(pos_l)) + 1
            c_s = [['w', 'k'][x] for x in ann % 2]
            c_t = [['k', 'w'][x] for x in ann % 2]
            plt.close()
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
        elif self.display == "test":
            df_b = pd.DataFrame(self.board, columns=[chr(65 + x) for x in range(15)], index=list(range(15, 0, -1)))
            print(df_b)

    def is_over(self):
        if len(self.scores) > 0:
            return (len(self.moves) >= 225) or self.scores[-1] >= 100000
        else:
            return False

    def scoring(self):
        return self.scores[-1]

