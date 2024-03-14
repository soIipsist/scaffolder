import os
    
def is_valid_dir(string):
    if os.path.isdir(string):
        return string
    else:
        raise NotADirectoryError(string)  

def is_valid_path(string):
    if os.path.exists(string):
        return string
    else:
        raise FileNotFoundError(string)
    
    
def is_exe_installed(executable_path):
    paths = os.environ["PATH"].split(os.pathsep)
    for path in paths:
        exe_path = os.path.join(path, executable_path)
        if os.path.exists(exe_path):
            return True
    
    return False