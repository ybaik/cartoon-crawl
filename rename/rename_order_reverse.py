# -*- coding: utf-8 -*-

import os
import shutil


def rename(base_path, target_episode, target_page, files):
    target_files = []
    for file in files:
        tags = file.split("-")
        if tags[1] == "ext":
            continue
        episode_src = int(tags[1])
        if episode_src != target_episode:
            continue
        target_files.append(file)
    target_files.sort()

    last_page = int(target_files[-1].split("-")[-1].split(".")[0]) + 1
    idx = len(target_files) - 1

    while idx:
        name, ext = os.path.splitext(target_files[idx])
        info = name.split("-")
        page = int(info[2])
        if target_page > page:
            break
        src_path = os.path.join(base_path, target_files[idx])
        dst_path = f"{base_path}/{info[0]}-{info[1]}-{last_page:03d}{ext}"

        os.rename(src_path, dst_path)

        last_page -= 1
        idx -= 1


def main():
    base_path = r"C:/comix/etc/c/13"

    files = os.listdir(base_path)
    files.sort()

    target_episode = 141
    target_page = 1

    rename(base_path, target_episode, target_page, files)


if __name__ == "__main__":
    main()
