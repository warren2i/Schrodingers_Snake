# Python Embedded Downloader and Zip Cradler

This script automates the process of downloading an embedded version of Python, zipping a specified Python file with password protection, and creating an execution "cradle" that runs the zipped Python file.

## Requirements

- Python 3.6 or higher
- `pyminizip` library: Install using `pip install pyminizip`

## Usage

1. Save the provided script as a `.py` file (e.g., `main.py`).
2. Run the script using the Python interpreter: `python main.py`
3. Follow the prompts to download an embedded version of Python, zip a Python file with password protection, and create an execution cradle.

## Functions

- `zip_file_with_password(file_path, password, output_zip_name)`: Compresses a file with password protection.
- `create_exec_cradle(password, zip_name, py_file_name, output_file_name)`: Creates an execution cradle to run a password-protected zipped Python file.
- `prompt_for_input(prompt_text)`: Prompts the user for input with the given text and returns the input.