import zipfile
import os


def build_tree():
    return {'_dirs': {}, '_files': {}}

def add_to_tree(tree, path_parts, content):
    current = tree
    for part in path_parts[:-1]:
        if part not in current['_dirs']:
            current['_dirs'][part] = build_tree()
        current = current['_dirs'][part]

    if path_parts[-1]:
        current['_files'][path_parts[-1]] = {'content': content}


def load_virtual_fs(zip_path):
    virtual_fs = build_tree()

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        for file in zip_ref.namelist():
            file_content = zip_ref.read(file)
            path_parts = file.split('/')
            add_to_tree(virtual_fs, path_parts, file_content)

    return virtual_fs

def print_tree(tree, indent=""):
    for file_name in tree['_files']:
        print(f"{indent}- {file_name} (file)")

    for dir_name, dir_content in tree['_dirs'].items():
        print(f"{indent}+ {dir_name}/ (directory)")
        print_tree(dir_content, indent + "  ")


fs = load_virtual_fs("C:/Users/serge/PycharmProjects/ConfHW1/myZIP.zip")
print_tree(fs)

