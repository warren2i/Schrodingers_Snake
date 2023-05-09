import os
import download_embedded
import zipfile
import pyminizip
import shutil

def zip_file_with_password(file_path, password, output_zip_name):
    compression_lvl = 5
    # compressing file
    pyminizip.compress(file_path, None, output_zip_name, password, compression_lvl)





zip_file_with_password('run.py', 'password', 'cradle.zip')

def main():
    target_dir = ''
    for directory in os.listdir('.'):
        if directory.startswith('python_embedded') or 'python_embedded' in directory:
            target_dir = directory
            break

    if target_dir:
        print(f"It seems that a previous version of python_embedded is already downloaded in {target_dir}")
        print("Do you want to replace the existing version with the new one?")
        print("y/n")
        answer = input()
        if answer == "n":
            print("Using the existing version.")
            return
        else:
            try:
                shutil.rmtree(target_dir)
            except Exception as e:
                print(f"Failed to delete the existing version: {e}")
                print("Exiting.")
                return

    print('Would you like us to help you choose a version to download?')
    print('y/n')
    answer = input()

    if answer == 'y':
        download_result = download_embedded.main()
    else:
        print('Please enter the version you want to download')
        print('e.g. 3.11.3')
        python_version = input()
        print('Please enter the os you want to download')
        print('e.g. win32 or amd64 or arm64')
        os_release = input()
        download_result = download_embedded.download_python_embedded(os_release=os_release, python_version=python_version)

    if download_result is None:
        print("An error occurred during the download. Exiting.")
        return

    version_number = os.path.splitext(os.path.basename(download_result))[0]

    target_dir = f'python_embedded-{version_number}'
    if os.path.isdir(target_dir):
        shutil.rmtree(target_dir)
    os.makedirs(target_dir)
    with zipfile.ZipFile(download_result, 'r') as zip_ref:
        zip_ref.extractall(target_dir)

    print(f'{target_dir} downloaded and unzipped successfully')

    file_path = input("Enter the file location to be zipped: ")
    password = input("Enter the password to use for zip protection: ")

    # Check if file path exists
    if os.path.exists(file_path):
        # Create output zip file name by appending '.zip' to original file name
        output_zip_name = os.path.splitext(file_path)[0] + ".zip"

        # Zip the file with password protection
        zip_file_with_password(file_path, password, output_zip_name)

        print("File successfully zipped with password protection!")
    else:
        print("File not found. Please enter a valid file path.")

if __name__ == '__main__':
    main()

