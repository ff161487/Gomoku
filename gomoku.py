import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from easyAI import TwoPlayerGame
from gmk_score import str_pos, dist2points, compute_move
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
        self.current_player = 1  # player 1 starts.
        self.moves = moves  # Record players' moves.
        self.dp = []  # Record defence points at each step
        self.scores = []
        self.display = show

    def possible_moves(self):
        if len(self.moves) == 0:
            return ['H8']
        else:
            # Get defence points at last move
            pm_l = dist2points(self.board)
            if len(self.dp) > 0:
                dp_ply, dp_op = self.dp[-1][self.current_player - 1], self.dp[-1][self.opponent_index - 1]
                # For now, we only focus on defense of 'Five'
                dp_ply = [x for x in dp_ply.split('|')[0].split('_') if x != '']
                dp_op = [x for x in dp_op.split('|')[0].split('_') if x != '']
                if len(dp_ply) > 0:
                    return dp_ply
                elif len(dp_op) > 0:
                    return dp_op
            return pm_l

    def make_move(self, move):
        # Change board
        pos = str_pos(move, 'to_pos')
        self.board[pos[0], pos[1]] = self.opponent_index - self.current_player

        # Compute score
        sc, dp = compute_move(self.board, pos)
        self.scores.append(sc)

        # Update defense points
        dp_new = ['___|___', '___|___']
        dp_new[self.current_player - 1] = dp
        # We need to update last step's defense points since the second step
        if len(self.dp) > 0:
            # The update is focus on opponent's defense points
            dp_op_old = self.dp[-1][self.opponent_index - 1]
            # For now, we only focus on defense of 'Five'
            dp_op_old = [x for x in dp_op_old.split('|')[0].split('_') if x != '']
            dp_op_new = [x for x in dp_op_old if move not in x]
            dp_op_new = '_'.join(dp_op_new) + '|___'
            dp_new[self.opponent_index - 1] = dp_op_new
        self.dp.append(tuple(dp_new))

        # Append to move list
        self.moves.append(move)

    def unmake_move(self, move):
        # Change board
        pos = str_pos(move, 'to_pos')
        self.board[pos[0], pos[1]] = 0

        # Delete the latest score added
        del self.scores[-1]

        # Delete the defense points added
        del self.dp[-1]

        # Delete the move added
        self.moves.remove(move)

    def ttentry(self):
        return "".join(self.moves)

    def show(self):
        if self.display == "play":
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
        elif self.display == "test":
            df_b = pd.DataFrame(self.board, columns=[chr(65 + x) for x in range(15)], index=list(range(15, 0, -1)))
            print(df_b)

    def is_over(self):
        if len(self.scores) > 0:
            return (len(self.moves) >= 225) or self.scores[-1] >= 100000

    def scoring(self):
        return self.scores[-1]

