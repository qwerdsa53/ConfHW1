import csv

def load_config(config_file):
    config = {}
    with open(config_file, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            config['username'] = row['username']
            config['computer'] = row['computer']
            config['fs_path'] = row['fs_path']
            config['startup_script'] = row['startup_script']
    return config
