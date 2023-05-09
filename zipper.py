import os
import shutil
import zipfile
import pyminizip
import download_embedded


def zip_file_with_password(file_path, password, output_zip_name):
    """
    Compresses a file with password protection.

    Args:
        file_path (str): The path of the file to compress.
        password (str): The password to protect the compressed file.
        output_zip_name (str): The name of the output zip file.
    """
    compression_lvl = 5
    pyminizip.compress(file_path, None, output_zip_name, password, compression_lvl)


def create_exec_cradle(password, zip_name, py_file_name, output_file_name):
    """
        Creates an execution cradle to run a password-protected zipped Python file in memory.

        Args:
            password (str): The password used for the zipped file.
            zip_name (str): The name of the zipped file.
            py_file_name (str): The name of the original Python file.
            output_file_name (str): The name of the output file.
        """

    cradle_file_path = "cradle.py"

    with open(cradle_file_path, "r") as file:
        file_contents = file.read()

        values_to_replace = {
            "password": f"{password}",
            "cradle.zip": f"{zip_name}",
            "run.py": f"{py_file_name}"
        }

        for old_value, new_value in values_to_replace.items():
            file_contents = file_contents.replace(old_value, new_value)

    with open(f'{output_file_name}', "w") as file:
        file.write(file_contents)


def prompt_for_input(prompt_text):
    """
        Prompts the user for input with the given text and returns the input.

        Args:
            prompt_text (str): The text to display when prompting for input.

        Returns:
            str: The user's input.
        """
    print(prompt_text)
    return input()


def main():
    """
    Main function that runs the script. It downloads an embedded version of Python,
    zips a specified Python file with password protection, and creates an execution
    "cradle" that runs the zipped Python file in memory.
    """
    target_dir = next((dir for dir in os.listdir('.')
                      if 'python_embedded' in dir), '')

    if target_dir:
        print(f"It seems that a previous version of python_embedded is already downloaded in {target_dir}")

        if prompt_for_input("Do you want to replace the existing version with the new one? (y/n)") == "n":
            print("Using the existing version.")
            return
        else:
            try:
                shutil.rmtree(target_dir)
            except Exception as e:
                print(f"Failed to delete the existing version: {e}")
                print("Exiting.")
                return

    answer = prompt_for_input('Would you like us to help you choose a version to download? (y/n)')

    if answer == 'y':
        download_result = download_embedded.main()
    else:
        python_version = prompt_for_input('Please enter the version you want to download (e.g. 3.11.3): ')
        os_release = prompt_for_input('Please enter the os you want to download (e.g. win32 or amd64 or arm64): ')
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

    file_path = prompt_for_input("Enter the python file to be zipped for execution in memory: ")
    password = prompt_for_input("Enter the password to use for zip protection: ")

    if os.path.exists(file_path):
        output_zip_name = os.path.splitext(file_path)[0] + ".zip"
        zip_file_with_password(file_path, password, output_zip_name)
        print("File successfully zipped with password protection!")

        print('Creating Python cradle for execution')
        create_exec_cradle(password, output_zip_name, file_path, 'cradle_runner.py')
        print('Cradle created successfully!')
        # Move the output_zip_name and temp_cradle into the target_dir
        shutil.move(output_zip_name, os.path.join(target_dir, output_zip_name))
        shutil.move(f'cradle_runner.py', os.path.join(target_dir, 'cradle_runner.py'))


if __name__ == '__main__':
    main()