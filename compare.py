# -*- coding: utf-8 -*-

import os


MAIN_DIRS = ["미완", "미완_스캔", "연재중", "연재중_스캔", "완결", "완결_스캔"]


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

        # Check dir count
        if len(dirs_src) != len(dirs_dst):
            print(f"Num dir difference: {main_dir_src}, {main_dir_dst}")

            # check names
            if len(dirs_src) > len(dirs_dst):
                check_dir_names(dirs_src, dirs_dst)
            else:
                check_dir_names(dirs_dst, dirs_src)
            diff = True
            continue

        # Check names
        for src, dst in zip(dirs_src, dirs_dst):
            if src != dst:
                diff = True
                print(f"Dir name different: {main_dir_src}/{src}")
                continue

            # check ext [zip and csv]
            files_src = os.listdir(f"{main_dir_src}/{src}")
            files_dst = os.listdir(f"{main_dir_dst}/{dst}")

            if ignore_verified:
                diff_set1 = set(files_src).difference(set(files_dst))
                diff_set2 = set(files_dst).difference(set(files_src))
                if len(diff_set1) + len(diff_set2):
                    diff = True
                    print(src, sorted(diff_set1), sorted(diff_set2))
            else:
                for file in files_src:
                    name, ext = os.path.splitext(file)
                    if ext not in [".zip", ".csv", ".txt"]:
                        diff = True
                        print(src)

                for file in files_dst:
                    name, ext = os.path.splitext(file)
                    if ext not in [".zip", ".csv", ".txt"]:
                        diff = True
                        print(dst)
        num_series += len(dirs_src)

    if not diff:
        print("No differences.")
        print(f"Series: {num_series}")

    print("done")


if __name__ == "__main__":
    main()
