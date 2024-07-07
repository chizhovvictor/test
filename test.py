import os
import sys
import zipfile
import tempfile
import logging
import shutil

logging.basicConfig(filename='app.log', filemode='w',
                    format='%(name)s - %(levelname)s - %(message)s')
logging.error('This will get logged to a file')

def unzip_file_to_temp(zip_file):
    zf = zipfile.ZipFile(zip_file)
    with tempfile.TemporaryDirectory() as tmp_dir:
        zf.extractall(tmp_dir)
        print(os.path.exists(tmp_dir))
        

def write_removed_folders_to_file(removed_folders):
    with open('cleaned.txt', 'w') as cleaned_file:
        for folder in removed_folders:
            cleaned_file.write(f"{folder}\n")


def remove_folders_without_init():
    removed_folders = []
    for root, dirs, files in os.walk("."):
        if "__init__.py" not in files and root != "." and ".git" not in root.split(os.path.sep):
            try:
                shutil.rmtree(root)
                removed_folders.append(root)
            except Exception as e:
                print(f"Error removing directory {root}: {e}")
    write_removed_folders_to_file(removed_folders)


def create_new_zip_file(zip_file):
    new_name = f"{zip_file.split('.')[0]}_new.zip"
    with zipfile.ZipFile(new_name, 'w') as zf:
        for dirpath, dirnames, files in os.walk("."):
            zf.write(dirpath)
            for filename in files:
                zf.write(os.path.join(dirpath, filename))
                

def main(zip_file):
    unzip_file_to_temp(zip_file)
    remove_folders_without_init()
    create_new_zip_file(zip_file)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python clean_app.py <zip-file name>")
        sys.exit(1)
    
    zip_file = sys.argv[1]
    main(zip_file)
