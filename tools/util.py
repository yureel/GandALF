import pandas as pd
import numpy as np
import GPy
from IPython.display import display
from optimizer import RProp

def read_data(datasheet):
    x = pd.read_csv(datasheet+'.csv')
    a = x.values
    inputs = a[:, :-1]
    output = a[:, -1]
    output = output.reshape(-1, 1)
    return inputs, output


def RMSE(Y1, Y2):
    if Y1.shape == Y2.shape:
        return np.sqrt(np.sum((Y1-Y2)**2)/np.size(Y1))
    else:
        print('Shape Y1 ', Y1.shape, ' is different from shape Y2 ', Y2.shape)


def MAE(Y1, Y2):
    if Y1.shape == Y2.shape:
        return np.sum(np.abs(Y1-Y2))/np.size(Y1)
    else:
        print('Shape Y1 ', Y1.shape, ' is different from shape Y2 ', Y2.shape)


def test_model(Xr, Yr, n, Xt, Yt, m):
    kernel = GPy.kern.RBF(input_dim=Xr.shape[1], ARD=True)
    m_random = GPy.models.GPRegression(Xr[:n], Yr[:n], kernel, normalizer=True)
    m_random.rbf.lengthscale = [1, 1, 1, 60, 15000, 10, 3, 500] # [1, 1, 1, 1, 1, 1, 1, 100]  # [1, 1, 1, 60, 15000, 10, 3, 500]
    m_random.optimize(RProp(max_iters=500), messages=True)
    m_random.optimize(messages=True)
    display(m_random)
    print(m_random.rbf.lengthscale)
    Yp_random = m_random.predict(Xr[:n])[0]
    Ytest_random = m_random.predict(Xt[:m])[0]
    print('training loss = ', RMSE(Yr[:n], Yp_random))
    print('test loss = ', RMSE(Yt[:m], Ytest_random))
    print('test MAE = ', MAE(Yt[:m], Ytest_random))
    unc = np.mean(np.sqrt(m_random.predict(Xr[:n])[1]))
    print('average uncertainty = ', unc)
    return m_random, kernel
