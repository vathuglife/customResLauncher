import os
from elevate import elevate
import subprocess

'''def is_root():
    return os.getuid() == 0'''

elevate(show_console=False)
subprocess.run("D:\\Games\\BH3.exe")

'''print("before ", is_root())
elevate()
print("after ", is_root())'''