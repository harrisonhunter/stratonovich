from config_parse import parse_config, create_params_object
from update_methods import UpdateFunctions
from random import choice
from time import time

def run_system(config_location, iterations, test, verbose=False):
	'''Code to run the hmm system'''
	config = parse_config(config_location)
	params = create_params_object(config, test)
	params.set_initial_params()
	update = UpdateFunctions(params)
	for i in xrange(iterations):
		if verbose:
			print '**************ITERATION ' + str(i) + ' ******************'
			print '*----PRIORS----*'
			print update.params.priors
			print '*----BETA------*'
			print update.params.beta
			print '*----SIGMA-----*'
			print update.params.sigma
			print '*----MEANS-----*'
			print update.params.means
			print '*----TRANS-----*'
			print update.params.trans
		else:
			print '**************ITERATION ' + str(i) + ' ******************'
		update.params.means = [update.eq_3(j) for j in xrange(update.params.d)]
		update.params.sigma = update.eq_4() # + 1
		update.params.beta = update.eq_5()
		update.params.trans = [update.eq_2(j) for j in xrange(update.params.d)]
		update.params.priors = update.eq_1()
		t1 = time()
		update.params.x = update.eq_6()
		print "time for updating x" + str(time() - t1)
	return params

#Usage
# run_system('sample.config')
