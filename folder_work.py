# -*- coding: utf-8 -*-

import os
import sys
import subprocess

def getFilesList(dirPath: str) -> list:
    return [os.path.join(path, name) for path, subdirs, files in os.walk(dirPath) for name in files]

# return False, if folder_path not exists or folder_path is not folder
def is_folder(folder_path: str) -> bool:
    return os.path.isdir(folder_path)

# return False, if file_path not exists or file_path is not file
def is_file(file_path: str) -> bool:
    return os.path.isfile(file_path)

# return False, if file_path not exists
def is_exists(file_path: str) -> bool:
    return os.path.exists(file_path)

def pout(msg : str, endl = True):
    if(endl == False):
        print(msg, end="")
    else:
        print(msg)

def get_hash_file(file_path: str) -> str:
    exe_res = exe(f"sha512sum \"{file_path}\"")
    if(exe_res[1] != ""):
        pout(f"Error with sha512sum: ")
        pout(f"\"{exe_res[1]}\"")
        exit()
    res = exe_res[0]
    return res[:res.find(" ")]

def get_hash_str(s: str, if_echo: bool = True):
    exe_res = exe(f"echo -n \"{s}\" | sha512sum", if_echo)
    if(exe_res[1] != ""):
        pout(f"Error with sha512sum: ")
        pout(f"\"{exe_res[1]}\"")
        exit()
    res = exe_res[0]
    return res[:res.find(" ")]

def exe(command : str, debug : bool = True) -> tuple:
    '''
    Аргумент - команда для выполнения в терминале. Например: "ls -lai ."
    Возвращает кортеж, где элементы:
        0 - строка stdout
        1 - строка stderr
        2 - returncode
    '''
    if(debug):
        pout(f"> {command}")

    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = process.stdout.read().decode("utf-8")
    err = process.stderr.read().decode("utf-8")
    errcode = process.returncode
    return (out, err, errcode)

def calc_hash(folder: str):
    folder_abs = os.path.abspath(folder)
    if(is_file(folder_abs) == True):
        pout(f"Hash of the file \"{folder_abs}\": \"{get_hash_file(folder_abs)}\"")
    elif(is_folder(folder_abs) == True):
        files = getFilesList(folder_abs)
        hashes = []
        for file_i in files:
            hash_i = get_hash_file(file_i)
            hashes.append(hash_i)
            pout(f"Hash of \"{file_i}\" = \"{hash_i}\"")
        hashes = sorted(hashes)

        hash_files = ""
        li = 0
        for hash_i in hashes:
            hash_files += hash_i
            li-=-1
            if(li == 30):
                hash_files = get_hash_str(hash_files, False)
                li = 0
        hash_files = get_hash_str(hash_files, False)

        # from io import StringIO
        # o = StringIO()
        # for hash_i in hashes:
        #     o.write(hash_i)
        # hash_files = get_hash_str(o.getvalue())

        pout(f"Hash (not considering the files hierarchy) of the directory \"{folder_abs}\": \n==============================\n{hash_files}\n==============================\n")

    else:
        pout(f"No such file or directory: \"{folder_abs}\"")

if __name__ == "__main__":
    argc = len(sys.argv)
    if(argc != 2):
        pout("Syntax error. Expected: \"> python folder_work.py {path_to_folder_or_file}\"")
    else:
        calc_hash(sys.argv[1])




















