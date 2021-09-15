from cprofile_graph import profile_decorator
from easyAI import AI_Player, Negamax, TranspositionTable
from gomoku_2 import Gomoku


@profile_decorator('prof.png')
def gomoku_AI_run():
    table = TranspositionTable()
    ai_1 = AI_Player(Negamax(2, tt=table))
    ai_2 = AI_Player(Negamax(2, tt=table))
    game = Gomoku([ai_1, ai_2], moves=['H8', 'I7', 'G7', 'I9', 'G6'])
    game.play()


if __name__ == '__main__':
    gomoku_AI_run()
