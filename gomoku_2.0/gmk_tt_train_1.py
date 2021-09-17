import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pickle import load
from pdb import set_trace

DIR = "/data/home/frankf/code_1/GMK_TT/"


def train():
    with open(f"{DIR}training.data", 'rb') as f:
        y_tr, x_tr = load(f)
    n_stones = (x_tr != 0).sum(axis=(1, 2))
    y_o, x_o = y_tr[np.abs(y_tr) >= 100000], x_tr[np.abs(y_tr) >= 100000]
    """
    df = pd.DataFrame({'Y': y_tr, 'n_stones': n_stones})
    sns.pairplot(df, kind='kde')
    plt.show()
    """
    set_trace()


if __name__ == '__main__':
    train()