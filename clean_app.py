import logging
import sys
from time import sleep
import zipfile
import os
import tempfile
import shutil

logging.basicConfig(filename='app.log', filemode='w',
                    format='%(name)s - %(levelname)s - %(message)s')
logging.error('This will get logged to a file')

# def unzip_file_to_temp(zip_file):
#     temp_dir = tempfile.mkdtemp()
#     with zipfile.ZipFile(zip_file, 'r') as zip_ref:
#         zip_ref.extractall(temp_dir)
#     return os.path.join(temp_dir, os.listdir(temp_dir)[0])

def unzip_file_to_temp(zip_file):
    temp_dir = tempfile.mkdtemp()
    shutil.unpack_archive(zip_file, temp_dir)
    print("temp_dir: ", temp_dir)
    return temp_dir



def write_removed_folders_to_file(removed_folders, temp_dir):
    print("Cleaning done.")
    filename='cleaned.txt'
    filepath = os.path.join(temp_dir, filename)
    with open(filename, 'w') as cleaned_file:
        for i, folder in enumerate(removed_folders):
            if i == len(removed_folders) - 1:
                cleaned_file.write(folder)
            else:
                cleaned_file.write(f"{folder}\n")


def remove_folders_without_init(temp_dir):
    remove_folders = []
    temp_dir = os.path.join(temp_dir, os.listdir(temp_dir)[0])
    for dirpath, dirnames, files in os.walk(temp_dir):
        if dirpath == temp_dir:
            continue
        if not os.path.exists(os.path.join(dirpath, "__init__.py")):
            relative_path = os.path.relpath(dirpath, temp_dir)
            remove_folders.append(relative_path)
            try:
                print(f"Removing {dirpath}")
                shutil.rmtree(dirpath)
            except Exception as e:
                print(f"Error while deleting {dirpath}: {e}")
    remove_folders.sort()
    write_removed_folders_to_file(remove_folders, temp_dir)


# def create_new_zip_file(temp_dir, zip_file):
#     new_name = f"{zip_file.split('.')[0]}_new.zip"
#     with zipfile.ZipFile(new_name, 'w') as zf:
#         for dirpath, dirnames, files in os.walk(temp_dir):
#             relative_path = os.path.relpath(dirpath, temp_dir)
#             zf.write(dirpath, arcname=relative_path)
#             for filename in files:
#                 file_path = os.path.join(dirpath, filename)
#                 zf.write(file_path, arcname=os.path.join(relative_path, filename))
                
def create_new_zip_file(zip_file, temp_dir):
    new_name = f"{zip_file.split('.')[0]}_new"
    shutil.make_archive(new_name, 'zip', temp_dir)
    print("New zip file created:", new_name)



def main(zip_file):
    temp_dir = unzip_file_to_temp(zip_file)
    remove_folders_without_init(temp_dir)
    create_new_zip_file(zip_file, temp_dir)
    # create_new_zip_file(temp_dir, zip_file)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python clean_app.py <zip-file name>")
        sys.exit(1)
    
    zip_file = sys.argv[1]
    
    if not os.path.exists(zip_file):
        print(f"File {zip_file} not found")
        sys.exit(1)
    
    main(zip_file)


