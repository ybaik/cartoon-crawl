# -*- coding: utf-8 -*-

import os
import shutil


def main():
    src_dir = r"C:/comix/완결_스캔/신세기 에반게리온 1-14(완)/13권"
    dst_dir = r"C:/comix/완결_스캔/신세기 에반게리온 1-14(완)/13"
    files = os.listdir(src_dir)
    files.sort()

    new_page = 1
    for file in files:
        name, ext = os.path.splitext(file)
        src_path = os.path.join(src_dir, file)
        dst_path = f"{dst_dir}/{new_page:03d}{ext}"
        shutil.copy2(src_path, dst_path)
        new_page += 1


if __name__ == "__main__":
    main()
