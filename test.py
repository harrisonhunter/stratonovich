'''
1. Generate a bunch of random data from params
2. Initialize a model with random params
3. Train a model on that data
4. See if params are recovered
'''

import hmm
import numpy as np
import random
from scipy.stats import norm

'''
Data for initialization, used for regen testing
'''
d = 3
trans = [
	[0.6, 0.3, 0.1],
	[0.1, 0.8, 0.1],
	[0.1, 0.3, 0.6]
]
means = [-2, 0, 2]
std = 1
init = [.2, .6, .2]
ys = []
dists = [init]

def emission_probs(obs, state):
    ''' Prob density of observing obs given the current state'''
    return norm.pdf(obs, loc=means[state], scale=std)

def normalize(array):
    '''normalize and array'''
    summed = float(sum(array))
    return [i/summed for i in array]

def select_random(choices):
    '''pick a random element from a weighted list (pdf) (probs sum to i)'''
    upto = 0
    for i in xrange(len(choices)):
        if upto + choices[i] >= random.random():
            return i
        upto += choices[i]
    assert False, "Shouldn't get here"

'''Run tests'''
if __name__ == "__main__":
    for i in xrange(1000):
        dist = []
        emission = random.gauss(means[select_random(dists[-1])], std)
        ys.append(emission)
        for st in xrange(d):
            if i == 0:
                prev_sum = dists[-1][st]
            else:
                prev_sum = sum([dists[-1][k]*trans[k][st] for k in xrange(d)])
            dist.append(emission_probs(emission, st) * prev_sum)
        dists.append(normalize(dist))

    with open('test_data.txt', 'w') as f:
        for y in ys:
            f.write(str(y) + '\n')
    params = hmm.run_system('test.config', 100, False)
    end = [0 for _ in xrange(3)]
    num_dists = len(dists)
    for dist in dists:
        for i, x in enumerate(dist):
            end[i] += x / num_dists 
    print "avg dist:"
    print end
    print "end means"
    print params.means
    print "end trans"
    print params.trans
    print "end priors"
    print params.init_priors.sample()
    print "end beta"
    print params.init_beta.sample()
    print "end stds"
    print params.sigma

