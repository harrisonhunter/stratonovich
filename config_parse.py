'''
Config File defined strictly as:
Comment
data path
# of hidden states
# of observed vars
which variables
method
path to prior file
#of states of observed vars

parse config
@params: the path to a config file
@returns: a dictionary with config fields as keys and the corresponding
values in the config file as values
'''
import numpy as np
from update_methods import Dirichlet, Normal, Gamma
from random import choice

class Parameters:
    def __init__(self, config, ys, n):
        self.config = config
        self.d = config['h_states']
        ones = [1 for i in xrange(self.d)]
        self.y = ys
        self.n = n
        self.minYk = min(ys)
        self.maxYk = max(ys)
        self.epsilon = (self.minYk + self.maxYk) / 2.0
        self.r = self.maxYk - self.minYk
        self.k = 1.0 / self.r**2
        self.alpha = 2.0
        self.g = 0.2
        self.h = 10.0 / self.r**2
        self.init_priors = Dirichlet(ones)
        self.init_beta = Gamma(self.g, self.h)
        self.init_root_sigma = Gamma(self.alpha, self.init_beta.sample())
        self.init_means = Normal(self.epsilon, self.k**-1)
        self.init_trans = [Dirichlet(ones) for i in xrange(self.d)]
        self.x = [choice(xrange(config['h_states'])) for i in xrange(self.n)]

    def set_initial_params(self):
        self.priors = self.init_priors.sample()
        self.beta = self.init_beta.sample()
        self.sigma = self.init_root_sigma.sample() ** (-1.0/2)
        print "starting stds = " + str(self.sigma)
        self.means = [self.init_means.sample() for i in xrange(self.d)]
        self.trans = [self.init_trans[i].sample() for i in xrange(self.d)]


def parse_config(path_to_config):
    config_fields = ['comment', 'data_path', 'h_states', 'o_vars', 'which_vars', 'method', 'prior', 'o_states']
    content = [line.strip().split(" ")[1] for line in open(path_to_config)]
    content = [int(content[i]) if i in [2, 3, 7] else [int(i) for i in content[4].split(',')] if i ==4 else content[i] for i in xrange(len(content))]
    return dict(zip(config_fields, content))

def load_data(config, n=1000, test=True):
    if test:
        return [choice(xrange(config['h_states'])) for i in xrange(n)]
    else:
        with open(config['data_path']) as f:
            out = [line.rstrip('\n') for line in f]
            return [float(i) for i in out]

def create_params_object(config, test=True):
    n = 1000
    ys = load_data(config, n, test)
    if not test: n = len(ys)
    params = Parameters(config, ys, n)
    return params
