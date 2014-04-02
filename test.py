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
    # print norm.pdf(obs, loc=means[state], scale=std)
    return norm.pdf(obs, loc=means[state], scale=std)

def normalize(array):
    summed = float(sum(array))
    return [i/summed for i in array]
    # return array / sum(array)

def select_random(ind, array):
    # print ind, array
    if ind < array[0]:
        # print "here"
        return 0
    for i in xrange(len(array)):
        if ind >= array[i]:
            if i != len(array) - 1:
                if ind < array[i+1]:
                    # print "this one"
                    # print 
                    return i + 1
                else:
                    continue
            else:
                # print "here"
                return i
    # print "end"
    return len(array) - 1

def select_random(choices):
    # print choices
    # total = sum(w for w in choices)
    # r = random.random()
    upto = 0
    for i in xrange(len(choices)):
        if upto + choices[i] >= random.random():
            return i
        upto += choices[i]
    assert False, "Shouldn't get here"



for i in xrange(100):
    # print dists
    dist = []
    emission = random.gauss(means[select_random(dists[-1])], std)
    ys.append(emission)
    for st in xrange(d):
        if i == 0:
            prev_sum = dists[-1][st]
        else:
            prev_sum = sum([dists[-1][k]*trans[k][st] for k in xrange(d)])
        # print d, prev_sum
        dist.append(emission_probs(emission, st) * prev_sum)
    dists.append(normalize(dist))

 #    cumlatives = [np.cumsum(prob) for prob in dists[-1]]
	# emission = select_random(dists[-1])
	# ys.append(emission)
	# dists.append(normalize(dists[-1]*trans emission_probs(emission)))

SEE IF WE CAN RECOVER PARAMS NOW THAT WE HAVE GENERATED DATA

print ys
print dists

