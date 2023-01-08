# -*- coding: utf-8 -*-

import os
import shutil

main_dirs = ["미완_스캔", "연재중", "완결", "완결_스캔"]


def check_dir_names(dirs_src, dirs_dst):
    for src in dirs_src:
        if src not in dirs_dst:
            print(f"Diff: {src}")


def main():

    base_path_src = "D:\comix"
    base_path_dst = "Z:/"
    base_path_dst = "F:/comix"

    diff = False

    for main_dir in main_dirs:
        main_dir_src = f"{base_path_src}/{main_dir}"
        main_dir_dst = f"{base_path_dst}/{main_dir}"
        dirs_src = os.listdir(main_dir_src)
        dirs_dst = os.listdir(main_dir_dst)

        # 1 check dir count
        if len(dirs_src) != len(dirs_dst):
            print(f"Num dir differenct: {main_dir_src}, {main_dir_dst}")

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

    if not diff:
        print("No differences.")
    print("done")


if __name__ == "__main__":
    main()
