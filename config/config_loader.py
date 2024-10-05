import unittest
from unittest.mock import mock_open, patch
import csv
from io import StringIO

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


class TestLoadConfig(unittest.TestCase):

    @patch("builtins.open", new_callable=mock_open)
    def test_load_config(self, mock_file):
        mock_csv_data = "username,computer,fs_path,startup_script\nuser1,comp1,/path/to/fs,start.py\n"
        mock_file.return_value = StringIO(mock_csv_data)
        config = load_config("dummy_config.csv")
        self.assertEqual(config['username'], 'user1')
        self.assertEqual(config['computer'], 'comp1')
        self.assertEqual(config['fs_path'], '/path/to/fs')
        self.assertEqual(config['startup_script'], 'start.py')


if __name__ == '__main__':
    unittest.main()