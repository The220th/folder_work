# -*- coding: utf-8 -*-

import os
import sys
import subprocess

def getFilesList(dirPath: str) -> list:
    return [os.path.join(path, name) for path, subdirs, files in os.walk(dirPath) for name in files]

def getDirsList(dirPath: str) -> list:
    return [os.path.join(path, name) for path, subdirs, files in os.walk(dirPath) for name in subdirs]

# return False, if folder_path not exists or folder_path is not folder
def is_folder(folder_path: str) -> bool:
    return os.path.isdir(folder_path)

# return False, if file_path not exists or file_path is not file
def is_file(file_path: str) -> bool:
    return os.path.isfile(file_path)

# return False, if file_path not exists
def is_exists(file_path: str) -> bool:
    return os.path.exists(file_path)

def is_folder_empty(folder_path: str) -> bool:
    if(len(os.listdir(folder_path)) == 0):
        return True
    else:
        return False

def rel_path(file_path: str, folder_path: str) -> str:
    return os.path.relpath(file_path, folder_path)


def rm_folder_content(folder_path: str):
    for root, dirs, files in os.walk(folder_path, topdown=False):
        for file_i in files:
            os.remove(os.path.join(root, file_i))
        for dir in dirs:
            os.rmdir(os.path.join(root, dir))
    # os.rmdir(folder_path)

def pout(msg : str, endl = True):
    if(endl == False):
        print(msg, end="")
    else:
        print(msg)

def write2File_str(fileName : str, s : str) -> None:
    with open(fileName, 'w', encoding="utf-8") as temp:
        temp.write(s)

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

def main_calc_hash(args: list):
    argc = len(args)
    if(argc != 1):
        pout("Syntax error. Expected: \"python folder_work.py hash {path_to_folder_or_file}\"")
        exit()
    folder = args[0]
    err_out = []
    folder_abs = os.path.abspath(folder)
    if(is_file(folder_abs) == True):
        pout(f"Hash of the file \"{folder_abs}\": \"{get_hash_file(folder_abs)}\"")
    elif(is_folder(folder_abs) == True):
        files = getFilesList(folder_abs)
        files = sorted(files)
        files_len = len(files)
        hashes = []
        d_4table = {}
        gi = 0
        for file_i in files:
            gi+=1
            if(is_file(file_i) == False):
                err_out.append(f"\"{file_i}\" is not file or does not exists, it will be skipped. ")
                continue
            hash_i = get_hash_file(file_i)
            hashes.append(hash_i)
            d_4table[file_i] = hash_i
            pout(f"({gi}/{files_len}) Hash of \"{file_i}\" = \"{hash_i}\"")
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

        try:
            import tabulate
            files_4table = list(d_4table.keys())
            rows = []
            for file_i in files_4table:
                rows.append([file_i, d_4table[file_i]])
            table_str = tabulate.tabulate(rows, headers=["file_name", "hash"])
            pout(table_str)
            #write2File_str("table_out.txt", table_str)
        except:
            pout(f"Cannot import tabulate. No table. ")

        # from io import StringIO
        # o = StringIO()
        # for hash_i in hashes:
        #     o.write(hash_i)
        # hash_files = get_hash_str(o.getvalue())
        if(len(err_out) != 0):
            pout(f"\n===============\nSome troubles happened:")
            for err_i in err_out:
                pout(f"\t{err_i}")
            pout(f"===============")

        pout(f"\n\nHash (not considering the files hierarchy) of the directory \"{folder_abs}\": \n==============================\n{hash_files}\n==============================\n")

    else:
        pout(f"No such file or directory: \"{folder_abs}\"")
    
    pout("=============== Done! ===============")

def main_cp(args: list):
    argc = len(args)
    if(argc != 2):
        pout("Syntax error. Expected: \"python folder_work.py clone {folder_src} {folder_dest}\"")
        exit()
    folder1 = args[0]
    folder2 = args[1]
    err_out = []
    folder1_abs = os.path.abspath(folder1)
    folder2_abs = os.path.abspath(folder2)
    if(is_folder(folder1_abs) == False):
        pout(f"\"{folder1_abs}\" is not folder. ")
        exit()
    if(is_folder(folder2_abs) == False):
        pout(f"\"{folder2_abs}\" is not folder. ")
    
    if(is_folder_empty(folder2_abs) == False):
        pout(f"Folder \"{folder2_abs}\" is not empty. ")
        pout(f"===============\n\t All files in \"{folder2_abs}\" will be removed before clonning. \n===============")
        pout("Continue? Type \"YES\" is capital letter if continue \n> ", endl=False)
        user_in = input()
        if(user_in.strip() != "YES"):
            pout("Exitting")
            exit()
        rm_folder_content(folder2_abs)
        if(is_folder_empty(folder2_abs) == True):
            pout(f"All files from folder \"{folder2_abs}\" removed. This folder is empty now. Clonning...")
        else:
            pout(f"Cannot clean folder \"{folder2_abs}\"! Exiting ")

    dirs_abs_1 = getDirsList(folder1_abs)
    dirs_abs_1 = sorted(dirs_abs_1)
    for dir_i_1 in dirs_abs_1:
        dir_i_rel = rel_path(dir_i_1, folder1_abs)
        dir_i_2 = os.path.join(folder2_abs, dir_i_rel)
        exe_out = exe(f"mkdir -p \"{dir_i_2}\"")
        if(exe_out[1] != ""):
            pout(f"ERROR: {exe_out[1]}")
            exit()

    files_abs_1 = getFilesList(folder1_abs)
    files_abs_1 = sorted(files_abs_1)
    gi, N = 0, len(files_abs_1)
    for file_i_1 in files_abs_1:
        gi+=1
        if(is_file(file_i_1) == False):
            err_out.append(f"\"{file_i_1}\" is not file or does not exists, it will be skipped. ")
            continue
        file_i_rel = rel_path(file_i_1, folder1_abs)
        file_i_2 = os.path.join(folder2_abs, file_i_rel)
        # In windows cp=copy
        pout(f"({gi}/{N}) Copying \"{file_i_rel}\"... ")
        exe_out = exe(f"cp \"{file_i_1}\" \"{file_i_2}\"")
        if(exe_out[1] != ""):
            err_out.append(f"ERROR: {exe_out[1]}")
            continue
    exe("sync")

    if(len(err_out) != 0):
        pout(f"\n===============\nSome troubles happened:")
        for err_i in err_out:
            pout(f"\t{err_i}")
        pout(f"===============")

    pout("=============== Done! ===============")

