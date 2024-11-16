# -*- coding: utf-8 -*-

import os
from common.info import MAIN_DIRS


def get_unverified_dirs(dirs):
    """Returns a list of directories without the '[o] ' prefix"""
    return [d for d in dirs if not d.startswith("[o] ")]


def get_diff_dirs(dirs1, dirs2):
    """Returns the difference between two lists of directories"""
    return set(dirs1) - set(dirs2)


def main():
    compare_btw_hdd = True
    base_path_src = "e:/comix" if compare_btw_hdd else "c:/comix"
    base_path_dst = "d:/comix"
    ignore_verified = not compare_btw_hdd

    diff = False
    num_series = 0
    for main_dir in MAIN_DIRS:
        main_dir_src = os.path.join(base_path_src, main_dir)
        main_dir_dst = os.path.join(base_path_dst, main_dir)
        dirs_src = sorted(
            get_unverified_dirs(os.listdir(main_dir_src))
            if ignore_verified
            else os.listdir(main_dir_src)
        )
        dirs_dst = sorted(
            get_unverified_dirs(os.listdir(main_dir_dst))
            if ignore_verified
            else os.listdir(main_dir_dst)
        )
        diff_src = get_diff_dirs(dirs_src, dirs_dst)
        diff_dst = get_diff_dirs(dirs_dst, dirs_src)

        if diff_src or diff_dst:
            print(f"Dir difference: {main_dir_src}, {main_dir_dst}")
            print("Missing in dst:", sorted(diff_src))
            print("Missing in src:", sorted(diff_dst))
            diff = True

        common_dirs = set(dirs_src) & set(dirs_dst)

        for title in common_dirs:
            files_src = os.listdir(os.path.join(main_dir_src, title))
            files_dst = os.listdir(os.path.join(main_dir_dst, title))
            if ignore_verified:
                diff_files = set(files_src) ^ set(files_dst)
                if diff_files:
                    print(title, sorted(diff_files))
                    diff = True
            else:
                for files in [files_src, files_dst]:
                    for file in files:
                        if not file.endswith((".zip", ".csv", ".txt")):
                            print(title, file)
                            diff = True

        num_series += len(dirs_src)

    if not diff:
        print("No differences.")

    print(f"Series: {num_series}")
    print("done")


if __name__ == "__main__":
    main()
