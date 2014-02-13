'''
General Gibbs Sampler

Impliments the Gibbs Sampling Algorithm, a class of MCMC Algorithm

Harrison

'''

import math
import random
import sys

'''
The Gibbs algorithm itself

ARGUMENTS:
 - iters: integer number of iterations for which to run algorithm
 - obj: objective function to be run on points to measure how "good"
   they are
 - updates: a set of functions used to update the parameters
 - init: the first point to be used, should be in the form of the
   argument/return value of next
 - verbose: whether or not to print info during the algorithm

RETURNS:
 - the markov chain of points visited
 - list of objective values of accepted points
 - best objective value reached
 - parameters that achieved best objective value

'''

def gibbs_sample(iters, obj, updates, init, verbose=False):

    accepted_points = [init]
    initial_score = obj(init)
    accepted_scores = [initial_score]

    candidates_accepted = 0

    best_parameters_so_far = init
    best_score_so_far = initial_score

    for i in xrange(iters):
        if verbose:
            print "---------" + tagline + "--------"
            print "iteration: "+str(i+startingIteration)
            print "best score so far" + str(best_score_so_far)
            print '\n'


        # most recent accepted point, and its score
        last_point = accepted_points[i]
        last_point_score = accepted_scores[i]
        # point to be considered, and its score
        candidate_point = next(last_point, whichBlock)
        candidate_point_score = o(candidate_point)

        # if necessary update best score seen and best parameters seen
        if candidate_point_score > best_score_so_far:
            best_score_so_far = candidate_point_score
            best_parameters_so_far = candidate_point



        # to avoid underflow, objective function may be the log of what we want,
        #   in which case we subtract and then exponentiate,
        #   instead of simply divide

        if candidate_point_score - last_point_score > math.log(sys.maxint):
            score_ratio = 1
        else:
            score_ratio = math.exp(float(candidate_point_score) -\
             float(last_point_score))

        # if the new point is better, accept it. if not, maybe accept it and
        # maybe don't accept it
        rand_threshold = random.random()
        next_point = last_point
        next_score = last_point_score
        if rand_threshold < min(1, score_ratio):
            next_point = candidate_point
            next_score = candidate_point_score
            candidates_accepted += 1

        accepted_points.append(next_point)
        accepted_scores.append(next_score)

    # calculate the fraction of candidates considered that were accepted
    acceptance_rate = float(candidates_accepted) / float(iters)

    if verbose:
        print "***----" + tagline + "-----***"
        print "best_parameters: "+str(best_parameters_so_far)
        print "best_score: "+str(best_score_so_far)
        print "acceptance_rate: "+str(acceptance_rate)
        print "***-------" + "-"*len(tagline) + "--***"

    return accepted_points, accepted_scores, acceptance_rate,\
     best_score_so_far, best_parameters_so_far
