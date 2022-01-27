import numpy as np
import GPyOpt

def discrete_constraints_8d(x):
    for i in range(x.shape[0]):
        a = np.argmax(x[i, 0:3])
        x[i, :3] = np.zeros(3)
        x[i, a] = 1
    return x


def normalizer(x, lower_bound, upper_bound):
    x = (x - lower_bound)/(upper_bound-lower_bound)
    return x


def denormalizer(x, lower_bound, upper_bound):
    x = x*(upper_bound-lower_bound) + lower_bound
    return x


def rescale(x, lengthscale, lower_bound, upper_bound):
    x = normalizer(x, lower_bound, upper_bound)/np.array([1, 1, 1, 0.8, 1, 1, 1, 1])
    # x = normalizer(x)/lengthscale*np.array([1, 1, 1, 110, 30000, 6, 2.75, 500])
    return x


def descale(x, lengthscale, lower_bound, upper_bound):
    # x = x*lengthscale/np.array([1, 1, 1, 110, 30000, 6, 2.75, 500])
    x = x*np.array([1, 1, 1, 0.8, 1, 1, 1, 1])
    x = denormalizer(x, lower_bound, upper_bound)
    return x


"""
spacelist = [{'name': 'Feed 1', 'type': 'discrete', 'domain': (0, 1)},
             {'name': 'Feed 2', 'type': 'discrete', 'domain': (0, 1)},
             {'name': 'Feed 3', 'type': 'discrete', 'domain': (0, 1)},
             {'name': 'TRO2', 'type': 'continuous', 'domain': (575, 685)},
             {'name': 'Hprot2', 'type': 'continuous', 'domain': (40000, 70000)},
             {'name': 'PRO2', 'type': 'continuous', 'domain': (10, 16)},
             {'name': 'LHSV2', 'type': 'continuous', 'domain': (0.75, 3.5)},
             {'name': 'H2/HC_2', 'type': 'continuous', 'domain': (300, 800)}
             ]
constraints = [{'name': 'const_1', 'constraint': '384.615*x[:,3]-x[:,4]-198461'},
               {'name': 'const_2', 'constraint': 'x[:,0]+x[:,1]+x[:,2]-1.1'},
               {'name': 'const_3', 'constraint': '-x[:,0]-x[:,1]-x[:,2]+0.9'}
               ]
min_values = np.array([0, 0, 0, 575, 40000, 10, 0.75, 300])
max_values = np.array([1, 1, 1, 685, 70000, 16, 3.5, 800])

space = GPyOpt.Design_space(space=spacelist, constraints=constraints)
pool = GPyOpt.experiment_design.initial_design('random', space, 10)
print(pool)
lengthscale = np.array([5, 10, 5500, 41, 15000, 15, 30, 50000])
pool = normalizer(pool, min_values, max_values)
print(pool)
pool = denormalizer(pool, min_values, max_values)
print(pool)
"""
