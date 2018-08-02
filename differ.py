#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

DIFF_FILE = 'diff.txt'

def get_diff(src_commit, dst_commit, path):
    command_diff = "git diff " + str(src_commit) + " " + str(dst_commit) + " " + " > " + str(path)
    print("Try: " + command_diff)
    return os.system(command_diff)

def main(argv):
    print("Start differ.")
    os.system("pwd")
    ret = get_diff(argv[1], argv[2], argv[3])
    print(ret)

if __name__ == '__main__':
    main(sys.argv)
