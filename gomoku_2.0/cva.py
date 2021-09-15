# Import necessary modules
import pandas as pd
import numpy as np
from pdb import set_trace

DIR = "/data/home/frankf/code_1/GMK_TT/"
N_FOLD = 10


def model_selection():
    df = pd.read_csv(f'{DIR}gscv_rt.csv', header=0, index_col=0)
    df.sort_values(by='mean_train_score', inplace=True)
    lst = ['split' + str(x) + '_train_score' for x in range(N_FOLD)]
    tr_sc = df[lst]
    tr_sc.columns = list(range(N_FOLD))
    lst = ['split' + str(x) + '_test_score' for x in range(N_FOLD)]
    ts_sc = df[lst]
    ts_sc.columns = list(range(N_FOLD))
    m_diff = (df['mean_train_score'] - df['mean_test_score']).values
    s_diff = (tr_sc - ts_sc).std(axis=1).values
    t_stat = np.divide(m_diff * np.sqrt(N_FOLD), s_diff, out=np.zeros_like(m_diff),
                       where=s_diff != 0)
    t_stat = pd.Series(t_stat, name='t_stat')
    cvr = df[['params', 'mean_train_score', 'mean_test_score']]
    cvr.index = list(range(cvr.shape[0]))
    cvr = pd.concat([cvr, t_stat], axis=1)
    cvr = cvr.dropna()
    params = [eval(x) for x in cvr['params']]
    params = pd.DataFrame.from_records(params)
    cvr = pd.concat([params, cvr.iloc[:, 1:]], axis=1)
    cvr.sort_values(by='mean_test_score', inplace=True)
    set_trace()
    cvr = cvr.loc[cvr['t_stat'] <= 7.8, :]
    id_max = cvr['mean_test_score'].idxmax()
    print(cvr.loc[id_max, :])
    set_trace()


if __name__ == "__main__":
    model_selection()
