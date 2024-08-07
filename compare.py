# -*- coding: utf-8 -*-

import os
import shutil

main_dirs = ["미완", "미완_스캔", "연재중", "완결", "완결_스캔"]
# main_dirs = ["완결_스캔"]


def check_dir_names(dirs_src, dirs_dst):
    for src in dirs_src:
        if src not in dirs_dst:
            print(f"Diff: {src}")


def filter_verified(dirs):
    dirs_return = []
    for d in dirs:
        if not "[o] " in d:
            dirs_return.append(d)
    return dirs_return


def main():
    ignore_verified = True
    base_path_src = "D:\comix"
    base_path_src = "Z:/"
    # base_path_dst = "Z:/"
    base_path_dst = "E:/comix"

    diff = False
    num_series = 0
    for main_dir in main_dirs:
        main_dir_src = f"{base_path_src}/{main_dir}"
        main_dir_dst = f"{base_path_dst}/{main_dir}"
        dirs_src = os.listdir(main_dir_src)
        dirs_dst = os.listdir(main_dir_dst)

        if ignore_verified:
            dirs_src = filter_verified(dirs_src)
            dirs_dst = filter_verified(dirs_dst)

        # 1 check dir count
        if len(dirs_src) != len(dirs_dst):
            print(f"Num dir difference: {main_dir_src}, {main_dir_dst}")

            # check names
            if len(dirs_src) > len(dirs_dst):
                check_dir_names(dirs_src, dirs_dst)
            else:
                check_dir_names(dirs_dst, dirs_src)
            diff = True
            continue

        # check names
        for src, dst in zip(dirs_src, dirs_dst):
            if src != dst:
                diff = True
                print(f"Dir name different: {main_dir_src}/{src}")
                continue

            # check ext [zip and csv]
            files_src = os.listdir(f"{main_dir_src}/{src}")
            files_dst = os.listdir(f"{main_dir_dst}/{dst}")

            diff_set1 = set(files_src).difference(set(files_dst))
            diff_set2 = set(files_dst).difference(set(files_src))
            if len(diff_set1) + len(diff_set2):
                diff = True
                print(src, diff_set1, diff_set2)
        num_series += len(dirs_src)

    if not diff:
        print("No differences.")
        print(f"Sceries: {num_series}")

    print("done")


if __name__ == "__main__":
    main()
