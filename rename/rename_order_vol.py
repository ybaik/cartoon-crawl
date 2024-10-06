# -*- coding: utf-8 -*-

import os
import shutil


def main():

    base_dir = "C:/comix/etc/d"

    for i in range(1, 9):
        src_dir = f"{base_dir}/{i:02d}권"
        dst_dir = f"{base_dir}/{i:02d}"
        files = os.listdir(src_dir)
        files.sort()

        if os.path.exists(dst_dir):
            os.rmdir(dst_dir)
        os.makedirs(dst_dir)

        new_page = 1
        for file in files:
            name, ext = os.path.splitext(file)
            src_path = os.path.join(src_dir, file)
            dst_path = f"{dst_dir}/{new_page:03d}{ext}"
            shutil.copy2(src_path, dst_path)
            new_page += 1


if __name__ == "__main__":
    main()
