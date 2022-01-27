import numpy as np
from GPyOpt.acquisitions.base import AcquisitionBase
import scipy
import math


class EMOC(AcquisitionBase):
    """
        General template to create a new GPyOPt acquisition function

        :param model: GPyOpt class of model
        :param space: GPyOpt class of domain
        :param optimizer: optimizer of the acquisition. Should be a GPyOpt optimizer
        :param cost_withGradients: function that provides the evaluation cost and its gradients

        """

    # --- Set this line to true if analytical gradients are available
    analytical_gradient_prediction = False

    def __init__(self, model, space, optimizer, X, pseudo_kernel, cost_withGradients=None, **kwargs):
        super(EMOC, self).__init__(model, space, optimizer)
        # self.optimizer = optimizer
        # self.model = model
        self.kernel = pseudo_kernel
        if model.noise_var == None:
            self.sigmaN = 0
        else:
            self.sigmaN = model.noise_var
        self.norm = 1
        # self.X = X
        self.X = np.copy(X)
        # print('update', self.X[-1])

    def gaussianAbsoluteMoment(self, muTilde, predVar):
        f11 = scipy.special.hyp1f1(-0.5 * self.norm, 0.5, -0.5 * np.divide(muTilde ** 2, predVar))
        prefactors = ((2 * predVar ** 2) ** (self.norm / 2.0) * math.gamma((1 + self.norm) / 2.0)) / np.sqrt(
            np.pi)

        return np.multiply(prefactors, f11)

    def calcEMOC(self, x):

        emocScores = np.asmatrix(np.empty([x.shape[0], 1], dtype=np.float))
        muTilde = np.asmatrix(np.zeros([x.shape[0], 1], dtype=np.float))

        kAll = self.kernel.K(np.vstack([self.X, x]))
        k = kAll[0:self.X.shape[0], self.X.shape[0]:]
        selfKdiag = np.asmatrix(np.diag(kAll[self.X.shape[0]:, self.X.shape[0]:])).T
        sigmaF = self.model.predict(x)[1]
        moments = np.asmatrix(self.gaussianAbsoluteMoment(np.asarray(muTilde), np.asarray(sigmaF)))

        term1 = 1.0 / (sigmaF + self.sigmaN)

        term2 = np.asmatrix(np.ones((self.X.shape[0] + 1, x.shape[0])), dtype=np.float) * (-1.0)
        term2[0:self.X.shape[0], :] = np.linalg.solve(
            self.kernel.K(self.X) + np.identity(self.X.shape[0], dtype=np.float) * self.sigmaN, k)

        preCalcMult = np.dot(term2[:-1, :].T, kAll[0:self.X.shape[0], :])
        for idx in range(x.shape[0]):
            vAll = term1[idx, :] * (preCalcMult[idx, :] + np.dot(term2[-1, idx].T, kAll[self.X.shape[0] + idx, :]))
            emocScores[idx, :] = np.mean(np.power(np.abs(vAll), self.norm))
        sol = np.multiply(emocScores, moments)
        sol = np.asarray(sol).reshape(-1)
        sol = np.array([sol]).reshape(-1, 1)
        return sol


    def _compute_acq(self, x):
        # --- DEFINE YOUR AQUISITION HERE (TO BE MAXIMIZED)
        #
        # Compute here the value of the new acquisition function. Remember that x is a 2D  numpy array
        # with a point in the domanin in each row. f_acqu_x should be a column vector containing the
        # values of the acquisition at x.
        #
        # print(self.calcEMOC(x).shape)
        return self.calcEMOC(x)


def gaussianAbsoluteMoment(muTilde, predVar, norm=1):
    f11 = scipy.special.hyp1f1(-0.5 * norm, 0.5, -0.5 * np.divide(muTilde ** 2, predVar))
    prefactors = ((2 * predVar ** 2) ** (norm / 2.0) * math.gamma((1 + norm) / 2.0)) / np.sqrt(
        np.pi)

    return np.multiply(prefactors, f11)


def calcEMOC(x, X, kernel, model, sigmaN, norm=1):

    emocScores = np.asmatrix(np.empty([x.shape[0], 1], dtype=np.float))
    muTilde = np.asmatrix(np.zeros([x.shape[0], 1], dtype=np.float))

    kAll = kernel.K(np.vstack([X, x]))
    k = kAll[0:X.shape[0], X.shape[0]:]
    selfKdiag = np.asmatrix(np.diag(kAll[X.shape[0]:, X.shape[0]:])).T
    sigmaF = model.predict(x)[1]
    moments = np.asmatrix(gaussianAbsoluteMoment(np.asarray(muTilde), np.asarray(sigmaF)))

    term1 = 1.0 / (sigmaF + sigmaN)

    term2 = np.asmatrix(np.ones((X.shape[0] + 1, x.shape[0])), dtype=np.float) * (-1.0)
    term2[0:X.shape[0], :] = np.linalg.solve(
        kernel.K(X) + np.identity(X.shape[0], dtype=np.float) * sigmaN, k)

    preCalcMult = np.dot(term2[:-1, :].T, kAll[0:X.shape[0], :])
    for idx in range(x.shape[0]):
        vAll = term1[idx, :] * (preCalcMult[idx, :] + np.dot(term2[-1, idx].T, kAll[X.shape[0] + idx, :]))
        emocScores[idx, :] = np.mean(np.power(np.abs(vAll), norm))
    sol = np.multiply(emocScores, moments)
    sol = np.asarray(sol).reshape(-1)
    sol = np.array([sol]).reshape(-1, 1)
    return sol
