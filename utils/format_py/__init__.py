import subprocess

def format_py(code_file:str)->str:
    result = subprocess.run(["black", "--quiet", code_file],stderr=subprocess.PIPE)
    if result.returncode != 0:
        return result.stderr
    return None

if __name__ == "__main__":
    code = '''
import    qwer

def a():
    a = b+ func(c    ,d )
    a+=2
'''
    import os
    module_dir = os.path.dirname(os.path.abspath(__file__))
    code_path = os.path.join(module_dir,'test.py')
    with open(os.path.join(module_dir,'test.py'),'w') as f:
        f.write(code)
    result = format_py(code_path)
    if result is not None:
        print(result)
    else:
        print("Success")