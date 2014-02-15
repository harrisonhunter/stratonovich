'''
The master file for the frame work

Consists of 3 parts:

1. Text file parsing and data aggregation

2. Model Selection and Parameter Estimation

3. Inferences
'''

from data_processing import file_prep as prep
from data_processing import load_data as load
from calculate_inferences import calc_inferences
from helper import generate_configs
from helper import model_selection
from train import train_model
from calculate_stats import calc_stats

def main(file_path, prep_config, aggregated=False, stats=False, configs=True):
	if aggregated:
		data = load(file_path)
	else:
		data = prep(file_path, prep_config)

	if stats:
		data_stats = calc_stats(data, stats_config)
	else:
		data_stats = 0

	if configs == True:
		config_list = generate_configs()
	else:
		config_list = configs

	inferences = []
	trained_models = []

	for config in config_list:
		model = model_selection(config, data)
		trained_models.append(train_model(config, model, data))
		inferences.append(calc_inferences(config, trained_model, data))

	return (data_stats, trained_models, inferences)
