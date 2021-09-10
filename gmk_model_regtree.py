import pandas as pd
from pickle import load
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import GridSearchCV
from pdb import set_trace

DIR = "/data/home/frankf/code_1/GMK_TT/"


def train_rt():
    with open(f"{DIR}training.data", 'rb') as f:
        mat_tr = load(f)
    X, y = mat_tr[:, 1:], mat_tr[:, 0]
    m_d = [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    msl = [0.0001, 0.0002, 0.0005, 0.001, 0.002, 0.005, 0.01, 0.02, 0.05, 0.1]
    param = {'max_depth': m_d, 'min_samples_leaf': msl}
    mdl = DecisionTreeRegressor(random_state=0)
    gs = GridSearchCV(mdl, param, scoring='r2', n_jobs=-1, cv=10, verbose=10,
                      return_train_score=True)
    gs.fit(X=X, y=y)
    rst = pd.DataFrame(gs.cv_results_)
    rst.to_csv(f'{DIR}gscv_rt.csv')


if __name__ == '__main__':
    train_rt()


