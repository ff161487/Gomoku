import numpy as np
from pdb import set_trace

# 'sp' for 'starting point', 'loc' for 'location', 'dfl' for 'default'
dfl_sp_loc = np.array([10000, 10000])

# 'drc' for 'direction', '_l' suffix for 'list', '_a' suffix for 'array'
drc_a = np.array([[0, 1], [-1, 1], [-1, 0], [-1, -1], [0, -1], [1, -1], [1, 0], [1, 1]])

# 'ln' for 'line', 'pat' for 'pattern'
ln_pat_l = {
    'BF_D': ['W0|B0|B0|B0|B1|W2', 'W0|B0|B0|B1|B0|W2', 'W0|B0|B0|B0|W2|B1', 'W0|B0|B0|W2|B0|B1', 'W0|B0|B0|W2|B0|B1',
             'W0|B0|B0|W2|B1|B0', 'W0|B0|W2|B0|B0|B1', 'W0|B0|W2|B1|B0|B0', 'W0|B0|W2|B0|B1|B0',
             'W0|B1|W2|B0|.|B0|.|B0|W0', 'W0|B1|.|B0|W2|B0|.|B0|W0', 'W0|B1|.|B0|.|B0|W2|B0|W0',
             'W0|B0|W2|B1|.|B0|.|B0|W0', 'W0|B0|.|B1|W2|B0|.|B0|W0', 'W0|B0|.|B1|.|B0|W2|B0|W0'],
    'OT_D': ['W2|B1|B0|B0', 'B1|B0|B0|W2', 'W2|B0|B1|B0', ], 'BF_W': [], 'OT_W': []}

if __name__ == '__main__':
    set_trace()
