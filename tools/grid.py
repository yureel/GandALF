import numpy as np


def grid(n):
    """
    X = np.meshgrid(np.linspace(575, 685, n), np.linspace(40000, 70000, n), np.linspace(10, 16, n),
                    np.linspace(0.75, 3.5, n), np.linspace(300, 800, n))
    """
    X = np.meshgrid(np.linspace(575, 685, n), np.linspace(70000, 40000, n), 10, 0.75, 800)
    X = np.array(X).reshape(5, -1).T
    return X


def select_grid_TH(X):
    j = 0
    for i in range(X.shape[0]):
        i = i-j
        if 384.615*X[i, 0]-X[i, 1]-198461 > 0:
            X = np.delete(X, i, 0)
            j += 1
    return X


def full_grid(n, step):
    L = []
    for i in range(n):
        L.append(np.arange(0.0, 1.00001, step))
    a = np.meshgrid(*L)
    m = np.array(a).reshape(n, -1).T
    j = 0
    for i in range(len(m)):
        if sum(m[i - j]) > 1:
            m = np.delete(m, i - j, 0)
            j += 1
    return m
