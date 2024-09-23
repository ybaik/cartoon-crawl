# -*- coding: utf-8 -*-

import os
from common.info import MAIN_DIRS


def check_dir_names(names):
    for name in names:
        print(f"Diff: {name}")


def filter_verified(dirs):
    dirs_return = []
    for d in dirs:
        if not "[o] " in d:
            dirs_return.append(d)
    return dirs_return


def main():
    ignore_verified = True
    base_path_src = "c:/comix"
    base_path_dst = "d:/comix"

    diff = False
    num_series = 0
    for main_dir in MAIN_DIRS:
        main_dir_src = f"{base_path_src}/{main_dir}"
        main_dir_dst = f"{base_path_dst}/{main_dir}"
        dirs_src = os.listdir(main_dir_src)
        dirs_dst = os.listdir(main_dir_dst)
        dirs_src.sort()
        dirs_dst.sort()

        if ignore_verified:
            dirs_src = filter_verified(dirs_src)
            dirs_dst = filter_verified(dirs_dst)

        # Check dir
        diff_src = set(dirs_src) - set(dirs_dst)
        if len(diff_src):
            print(f"Num dir difference: {main_dir_src}, {main_dir_dst}")
            # check names
            check_dir_names(diff_src)
            diff = True

        diff_dst = set(dirs_dst) - set(dirs_src)
        if len(diff_dst):
            print(f"Num dir difference: {main_dir_src}, {main_dir_dst}")
            # check names
            check_dir_names(diff_dst)
            diff = True

        names = set(dirs_src) & set(dirs_dst)

        # Check names
        for name in names:
            # check ext [zip and csv]
            files_src = os.listdir(f"{main_dir_src}/{name}")
            files_dst = os.listdir(f"{main_dir_dst}/{name}")

            if ignore_verified:
                diff_set1 = set(files_src).difference(set(files_dst))
                diff_set2 = set(files_dst).difference(set(files_src))
                if len(diff_set1) + len(diff_set2):
                    diff = True
                    print(name, sorted(diff_set1), sorted(diff_set2))
            else:
                for file in files_src:
                    name, ext = os.path.splitext(file)
                    if ext not in [".zip", ".csv", ".txt"]:
                        diff = True
                        print(name)

                for file in files_dst:
                    name, ext = os.path.splitext(file)
                    if ext not in [".zip", ".csv", ".txt"]:
                        diff = True
                        print(name)
        num_series += len(dirs_src)

    if not diff:
        print("No differences.")
        print(f"Series: {num_series}")

    print("done")


if __name__ == "__main__":
    main()
