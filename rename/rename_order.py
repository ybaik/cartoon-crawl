# -*- coding: utf-8 -*-

import os


def rename(base_path, files):
    for i, file in enumerate(files, start=1):
        _, ext = os.path.splitext(file)
        src_path = os.path.join(base_path, file)
        dst_path = f"{base_path}/{i:03d}{ext}"
        os.rename(src_path, dst_path)


def main():

    base_dir = "C:/comix/etc/a"
    vol_range = [31]

    for vol in range(vol_range[0], vol_range[-1] + 1):
        target_dir = f"{base_dir}/{vol:02d}"
        files = os.listdir(target_dir)
        files.sort()
        rename(target_dir, files)


if __name__ == "__main__":
    main()
