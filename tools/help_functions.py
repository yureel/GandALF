import numpy as np


def rosenbrock(X):
    X = X[0]
    f = 0
    for i in range(X.shape[1]-1):
        f += 100*(X[i+1]-X[i]**2)**2+(1-X[i])**2
    print(f)
    return np.array([np.array([f])])


def pseudo_PR1ME(X):
    X = X[0]
    print(X)
    k = int(list(X[:3]).index(1.0)) + 1
    f = 100*k*np.exp((40000-X[4])/(8.314*X[3]))/(X[6]*(1+X[5]/10))
    return np.array([np.array([f])])
