# -*- coding: utf-8 -*-

import os
import shutil


def main():
    vol = 52
    # base_dir = f"C:/comix/etc/a/{vol:02d}"
    base_dir = f"C:/comix/etc/a/446화"
    dst_dir = f"C:/comix/etc/c/{vol:02d}"
    episode = 446
    page_range = [1, 29]

    files = os.listdir(base_dir)
    files.sort()
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)

    new_page = 4
    for file in files:
        name, ext = os.path.splitext(file)
        if len(name) > 3:
            continue

        page = int(name)
        if page < page_range[0] or page > page_range[-1]:
            continue

        file_new = f"{vol:02d}-{episode:03d}-{new_page:03d}{ext}"

        shutil.copyfile(os.path.join(base_dir, file), f"{dst_dir}/{file_new}")
        new_page += 1


if __name__ == "__main__":
    main()
