# -*- coding: utf-8 -*-

import os
import shutil


def rename(base_path, vol, files):
    target_files = []
    for file in files:
        vol_src = int(file.split("-")[1])
        if vol_src != vol:
            continue
        target_files.append(file)
    target_files.sort()

    for i, file in enumerate(target_files, start=1):
        name, ext = os.path.splitext(file)
        info = name.split("-")
        src_path = os.path.join(base_path, file)
        dst_path = f"{base_path}/{info[0]}-{info[1]}-{i:03d}{ext}"
        os.rename(src_path, dst_path)


def main():
    base_path = "D:/comix/etc/c/044"
    # base_path = "D:/comix/etc/원피스/096"

    files = os.listdir(base_path)
    files.sort()

    vols = set()
    for file in files:
        vols.add(int(file.split("-")[1]))

    print(vols)

    for vol in vols:
        if vol == 0:
            continue
        rename(base_path, vol, files)


if __name__ == "__main__":
    main()
