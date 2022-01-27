from GPyOpt.acquisitions.base import AcquisitionBase


class AcquisitionAL(AcquisitionBase):
    """
    General template to create a new GPyOPt acquisition function

    :param model: GPyOpt class of model
    :param space: GPyOpt class of domain
    :param optimizer: optimizer of the acquisition. Should be a GPyOpt optimizer
    :param cost_withGradients: function that provides the evaluation cost and its gradients

    """

    # --- Set this line to true if analytical gradients are available
    analytical_gradient_prediction = False

    def __init__(self, model, space, optimizer, cost_withGradients=None, **kwargs):
        self.optimizer = optimizer
        super(AcquisitionAL, self).__init__(model, space, optimizer)

    def _compute_acq(self, x):
        # --- DEFINE YOUR AQUISITION HERE (TO BE MAXIMIZED)
        #
        # Compute here the value of the new acquisition function. Remember that x is a 2D  numpy array
        # with a point in the domanin in each row. f_acqu_x should be a column vector containing the
        # values of the acquisition at x.
        #
        m, s = self.model.predict(x)
        f_acqu_x = s

        return f_acqu_x

    def _compute_acq_withGradients(self, x):
        # --- DEFINE YOUR AQUISITION (TO BE MAXIMIZED) AND ITS GRADIENT HERE HERE
        #
        # Compute here the value of the new acquisition function. Remember that x is a 2D  numpy array
        # with a point in the domanin in each row. f_acqu_x should be a column vector containing the
        # values of the acquisition at x. df_acqu_x contains is each row the values of the gradient of the
        # acquisition at each point of x.
        #
        # NOTE: this function is optional. If note available the gradients will be approxiamted numerically.
        m, s, dmdx, dsdx = self.model.predict_withGradients(x)
        f_acqu_x = s
        df_acqu_x = dsdx
        return f_acqu_x, df_acqu_x
