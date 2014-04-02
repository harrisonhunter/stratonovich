from config_parse import parse_config, create_params_object
from update_methods import UpdateFunctions
from random import choice

def run_system(config_location):
	config = parse_config('sample.config')
	params = create_params_object(config)
	params.set_initial_params()
	iterations = 10
	update = UpdateFunctions(params)
	for i in xrange(iterations):
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
		update.params.means = [update.eq_3(i) for i in xrange(update.params.d)]
		update.params.sigma = update.eq_4()**(-1.0/2) + 1
		update.params.beta = update.eq_5()
		update.params.trans = [update.eq_2(i) for i in xrange(update.params.d)]
		update.params.priors = update.eq_1()
		update.params.x = [update.eq_6()] + update.eq_7()
	return params

# run_system('sample.config')
