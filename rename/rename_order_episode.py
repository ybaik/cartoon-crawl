# -*- coding: utf-8 -*-

import os


def numbering_000(base_dir, vol, files):

    list_000 = []
    for file in files:
        if not file.split("-")[1] == "000":
            continue
        list_000.append(file)

    list_000.sort(reverse=True)

    for file in list_000:
        name, ext = os.path.splitext(file)
        num = int(name.split("-")[-1])

        src_path = f"{base_dir}/{vol:02d}/{file}"
        dst_path = f"{base_dir}/{vol:02d}/{vol:02d}-000-{num+1:03d}{ext}"
        os.rename(src_path, dst_path)


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

    base_dir = "C:/comix/etc/cc"
    vol_range = [1]
    for vol in range(vol_range[0], vol_range[-1] + 1):
        target_dir = f"{base_dir}/{vol:02d}"
        files = os.listdir(target_dir)
        files.sort()

        episodes = set()
        for file in files:
            episode = file.split("-")[1]
            episodes.add(episode)

        for episode in episodes:
            if episode == "000" and (
                f"{vol:02d}-000-000.png" in files or f"{vol:02d}-000-000.jpg" in files
            ):
                numbering_000(base_dir, vol, files)
            else:
                rename(target_dir, episode, files)

        episodes = list(episodes)
        episodes.sort()
        print(episodes)


if __name__ == "__main__":
    main()
