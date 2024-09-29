# -*- coding: utf-8 -*-

import os


def rename(base_dir, target_page, target_files):

    last_page = int(target_files[-1].split(".")[0]) + 1
    idx = len(target_files) - 1

    while idx:
        name, ext = os.path.splitext(target_files[idx])
        page = int(name)
        if target_page > page:
            break
        src_path = os.path.join(base_dir, target_files[idx])
        dst_path = f"{base_dir}/{last_page:03d}{ext}"

        os.rename(src_path, dst_path)

        last_page -= 1
        idx -= 1


def main():
    src_dir = r"C:/comix/완결_스캔/신세기 에반게리온 1-14(완)/14권"

    files = os.listdir(src_dir)
    files.sort()
    target_page = 72
    rename(src_dir, target_page, files)


if __name__ == "__main__":
    main()
