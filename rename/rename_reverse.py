# -*- coding: utf-8 -*-

import os
import shutil


def rename(base_dir, target_page, files):

    last_page = int(files[-1].split(".")[0]) + 10
    idx = len(files) - 1

    while idx:
        name, ext = os.path.splitext(files[idx])
        info = name.split(".")
        page = int(info[0])
        if target_page > page:
            break
        src_path = os.path.join(base_dir, files[idx])
        dst_path = f"{base_dir}/{last_page:03d}{ext}"
        os.rename(src_path, dst_path)
        last_page -= 1
        idx -= 1


def main():
    base_dir = r"C:/comix/etc/a/31"

    files = os.listdir(base_dir)
    files.sort()

    target_page = 11
    rename(base_dir, target_page, files)


if __name__ == "__main__":
    main()
