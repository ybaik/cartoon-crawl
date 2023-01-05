# -*- coding: utf-8 -*-

import os

main_dirs = ["미완_스캔", "연재중", "완결", "완결_스캔"]


def main():

    base_path = "D:\comix"
    keyword = "H2"

    for main_dir in main_dirs:
        main_dir_src = f"{base_path}/{main_dir}"
        dirs_src = os.listdir(main_dir_src)

        for src in dirs_src:
            if keyword in src:
                print(f"{main_dir}/{src}")

    print("done")


if __name__ == "__main__":
    main()
