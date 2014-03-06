import numpy as np
from scipy.stats import norm

def forward_backward(transition_probs, means, std, initial_dist, emissions, d):
    def emission_probs(x):
        return np.array([norm.pdf(x, loc=means[i], scale=std) for i in xrange(d)])
    forward_dists = forward(transition_probs, emission_probs, initial_dist, emissions)
    return forward_dists
    # backward_dists = backward(transition_probs, emission_probs, emissions)
    # print backward_dists
    # return normalize(np.multiply(forward_dists, backward_dists))

def backward(transition_probs, emission_probs, emissions):
    num_states = 2
    dist = normalize(np.ones((1,num_states)))
    dists = [dist]
    for emission in reversed(emissions): 
        print normalize(transition_probs * np.dot(emission_probs(emission), dist.T))
        dists.append(normalize(transition_probs * np.dot(emission_probs(emission), dist.T).T))
    dists.reverse()
    return np.row_stack(dists)

def forward(transition_probs, emission_probs, initial_dist, emissions):
    dists = [initial_dist] 
    for emission in emissions:
        dists.append(normalize(dists[-1]*np.dot(transition_probs, emission_probs(emission))))
    return np.row_stack(dists)

def normalize(array):
    return array / sum(array)

# wiki_means = np.array([0.9, 0.1])
# wiki_std = 1
# wiki_initial_dist = np.array([0.5, 0.5])
# wiki_emissions = [0, 0, 1, 0, 0, 1, 1, 0]
# wiki_transition_probs = np.array([[0.7, 0.3], [0.3, 0.7]])

# if __name__ == "__main__":
#     # print(forward(wiki_transition_probs, wiki_emission_probs, wiki_initial_dist, wiki_emissions))
#     # print(backward(wiki_transition_probs, wiki_emission_probs, wiki_emissions))
#     print(forward_backward(wiki_transition_probs, wiki_means, wiki_std, wiki_initial_dist, wiki_emissions, 2))
