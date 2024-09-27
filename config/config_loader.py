import csv


def load_config(config_path):
    config = {}
    with open(config_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            key, value = row
            config[key] = value
    return config


if __name__ == '__main__':
    config = load_config("C:/Users/qwerdsa53/OneDrive/Desktop/file.csv")
    print(config)
