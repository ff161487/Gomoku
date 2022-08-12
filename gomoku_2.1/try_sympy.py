import matplotlib.pyplot as plt
from sympy import Matrix, MatrixSymbol, MatrixExpr, Sum
from sympy.abc import i, j, k, l, N
from pdb import set_trace


def test():
    # plt.plot([[0, 1], [1, 0], [0, -1], [-1, 0]])
    plt.plot(x=[0, 1, 0, -1], y=[1, 0, -1, 0])
    plt.show()
    set_trace()
    A = MatrixSymbol("A", N, N, N)
    # a = MatrixSymbol("a", 3, 3)
    x = MatrixSymbol("x", 1, N)
    # y = MatrixSymbol("y", 3, 1)
    expr = Sum(A[i, j, k] * x[0, i] * x[0, j] * x[0, k], (i, 0, N - 1), (j, 0, N - 1), (k, 0, N - 1))
    expr_m = MatrixExpr.from_index_summation(expr)
    set_trace()


if __name__ == '__main__':
    test()