from easyAI import AI_Player, Negamax, Human_Player
from gomoku_2 import Gomoku
from pdb import set_trace


def play_gomoku():
    ply_1 = Human_Player()
    ply_2 = AI_Player(Negamax(4))
    game = Gomoku([ply_1, ply_2], moves=['H8', 'I7'], show='play')
    game.play()
    set_trace()


if __name__ == '__main__':
    play_gomoku()
