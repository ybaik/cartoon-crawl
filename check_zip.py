# -*- coding: utf-8 -*-

import os
from zipfile import ZipFile

main_dirs = ["미완", "미완_스캔", "연재중", "연재중_스캔", "완결", "완결_스캔"]


def check_zip(base_dir):
    cands = os.listdir(base_dir)

    for cand in cands:
        cand_path = os.path.join(base_dir, cand)
        if os.path.isdir(cand_path):
            print(f"{cand_path}, dir???")
            continue
        name, ext = os.path.splitext(cand)
        if ext != ".zip":
            continue

        cnt = 0
        with ZipFile(cand_path, "r") as zipObj:
            listOfFileNames = zipObj.namelist()
            for fileName in listOfFileNames:
                if ".." in fileName:
                    cnt += 1
        if cnt:
            print(cand_path)


def main():
    base_dir = "z:/"

    for main_dir in main_dirs:
        main_dir_src = f"{base_dir}/{main_dir}"

        if not os.path.exists(main_dir_src):
            continue

        dirs_src = os.listdir(main_dir_src)

        for comix in dirs_src:
            comix_dir = os.path.join(main_dir_src, comix)
            if os.path.isdir(comix_dir):
                check_zip(comix_dir)


if __name__ == "__main__":
    main()
