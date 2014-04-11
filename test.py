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
    return norm.pdf(obs, loc=means[state], scale=std)

def normalize(array):
    summed = float(sum(array))
    return [i/summed for i in array]

def select_random(ind, array):
    if ind < array[0]:
        return 0
    for i in xrange(len(array)):
        if ind >= array[i]:
            if i != len(array) - 1:
                if ind < array[i+1]:
                    return i + 1
                else:
                    continue
            else:
                return i
    return len(array) - 1

def select_random(choices):
    upto = 0
    for i in xrange(len(choices)):
        if upto + choices[i] >= random.random():
            return i
        upto += choices[i]
    assert False, "Shouldn't get here"


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
    params = hmm.run_system('test.config', 1000, False)
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

