import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pickle import load
from pdb import set_trace

DIR = "/data/home/frankf/code_1/GMK_TT/"


def train():
    with open(f"{DIR}train.data", 'rb') as f:
        y_tr, x_tr = load(f)
    n_stones = (x_tr != 0).sum(axis=(1, 2))
    y_5, x_5 = y_tr[y_tr >= 50000], x_tr[y_tr >= 50000]
    y_1, x_1 = y_tr[y_tr == 2.5], x_tr[y_tr == 2.5]
    """
    df = pd.DataFrame({'Y': y_tr, 'n_stones': n_stones})
    sns.pairplot(df, kind='kde')
    plt.show()
    """
    set_trace()


if __name__ == '__main__':
    train()