from easyAI import AI_Player, Negamax, TT
from gomoku import Gomoku
from pdb import set_trace


def play_gomoku():
    table = TT()
    ai_1 = AI_Player(Negamax(4, tt=table))
    ai_2 = AI_Player(Negamax(4, tt=table))
    game = Gomoku([ai_1, ai_2], moves=['H8', 'I7'])
    game.play()
    set_trace()


if __name__ == '__main__':
    play_gomoku()
