#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import copy

DIFF_FILE = 'diff.txt'

PATCHES_BASE_FILE = 'patch.list'
patches_base = []

def check_null_string(f):
    def checker(line):
        if line == "":
            return line
        else: 
            return f(line)
    return checker


@check_null_string
def diff_filenames(line):
    l = line.split()
    if l[2][1:] != l[3][1:]:
        print("rename: ", l[2][1:], " -> ", l[3][1:])
    return l[2][2:], l[3][2:]


@check_null_string
def get_text(filename):
    text = []
    with open(filename, "r") as in_f:
        for line in in_f:
#        line = in_f.readline()
            text.append(line.encode('utf-8'))
#        text = in_f.readlines()
    return text

@check_null_string
def patch_name_file_form(line):
    return str(line).replace("/", "-") + ".patch"

def patch_name_file_form_idx(line, i):
    if line == "":
        return line
    return str(line).replace("/", "-") + "-" + str(i) + ".patch"

def put_patch_to_file(filename, text):
    if filename == "":
        print("ERROR: put_patch_to_file get filename null")
        return
    if text == "":
        print("ERROR: put_patch_to_file get text null")
        return
    with open(filename, 'w') as f:
        for line in text:
            f.write(line)

def log_split(files, patches):
    print("Splitting has been completed with ", 
            files, " file to ", patches, " patches")

@check_null_string
def split_patch_by_change(text):
    index = -1
    j = 0
    header_is = 0
    patch_header = []
    patch = []
    name = ""
    for line in text:
        index += 1
        if index == 0:
            key = diff_filenames(line)
        if (line.find("@@ ") == 0):
            header_is = 1
            if len(patch) > 0:
                put_patch_to_file(name, patch)
            j += 1
            name = patch_name_file_form_idx(key[0], j)
            patches_base.append(name)
            patch = copy.copy(patch_header)
            patch.append(line)
            continue
        if header_is == 0:
            patch_header.append(line)
            continue
        patch.append(line)

    # case rename patch:
    if j == 0:
        j += 1
        name = patch_name_file_form_idx(key[0], j)
        patches_base.append(name)
        patch = copy.copy(patch_header)

    #last patch:
    put_patch_to_file(name, patch)
    return j

def split_patches(text, mode):
    i = 0
    patch = []
    key   = ("", "")
    index = 0
    files = 0

    if mode == "-f" or mode == "-s":
        for line in text:
            if (line.find("diff --git") == 0):
                i += 1
                # -- flush patch:
                name = patch_name_file_form(key[0])
                if name != "":
                    if mode == "-s":
                        files += split_patch_by_change(patch)
                    else:
                        patches_base.append(name)
                        put_patch_to_file(name, patch)
                        files += 1
                patch = []
                key = diff_filenames(line)
            patch.append(line)
        #last patch:
        if mode == "-s":
            files += split_patch_by_change(patch)
        else:
            name = patch_name_file_form(key[0])
            patches_base.append(name)
            put_patch_to_file(name, patch)
            files += 1

        log_split(files, i)
    else:
        print("Error: unknown mode ", mode)


@check_null_string
def main(mode):
    split_patches(get_text(DIFF_FILE), mode)
    with open(PATCHES_BASE_FILE, "w", encoding="utf8") as f:
        for patch in patches_base:
            f.write(patch + "\n")
            
def select_mode_and_try_run(argv):
    if len(argv) > 1:
            main(argv[1])
            return 0
    else:
        print("Too few parameters, use -f for file or -s for string mode")
        return -1


if __name__ == '__main__':
    select_mode_and_try_run(sys.argv)
