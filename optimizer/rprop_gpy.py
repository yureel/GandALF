from .rprop import Rprop
from GPy.inference.optimization import Optimizer


class RProp(Optimizer):
    # We want the optimizer to know some things in the Optimizer implementation:
    def __init__(self, step_shrink=0.5, step_grow=1.2, min_step=1e-06, max_step=1, changes_max=0.1, *args,
                 **kwargs):
        super(RProp, self).__init__(*args, **kwargs)
        self.opt_name = 'RProp (climin)'
        self.step_shrink = step_shrink
        self.step_grow = step_grow
        self.min_step = min_step
        self.max_step = max_step
        self.changes_max = changes_max

    def opt(self, x_init, f_fp=None, f=None, fp=None):
        # We only need the gradient of the
        assert not fp is None

        # Do the optimization, giving previously stored parameters
        opt = Rprop(x_init, fp,
                                 step_shrink=self.step_shrink, step_grow=self.step_grow,
                                 min_step=self.min_step, max_step=self.max_step,
                                 changes_max=self.changes_max)

        # Get the optimized state and transform it into Paramz readable format by setting
        # values on this object:
        # Important ones are x_opt and status:
        for info in opt:
            if info['n_iter'] >= self.max_iters:
                self.x_opt = opt.wrt
                self.status = 'maximum number of function evaluations exceeded'
                break
