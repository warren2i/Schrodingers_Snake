# Schrödinger's Snake

Schrödinger's Snake: Injecting uncertainty. You won't know what it's up to until you run it!


![alt text](https://github.com/warren2i/python_in-memory_zipobject/blob/master/img_snake.jpg?raw=true)

# Python Embedded Downloader and Zip Cradler

This script automates the process of downloading an embedded version of Python, zipping a specified Python file with password protection, and creating an execution "cradle" that runs the zipped Python file.

## Requirements

- Python 3.6 or higher
- `pyminizip` library: Install using `pip install pyminizip`  

## Usage
1. git clone https://github.com/warren2i/python_in-memory_zipobject
2. cd python_in-memory_zipobject
3. pip install -r requirements.txt
4. Place dirty dll or .py file inside python_in-memory_zipobject dir 
5. Run the script using the Python interpreter: `python zipper.py`
6. Follow the prompts to download an embedded version of Python, zip a Python file with password protection, and create an execution cradle.
7. A folder will be created containing everything needed to inject the dll or py file inside memory.

## Functions

- `zip_file_with_password(file_path, password, output_zip_name)`: Compresses a file with password protection.
- `create_exec_cradle(password, zip_name, py_file_name, output_file_name)`: Creates an execution cradle to run a password-protected zipped Python file.
- `prompt_for_input(prompt_text)`: Prompts the user for input with the given text and returns the input. 
