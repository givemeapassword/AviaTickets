import os

def list_files(directory, exclude_folders=None, exclude_files=None):
    if exclude_folders is None:
        exclude_folders = []
    if exclude_files is None:
        exclude_files = []
        
    for root, dirs, files in os.walk(directory):
        # Исключение папок
        dirs[:] = [d for d in dirs if d not in exclude_folders]
        
        for file in files:
            if file not in exclude_files:
                print(os.path.join(root, file))

# Укажите путь к директории и исключения
path = r'C:\Users\VT070\Desktop\service'
excluded_folders = ['avia_app', 'templates','__pycache__','.git']
excluded_files = ['file_to_exclude.txt', 'another_file.txt']

list_files(path, excluded_folders, excluded_files)
