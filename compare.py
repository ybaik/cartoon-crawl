# -*- coding: utf-8 -*-

import os
import shutil

main_dirs = ["미완_스캔", "연재중", "완결", "완결_스캔"]


def main():

    base_path_src = "D:\comix"
    base_path_dst = "//192.168.1.1\comix"

    for main_dir in main_dirs:
        main_dir_src = f"{base_path_src}/{main_dir}"
        main_dir_dst = f"{base_path_dst}/{main_dir}"
        dirs_src = os.listdir(main_dir_src)
        dirs_dst = os.listdir(main_dir_dst)

        # 1 check dir count
        if len(dirs_src) != len(dirs_dst):
            print(f"Num dir differenct: {main_dir_src}, {main_dir_dst}")
            continue

        # check names
        is_same = True
        for src, dst in zip(dirs_src, dirs_dst):
            if src != dst:
                is_same = False
                print(f"Dir name different: {main_dir_src}/{src}")
        if is_same == False:
            continue

        # check ext [zip and csv]


if __name__ == "__main__":
    main()
