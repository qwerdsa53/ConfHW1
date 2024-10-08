import os
import zipfile
import shutil

from fs.unpack_fs import print_tree


def ls(current_path, fs):
    try:
        current_directory = get_directory(current_path, fs)
        directories = list(current_directory['_dirs'].keys())
        files = list(current_directory['_files'].keys())
        result = []
        if directories:
            result.extend([f"  {dir_name}/" for dir_name in directories])
        if files:
            result.extend([f"  {file_name}" for file_name in files])
        return "\n".join(result) if result else "Директория пусстая"
    except FileNotFoundError:
        return "Директория не найдена"


def get_directory(path, fs):
    current_directory = fs
    for directory in path:
        current_directory = current_directory['_dirs'].get(directory, None)
        if current_directory is None:
            raise FileNotFoundError(f"Директория '{directory}' не найдена")
    return current_directory


def cd(new_directory, current_path, fs):
    current_directory = get_directory(current_path, fs)
    if new_directory == "..":
        if current_path:
            current_path.pop()
        else:
            return "Вы находитесь в верхней директории"
    elif new_directory.strip() in current_directory['_dirs']:
        current_path.append(new_directory.strip())
    else:
        return "Директория не найдена"
    return current_path


def rename(old_name, new_name, cur_dir, fs, zip_path):
    current_directory = get_directory(cur_dir, fs)

    if old_name in current_directory['_dirs']:
        current_directory['_dirs'][new_name] = current_directory['_dirs'].pop(old_name)
        print_tree(current_directory)
        update_zip_with_rename(old_name, new_name, cur_dir, zip_path, is_directory=True)
        return f"Директория '{old_name}' переименована '{new_name}'"

    elif old_name in current_directory['_files']:
        current_directory['_files'][new_name] = current_directory['_files'].pop(old_name)
        print_tree(current_directory)
        update_zip_with_rename(old_name, new_name, cur_dir,zip_path, is_directory=False)
        return f"Файл '{old_name}' переименован '{new_name}'"

    else:
        return f"Error: '{old_name}' not found in the current directory"


def update_zip_with_rename(old_name, new_name, cur_dir, zip_path, is_directory,):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall('temp_zip')

    old_path = os.path.join('temp_zip', *cur_dir, old_name)
    new_path = os.path.join('temp_zip', *cur_dir, new_name)

    if is_directory:
        os.rename(old_path, new_path)
    else:
        os.rename(old_path, new_path)

    with zipfile.ZipFile(zip_path, 'w') as zip_ref:
        for foldername, subfolders, filenames in os.walk('temp_zip'):
            for filename in filenames:
                file_path = os.path.join(foldername, filename)
                zip_ref.write(file_path, os.path.relpath(file_path, 'temp_zip'))
            for subfolder in subfolders:
                folder_path = os.path.join(foldername, subfolder)
                zip_ref.write(folder_path, os.path.relpath(folder_path, 'temp_zip'))

    shutil.rmtree('temp_zip')


def move(file_name, path, cur_dir, fs, zip_path):
    current_directory = get_directory(cur_dir, fs)

    if file_name in current_directory['_files']:
        item = current_directory['_files'].pop(file_name)
    elif file_name in current_directory['_dirs']:
        item = current_directory['_dirs'].pop(file_name)
    else:
        return f"Файл: '{file_name}' не найден в текущей директории"

    target_path_parts = path.strip('/').split('/')
    target_directory = get_directory(target_path_parts, fs)

    if file_name in target_directory['_files'] or file_name in target_directory['_dirs']:
        return f"Файл или директория с именем '{file_name}' уже существует в целевой директории"

    if isinstance(item, dict):
        target_directory['_dirs'][file_name] = item
    else:
        target_directory['_files'][file_name] = item

    update_zip_with_move(file_name, path, cur_dir, zip_path, is_directory=isinstance(item, dict))

    return f"'{file_name}' успешно перемещёен в '{path}'"


def update_zip_with_move(file_name, target_path, cur_dir, zip_path, is_directory):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall('temp_zip')

    old_path = os.path.join('temp_zip', *cur_dir, file_name)
    new_path = os.path.join('temp_zip', *target_path.strip('/').split('/'), file_name)

    os.makedirs(os.path.dirname(new_path), exist_ok=True)

    shutil.move(old_path, new_path)

    with zipfile.ZipFile(zip_path, 'w') as zip_ref:
        for foldername, subfolders, filenames in os.walk('temp_zip'):
            for filename in filenames:
                file_path = os.path.join(foldername, filename)
                zip_ref.write(file_path, os.path.relpath(file_path, 'temp_zip'))
            for subfolder in subfolders:
                folder_path = os.path.join(foldername, subfolder)
                zip_ref.write(folder_path, os.path.relpath(folder_path, 'temp_zip'))

    shutil.rmtree('temp_zip')


def copy(file_name, target_path, cur_dir, fs, zip_path):

    current_directory = get_directory(cur_dir, fs)

    if file_name in current_directory['_files']:
        item = current_directory['_files'][file_name]
        is_directory = False
    elif file_name in current_directory['_dirs']:
        item = current_directory['_dirs'][file_name]
        is_directory = True
    else:
        return f"'{file_name}' не найден в текущей директории"

    target_path_parts = target_path.strip('/').split('/')
    target_directory = get_directory(target_path_parts, fs)

    if file_name in target_directory['_files'] or file_name in target_directory['_dirs']:
        return f"Файл или директория с именем '{file_name}' уже существует в целевой директории"

    if is_directory:
        target_directory['_dirs'][file_name] = item.copy()
    else:
        target_directory['_files'][file_name] = item.copy()

    update_zip_with_copy(file_name, target_path, cur_dir, zip_path, is_directory)

    return f"'{file_name}' успешно скопирован в '{target_path}'"


def update_zip_with_copy(file_name, target_path, cur_dir, zip_path, is_directory):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall('temp_zip')

    old_path = os.path.join('temp_zip', *cur_dir, file_name)
    new_path = os.path.join('temp_zip', *target_path.strip('/').split('/'), file_name)

    os.makedirs(os.path.dirname(new_path), exist_ok=True)

    if is_directory:
        shutil.copytree(old_path, new_path)
    else:
        shutil.copy2(old_path, new_path)

    with zipfile.ZipFile(zip_path, 'w') as zip_ref:
        for foldername, subfolders, filenames in os.walk('temp_zip'):
            for filename in filenames:
                file_path = os.path.join(foldername, filename)
                zip_ref.write(file_path, os.path.relpath(file_path, 'temp_zip'))
            for subfolder in subfolders:
                folder_path = os.path.join(foldername, subfolder)
                zip_ref.write(folder_path, os.path.relpath(folder_path, 'temp_zip'))

    shutil.rmtree('temp_zip')

