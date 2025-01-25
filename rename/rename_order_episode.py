# -*- coding: utf-8 -*-

import os


def rename(base_path, episode, files):
    target_files = [f for f in files if f.split("-")[1] == episode]
    target_files.sort()

    for i, file in enumerate(target_files, start=1):
        name, ext = os.path.splitext(file)
        info = name.split("-")
        src_path = os.path.join(base_path, file)
        dst_path = f"{base_path}/{info[0]}-{info[1]}-{i:03d}{ext}"
        os.rename(src_path, dst_path)


def main():

    base_dir = "C:/comix/etc/dd"
    vol_range = [51, 63]
    for vol in range(vol_range[0], vol_range[-1] + 1):
        target_dir = f"{base_dir}/{vol:02d}"
        files = os.listdir(target_dir)
        files.sort()

        episodes = set()
        for file in files:
            episode = file.split("-")[1]
            episodes.add(episode)

        for episode in episodes:
            # if episode == "000":
            #     continue
            rename(target_dir, episode, files)

        episodes = list(episodes)
        episodes.sort()
        print(episodes)


if __name__ == "__main__":
    main()
