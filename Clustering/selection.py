import GPy
from optimizer import RProp
import numpy as np
from acquisitions import calcEMOC
from sklearn.cluster import KMeans
import random


def select_uncertainty(pool, X, Y, lower_bound, upper_bound):
    kernel = GPy.kern.RBF(input_dim=X.shape[1], ARD=True)
    model = GPy.models.GPRegression(X, Y, kernel, normalizer=True)
    kernel.lengthscale = list((lower_bound + upper_bound)/2)
    model.optimize(RProp(), messages=True)
    model.optimize(messages=True, max_iters=5000)
    print(kernel.lengthscale)
    print(kernel.variance)
    var = model.predict(pool)[1]
    return pool[np.argmax(var)]


def select_EMOC(pool, X, Y, lower_bound, upper_bound):
    kernel = GPy.kern.RBF(input_dim=X.shape[1], ARD=True)
    model = GPy.models.GPRegression(X, Y, kernel, normalizer=True)
    kernel.lengthscale = list((lower_bound + upper_bound)/2)
    model.optimize(RProp(max_iters=250), messages=True)
    model.optimize(messages=True, max_iters=5000)
    print(kernel.lengthscale)
    print(kernel.variance)
    sigmaN = model.Gaussian_noise[0]
    var = calcEMOC(pool, X, kernel, model, sigmaN)
    return pool[np.argmax(var)], kernel.lengthscale


def select_center(pool, cluster, new_cluster):
    var = cluster.transform(pool)[:, new_cluster]
    return pool[np.argmin(var)]


def select_random(pool):
    return random.choice(pool)

