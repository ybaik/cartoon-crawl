# -*- coding: utf-8 -*-

import os


def rename(base_dir, target_page, files):
    last_page = int(files[-1].split(".")[0]) + 10

    for file in reversed(files):
        name, ext = os.path.splitext(file)
        info = name.split(".")
        page = int(info[0])
        if target_page > page:
            break
        src_path = os.path.join(base_dir, file)
        dst_path = os.path.join(base_dir, f"{last_page:03d}{ext}")
        os.rename(src_path, dst_path)
        last_page -= 1


def main():
    base_dir = r"C:/comix/etc/a/31"
    target_page = 11

    rename(base_dir, target_page, sorted(os.listdir(base_dir)))


if __name__ == "__main__":
    main()
