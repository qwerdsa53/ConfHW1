import unittest
from unittest.mock import patch, mock_open, MagicMock
import os
import shutil
import zipfile
from io import StringIO
from commands.basic_commands import rename, move, copy, ls, get_directory, cd
from config.config_loader import load_config
from fs.unpack_fs import load_virtual_fs


class TestLoadConfig(unittest.TestCase):
    def setUp(self):
        self.fs = load_virtual_fs("C:\\Users\\qwerdsa53\\PycharmProjects\\ConfHW1\\myZIP.zip")

    def test_ls(self):
        result = ls(['myZIP', 'myFS'], self.fs)
        self.assertIn('  dir1/', result)
        self.assertIn('  1.txt', result)

    def test_ls_directory_not_found(self):
        result = ls(['not_exist'], self.fs)
        self.assertEqual(result, 'Директория не найдена')

    def test_cd_change_directory(self):
        current_path = ['myZIP']
        result = cd('myFS', current_path, self.fs)
        self.assertEqual(result, ['myZIP', 'myFS'])

    def test_cd_back_to_parent(self):
        current_path = ['myZIP', 'myFS']
        result = cd('..', current_path, self.fs)
        self.assertEqual(result, ['myZIP'])

    def test_cd_directory_not_found(self):
        result = cd('not_exist', ['myZIP'], self.fs)
        self.assertEqual(result, 'Директория не найдена')

    @patch("builtins.open", new_callable=mock_open)
    def test_load_config(self, mock_file):
        mock_csv_data = "username,computer,fs_path,startup_script\nuser1,comp1,/path/to/fs,start.sh\n"
        mock_file.return_value = StringIO(mock_csv_data)
        config = load_config("dummy_config.csv")
        self.assertEqual(config['username'], 'user1')
        self.assertEqual(config['computer'], 'comp1')
        self.assertEqual(config['fs_path'], '/path/to/fs')
        self.assertEqual(config['startup_script'], 'start.sh')

    @patch('zipfile.ZipFile')
    @patch('shutil.rmtree')
    @patch('os.rename')
    def test_rename_directory(self, mock_rename, mock_rmtree, mock_zipfile):
        result = rename('dir1', 'new_dir1', ['myZIP', 'myFS'], self.fs, 'test.zip')
        self.assertEqual(result, "Директория 'dir1' переименована 'new_dir1'")

    @patch('zipfile.ZipFile')
    @patch('shutil.rmtree')
    @patch('os.rename')
    def test_rename_file(self, mock_rename, mock_rmtree, mock_zipfile):
        result = rename('1.txt', 'new_1.txt', ['myZIP', 'myFS'], self.fs, 'test.zip')
        self.assertEqual(result, "Файл '1.txt' переименован 'new_1.txt'")

    @patch('zipfile.ZipFile')
    @patch('shutil.rmtree')
    @patch('shutil.move')
    def test_move(self, mock_move, mock_rmtree, mock_zipfile):
        result = move('1.txt', 'myZIP/myFS/dir1', ['myZIP', 'myFS'], self.fs, 'test.zip')
        print(self.fs)
        self.assertEqual(result, "'1.txt' успешно перемещёен в 'myZIP/myFS/dir1'")

    @patch('zipfile.ZipFile')
    @patch('shutil.rmtree')
    @patch('shutil.copy2')
    def test_copy_file(self, mock_copy2, mock_rmtree, mock_zipfile):
        result = copy('1.txt', 'myZIP/myFS/dir2', ['myZIP', 'myFS'], self.fs, 'test.zip')
        self.assertEqual(result, "'1.txt' успешно скопирован в 'myZIP/myFS/dir2'")
        mock_copy2.assert_called_once()


if __name__ == '__main__':
    unittest.main()