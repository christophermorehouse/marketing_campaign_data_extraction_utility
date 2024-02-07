import yaml, os

# Set parent directory
path = os.path.abspath(__file__)
dir_path = os.path.dirname(os.path.dirname(path))

# Get configuration from yaml file
try:
    # Run this if executing from cx_Freeze binary
    with open(dir_path + '/../env_config.yaml', "r") as f:
        config_yaml = yaml.safe_load(f)
except:
    #Run this if executing from python interpreter
    with open(dir_path + '/env_config.yaml', "r") as f:
        config_yaml = yaml.safe_load(f)

print('env_config.yaml found in: ' + dir_path + '/')

# Set global variables with values from yaml file
apollo_auth_token = config_yaml['Script Parameters'][0]['apollo_auth_token']
seniority_level = config_yaml['Script Parameters'][1]['seniority_level']
org_source_csv = config_yaml['Script Parameters'][2]['source_file_name']
enriched_data_output_path = config_yaml['Script Parameters'][3]['target_file_name']