from easyAI import AI_Player, Negamax, TranspositionTable
from gomoku_2 import Gomoku
from pdb import set_trace

DIR = "/data/home/frankf/code_1/GMK_TT/"


def gomoku_AI_run():
    table = TranspositionTable()
    table.from_file(f"{DIR}tt_g.data")
    print(len(table.d))
    ai_1 = AI_Player(Negamax(4, tt=table))
    ai_2 = AI_Player(Negamax(4, tt=table))
    game = Gomoku([ai_1, ai_2], moves=['H8', 'I7', 'G7', 'I9', 'G6'])
    game.play()
    print(len(table.d))
    set_trace()


if __name__ == '__main__':
    gomoku_AI_run()