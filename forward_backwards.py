import numpy as np
from scipy.stats import norm

def forward_backward(transition_probs, means, std, initial_dist, emissions, d):
    def emission_probs(x, state):
        return norm.pdf(x, loc=means[state], scale=std)
    forward_dists = forward(transition_probs, emission_probs, initial_dist, emissions, d)
    return forward_dists
    # backward_dists = backward(transition_probs, emission_probs, emissions)
    # print backward_dists
    # return normalize(np.multiply(forward_dists, backward_dists))

def backward(transition_probs, emission_probs, emissions):
    num_states = 2
    dist = normalize(np.ones((1, num_states)))
    dists = [dist]
    for emission in reversed(emissions): 
        dists.append(normalize(transition_probs * np.dot(emission_probs(emission), dist.T).T))
    dists.reverse()
    return np.row_stack(dists)

def forward(transition_probs, emission_probs, initial_dist, emissions, d):
    dists = [initial_dist] 
    for i, emission in enumerate(emissions):
        dist = []
        for st in xrange(d):
            if i == 0:
                prev_sum = dists[-1][st]
            else:
                prev_sum = sum([dists[-1][k]*transition_probs[k][st] for k in xrange(d)])
            dist.append(emission_probs(emission, st) * prev_sum)
        dists.append(normalize(dist))
    return dists

def normalize(array):
    return array / sum(array)
