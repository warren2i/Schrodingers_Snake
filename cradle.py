import zipfile

string = 'password'
pword_bytes = bytes(string, 'utf-8')

with zipfile.ZipFile('cradle.zip', 'r') as zf:
    with zf.open('run.py', 'r', pwd=pword_bytes) as py_file:
        memory_buffer = py_file.read()

exec(memory_buffer)