def diff_new_files(dr1, dr2) -> list:
    files_rel_old, files_rel_new = list(dr1.keys()), list(dr2.keys())
    res = []
    for file_i in files_rel_new:
        if(file_i not in files_rel_old):
            res.append(file_i)
    return res

def diff_changes_files(dr1, dr2) -> list:
    files_rel_old, files_rel_new = list(dr1.keys()), list(dr2.keys())
    res = []
    for file_i in files_rel_new:
        if(file_i in files_rel_old):
            if(dr1[file_i] != dr2[file_i]):
                res.append(file_i)
    return res

def diff_removed_files(dr1, dr2) -> list:
    files_rel_old, files_rel_new = list(dr1.keys()), list(dr2.keys())
    res = []
    for file_i in files_rel_old:
        if(file_i not in files_rel_new):
            res.append(file_i)
    return res

def diff_identical_files(d1, d2, old_folder_path, new_folder_path) -> list:
    len_diff = len(old_folder_path) - len(new_folder_path)
    old_folder_prefix, new_folder_prefix = "", ""
    if(len_diff > 0):
        new_folder_prefix = " "*len_diff
    else:
        old_folder_prefix = " "*(-len_diff)
    files_rel_old, files_rel_new = list(d1.keys()), list(d2.keys())
    hashes1, hashes2 = list(d1.values()), list(d2.values())
    hashes = set(hashes1 + hashes2)
    res = []
    for hash_i in hashes:
        item_fits = 0
        S = f"* Hash \"{hash_i}\" have files: \n"
        for file_i in files_rel_new:
            if(d2[file_i] == hash_i):
                item_fits += 1
                S += f"\t- {new_folder_prefix}{file_i}\n"
        for file_i in files_rel_old:
            if(d1[file_i] == hash_i):
                item_fits += 1
                S += f"\t- {old_folder_prefix}{file_i}\n"
        if(item_fits >= 2):
            res.append(S)
    return res

