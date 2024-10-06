# -*- coding: utf-8 -*-

import os


def rename(base_path, episode, files):
    target_files = []
    for file in files:
        episode_src = file.split("-")[1]
        if episode_src != episode:
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

    base_dir = "C:/comix/etc/c"
    vol_range = [22, 22]

    for vol in range(vol_range[0], vol_range[-1] + 1):
        target_dir = f"{base_dir}/{vol:02d}"
        files = os.listdir(target_dir)
        files.sort()

        episodes = set()
        for file in files:
            episodes.add(file.split("-")[1])

        print(episodes)

        for episode in episodes:
            if episode == "000":
                continue
            rename(target_dir, episode, files)


if __name__ == "__main__":
    main()
