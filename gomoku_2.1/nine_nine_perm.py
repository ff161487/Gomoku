from itertools import combinations
from sympy.combinatorics import Permutation
from sympy import eye, Matrix
from pdb import set_trace


# noinspection PyPep8Naming
def rp_perm(k=2):
    # Step 1: Generate polynomial basis
    x_l = [f"x_{i}" for i in range(9)]
    m_l = [' * '.join(sorted(m)) for m in combinations(x_l, k)]

    # Step 2: Find matrix representation of group generators
    a = Permutation(1, 3, 5, 7)(2, 4, 6, 8)
    b = Permutation(1, 5)(2, 4)(6, 8)
    x_l_a, x_l_b = a(x_l), b(x_l)
    m_l_a = [' * '.join(sorted(m)) for m in combinations(x_l_a, k)]
    m_l_b = [' * '.join(sorted(m)) for m in combinations(x_l_b, k)]
    a_p = [m_l.index(x) for x in m_l_a]
    b_p = [m_l.index(x) for x in m_l_b]
    a_p, b_p = Permutation(a_p), Permutation(b_p)

    # Step 3: Find common eigenvectors with unit eigenvalue
    idm = eye(len(m_l))
    AT, BT = idm.permute(a_p).T, idm.permute(b_p).T
    M = Matrix([[idm - AT], [idm - BT]])
    null_vec = [vec.T for vec in M.nullspace()]
    m_l_m = Matrix(m_l)
    inv_poly_base = [n_v.dot(m_l_m) for n_v in null_vec]
    return inv_poly_base


if __name__ == '__main__':
    rst = rp_perm(k=3)
    set_trace()
