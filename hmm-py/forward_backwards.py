import numpy as np
from scipy.stats import norm

def forward_backward(transition_probs, means, std, initial_dist, emissions, d):
    def emission_probs(x, state):
        return norm.pdf(x, loc=means[state], scale=std)
    forward_dists = forward(transition_probs, emission_probs, initial_dist, emissions, d)
    print forward_dists[:10]
    backward_dists = backward(transition_probs, emission_probs, initial_dist, emissions, d)
    print backward_dists[:10]
    return forward_dists
    # return normalize(np.multiply(forward_dists, backward_dists))
''
def backward(transition_probs, emission_probs, initial_dist, emissions, d):
    bkw = []
    b_prev = []
    for i, emission in enumerate(reversed(emissions[1:])):
        b_curr = []
        for st in xrange(d):
            if i == 0:
                # base case for backward part
                b_curr.append(transition_probs[st][end_st])
            else:
                b_curr.append(sum(transition_probs[st][l]*emission_probs(emission, l)*b_prev[l] for l in states))
        bkw.insert(0,b_curr)
        b_prev = b_curr
    p_bkw = sum(initial_dist[l] * emission_probs(emissions[0],l) * b_curr[l] for l in states)
    return bkw
    # # merging the two parts
    # posterior = []
    # for i in range(L):
    #     posterior.append({st: fwd[i][st]*bkw[i][st]/p_fwd for st in states})

''
# def backward(transition_probs, emission_probs, emissions, d):
#     dist = normalize(np.ones((1, d)))
#     dists = [dist]
#     for emission in reversed(emissions):
#         dist = []
#         for st in xrange(d):
#             dist.append(normalize(transition_probs * np.dot(emission_probs(emission, st), dist.T).T))
#         dists.append(normalize(dist))
#     dists.reverse()
#     return np.row_stack(dists)

def forward(transition_probs, emission_probs, initial_dist, emissions, d):
    dists = [initial_dist]
    dist = []
    for st in xrange(d):
        prev_sum = dists[-1][st]
        dist.append(emission_probs(emissions[0], st) * prev_sum)
    dists.append(dist)
    for emission in emissions[1:]:
        dist = []
        for st in xrange(d):
            dist.append(emission_probs(emission, st) * sum([dists[-1][k]*transition_probs[k][st] for k in xrange(d)]))
        dists.append(normalize(dist))
    return dists

def normalize(array):
    return array / sum(array)
