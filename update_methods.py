'''
All the update methods for gibbs sampling
Includes all the distributions we are using

Specifically:
Gaussian
Dirichlet
Weibull
'''

import numpy.random as npr

class Normal:
    def __init__(self, init_mean, init_std):
        self.mean = init_mean
        self.std = init_std

    def sample(self):
        '''
        loc : float
        Mean ("centre") of the distribution.
        scale : float
        Standard deviation (spread or "width") of the distribution.
        size : tuple of ints
        Output shape. If the given shape is, e.g., (m, n, k), 
        then m * n * k samples are drawn.
        '''
        return npr.normal(loc=self.mean, scale=self.std, size=None)

class Dirichlet:
    def __init__(self, init_alpha):
        self.alpha = init_alpha

    def sample(self):
        '''
        alpha : array
        Parameter of the distribution (k dimension for sample of dimension k).
        size : array
        Number of samples to draw.
        '''
        return npr.dirichlet(self.alpha, size=None)

class Weibull:
    def __init__(self, init_a):
        self.a = init_a

    def sample(self):
        ''' a : float
        Shape of the distribution.
        size : tuple of ints
        Output shape. If the given shape is, e.g., (m, n, k),
        then m * n * k samples are drawn.
        '''
        return npr.weibull(self.a, size=None)

class Gamma:
    def __init__(self, init_shape, init_scale):
        self.shape = init_shape
        self.scale = init_scale

    def sample(self):
        '''shape : scalar > 0
        The shape of the gamma distribution.
        scale : scalar > 0, optional
        The scale of the gamma distribution. Default is equal to 1.
        size : shape_tuple, optional
        Output shape. If the given shape is, e.g., (m, n, k),
        then m * n * k samples are drawn.
        '''
        return npr.gamma(self.shape, self.scale, size=None)

class UpdateFunctions():
    def __init__(self, params):
        self.params = params

    def get_I(self, i):
        return sum([1 if self.params.x[0] == i else 0])

    def get_n(self, i):
        return sum([1 for k in xrange(self.params.n) if self.params.x[k] == i ])

    def get_n_trans(self, i, j):
        return sum([1 for k in xrange(self.params.n) if self.params.x[k-1] == i and self.params.x[k] == j])

    def get_s(self, i):
        return 1

    def eq_1(self):
        Is = [self.get_I(i) for i in xrange(self.params.d)]
        return Dirichlet([Is[i] + 1 for i in xrange(self.params.d)]).sample()

    def eq_2(self, i):
        ns = [self.get_n_trans(i, j) for j in xrange(self.params.d)]
        return Dirichlet([ns[j] + 1 for j in xrange(self.params.d)]).sample()

    def eq_3(self, i):
        mean = (self.get_s(i) + self.params.k * self.params.epsilon * self.params.sigma**2) / (1.0 * self.get_n(i) + self.params.k * self.params.sigma**2)
        std = (self.params.sigma**2) / (self.get_n(i) + self.params.k * self.params.sigma**2)
        return Normal(mean, std).sample()

    def eq_4(self):
        shape = self.params.alpha + self.params.n / 2.0
        a = sum([(self.params.y[k] - self.params.means[self.params.x[k]])**2 for k in xrange(1, self.params.n)])
        scale = self.params.beta + a / 2.0
        return Gamma(shape, scale).sample()

    def eq_5(self):
        shape = self.params.g + self.params.alpha
        scale = self.params.h + self.params.sigma**-2
        return Gamma(shape, scale).sample()

    def eq_6(self):
        pass

    def eq_7(self, i):
        pass
