import numpy as np
from time import perf_counter
from pdb import set_trace


def find_seg(cond):
    scv = np.zeros(len(cond) + 2, dtype=bool)
    scv[0], scv[-1] = False, False
    scv[1:-1] = cond
    start = np.nonzero(cond & ~scv[:-2])[0]
    end = np.nonzero(cond & ~scv[2:])[0]
    return list(zip(start, end))


def time_nz():
    arr = np.random.randint(low=-1, high=2, size=15, dtype='int8')
    find_seg((arr > -1))
    set_trace()


if __name__ == '__main__':
    time_nz()