def main_diff(args: list):
    argc = len(args)
    mode_explain_str = "\t- n: show New files\n\t- c: show Changed files\n\t- r: show Removed files\n\t- s: show Identical files"
    if(argc != 3):
        pout("Syntax error. Expected: \"python folder_work.py diff {n|c|r|i} {folder_old} {folder_new}\", where: ")
        pout(mode_explain_str)
        exit()
    mode = args[0]
    folder_old = args[1]
    folder_new = args[2]
    err_out = []
    folder_old_abs = os.path.abspath(folder_old)
    folder_new_abs = os.path.abspath(folder_new)
    if(is_folder(folder_old_abs) == False):
        pout(f"\"{folder_old_abs}\" is not folder. ")
        exit()
    if(is_folder(folder_new_abs) == False):
        pout(f"\"{folder_new_abs}\" is not folder. ")
    for letter_i in mode:
        if(letter_i not in "ncri"):
            pout(f"Cannot understand \"{letter_i}\" in \"{mode}\". Expected: n, c, r, i or their combination: ")
            pout(mode_explain_str)
            exit()
        if(mode.count(letter_i) > 1):
            pout(f"\"{letter_i}\" cannot repeat. ")
            exit()
    d1, d2, dr1, dr2 = {}, {}, {}, {}
    files_abs_old = sorted(getFilesList(folder_old_abs))
    files_abs_new = sorted(getFilesList(folder_new_abs))
    #files_rel_old = [rel_path(file_i, files_abs_old) for file_i in files_abs_old]
    #files_rel_new = [rel_path(file_i, files_abs_new) for file_i in files_abs_new]
    gi, N = 0, len(files_abs_old)+len(files_abs_new)
    for file_i in files_abs_old:
        gi+=1
        if(is_file(file_i) == False):
            err_out.append(f"\"{file_i}\" is not file or does not exists, it will be skipped. ")
            continue
        file_i_hash = get_hash_file(file_i)
        pout(f"({gi}/{N}) Calculated hash of \"{file_i}\": {file_i_hash}")
        d1[file_i] = file_i_hash
        file_i_rel = rel_path(file_i, folder_old_abs)
        dr1[file_i_rel] = file_i_hash
    for file_i in files_abs_new:
        gi+=1
        if(is_file(file_i) == False):
            err_out.append(f"\"{file_i}\" is not file or does not exists, it will be skipped. ")
            continue
        file_i_hash = get_hash_file(file_i)
        pout(f"({gi}/{N}) Calculated hash of \"{file_i}\": {file_i_hash}")
        d2[file_i] = file_i_hash
        file_i_rel = rel_path(file_i, folder_new_abs)
        dr2[file_i_rel] = file_i_hash

    for mode_i in mode:
        if(mode_i == "n"):
            new_files_rel = diff_new_files(dr1, dr2)
            pout("\n====================\n* New files: ")
            if(len(new_files_rel) > 0):
                for file_i in new_files_rel:
                    pout(f"\t{os.path.join(folder_new_abs, file_i)}")
            else:
                pout("\tNo such files. ")
        elif(mode_i == "c"):
            changed_files_rel = diff_changes_files(dr1, dr2)
            pout("\n====================\n* Changed files: ")
            if(len(changed_files_rel) > 0):
                for file_i in changed_files_rel:
                    pout(f"\t{file_i}")
            else:
                pout("\tNo such files. ")
        elif(mode_i == "r"):
            removed_files_rel = diff_removed_files(dr1, dr2)
            pout("\n====================\n* Removed files: ")
            if(len(removed_files_rel) > 0):
                for file_i in removed_files_rel:
                    pout(f"\t{os.path.join(folder_old_abs, file_i)}")
            else:
                pout("\tNo such files. ")
        elif(mode_i == "i"):
            identical_files = diff_identical_files(d1, d2, folder_old_abs, folder_new_abs)
            pout("\n====================\n* Identical files: ")
            if(len(identical_files) > 0):
                for file_i in identical_files:
                    pout(f"{file_i}")
            else:
                pout("\tNo such files. ")
        else:
            pout(f"Failed successfully (\"{mode_i}\").")

    if(len(err_out) != 0):
        pout(f"\n===============\nSome troubles happened:")
        for err_i in err_out:
            pout(f"\t{err_i}")
        pout(f"===============")

    pout("=============== Done! ===============")

def main_repeats(args: list):
    argc = len(args)
    if(argc != 1):
        pout("Syntax error. Expected: \"python folder_work.py repeats {folder_path}\"")
        exit()
    folder = args[0]
    err_out = []
    folder_abs = os.path.abspath(folder)
    if(is_folder(folder_abs) == False):
        pout(f"\"{folder_abs}\" is not folder. ")
        exit()
    files_abs = sorted(getFilesList(folder_abs))
    hashes = set()
    d = {}
    gi, N = 0, len(files_abs)
    for file_i in files_abs:
        gi+=1
        if(is_file(file_i) == False):
            err_out.append(f"\"{file_i}\" is not file or does not exists, it will be skipped. ")
            continue
        file_i_hash = get_hash_file(file_i)
        pout(f"({gi}/{N}) Calculated hash of \"{file_i}\": {file_i_hash}")
        if(file_i_hash not in hashes):
            hashes.add(file_i_hash)
            d[file_i_hash] = [file_i]
        else:
            d[file_i_hash].append(file_i)

    pout("\n===============\nIdentical files: ")
    IF_AT_LEAST_ONE = False
    hashesss = list(d.keys())
    for hash_i in hashesss:
        fl = d[hash_i]
        if(len(fl) > 1):
            IF_AT_LEAST_ONE = True
            pout(f"* Hash \"{hash_i}\" have files: ")
            for file_i in fl:
                pout(f"\t{file_i}")
            pout("")
    if(IF_AT_LEAST_ONE == False):
        pout("\tNo such files")

    if(len(err_out) != 0):
        pout(f"\n===============\nSome troubles happened:")
        for err_i in err_out:
            pout(f"\t{err_i}")
        pout(f"===============")

    pout("=============== Done! ===============")

if __name__ == "__main__":
    SyntaxError_str = "Syntax error. Expected: \"> python folder_work.py {hash, clone, diff, repeats} ...\""
    argc = len(sys.argv)
    if(argc < 2):
        pout(SyntaxError_str)
        exit()
    else:
        sub_modul_name = sys.argv[1]
        if(sub_modul_name == "hash"):
            main_calc_hash(sys.argv[2:])
        elif(sub_modul_name == "clone"):
            main_cp(sys.argv[2:])
        elif(sub_modul_name == "diff"):
            main_diff(sys.argv[2:])
        elif(sub_modul_name == "repeats"):
            main_repeats(sys.argv[2:])
        else:
            pout(SyntaxError_str)
            exit()

