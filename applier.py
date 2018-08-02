#! /usr/bin/env python3
import os
import sys

PATCHES_BASE_FILE = './patches/patch.list'

FAILURE_LIST_FILE = './fails.list'
SUCCESS_LIST_FILE = './success.list'
CORRUPTED_LIST_FILE = './corrupted.list'
APPLIED_LIST_FILE = './already_applied.list'

FAILURE_LIST = []
SUCCESS_LIST = []
CORRUPTED_LIST = []
APPLIED_LIST = []

total = 0

def singe_patch_apply(patch, key):
    return os.system("git apply -v " + key + " ./patches/" + patch)

def patch_apply(patch):
    global total 
    total += 1
    ret = os.system("git apply -v ./patches/" + patch)
    if (ret != 0):
        FAILURE_LIST.append(patch)
        if singe_patch_apply(patch, "-R") == 0:
            singe_patch_apply(patch, "") # -- apply again!
            APPLIED_LIST.append(patch)
        else:
            CORRUPTED_LIST.append(patch)
    else:
        SUCCESS_LIST.append(patch)

def show_failures():
    print("===== FAILURE_LIST: =====\n")
    for i in FAILURE_LIST:
        print(i)

def show_successes():
    print("===== SUCCESS_LIST: =====\n")
    for i in SUCCESS_LIST:
        print(i)

def check_fails_for_already_applied():
    with open(FAILURE_LIST_FILE, "r") as f:
        patches = f.readlines()
    for patch in patches:
        patch = "./patches/" + patch
        if singe_patch_apply(patch.strip(), "-R") == 0:
            singe_patch_apply(patch.strip(), "") # -- apply again!
            APPLIED_LIST.append(patch.strip())
        else:
            CORRUPTED_LIST.append(patch.strip())

    print("===== CORRUPTED_LIST: =====\n")
    for i in CORRUPTED_LIST:
        print(i)
    print("===== APPLIED_LIST: =====\n")
    for i in APPLIED_LIST:
        print(i)
            

def flush_patches_results():
    with open(SUCCESS_LIST_FILE, "w") as f:
        for item in SUCCESS_LIST:
            f.write(item + "\n")
    with open(FAILURE_LIST_FILE, "w") as f:
        for item in FAILURE_LIST:
            f.write(item + "\n")
    with open(CORRUPTED_LIST_FILE, "w") as f:
        for item in CORRUPTED_LIST:
            f.write(item + "\n")
    with open(APPLIED_LIST_FILE, "w") as f:
        for item in APPLIED_LIST:
            f.write(item + "\n")


def show_stats():
    print("\n------------STATS---------------")
    print("Total: ", total)
    print("Success: ", len(SUCCESS_LIST))
    print("Corrupted: ", len(CORRUPTED_LIST))
    print("Already applied: ", len(APPLIED_LIST))

def main():
    if len(sys.argv) > 1:
        key = ""
        # -- "-R" for revert commit
        if (len(sys.argv) > 2):
            key = sys.argv[2]
        singe_patch_apply(sys.argv[1], key)
        return 0
    else:
        with open(PATCHES_BASE_FILE, "r") as f:
            patches = f.readlines()
        for patch in patches:
            patch_apply(patch.strip())
        show_successes()
        show_failures()

if __name__ == '__main__':
    print("Start patches apply from ", PATCHES_BASE_FILE)
    main()
    flush_patches_results()
    show_stats()

