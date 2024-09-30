# -*- coding: utf-8 -*-

import os
import shutil


def main():
    vol = "14"
    base_path = f"C:/comix/etc/c/{vol}"
    bg_path = f"C:/comix/etc/c/00-000-000.png"
    episodes = dict()
    files = os.listdir(base_path)
    for file in files:
        name, ext = os.path.splitext(file)

        episode = name.split("-")[1]
        number = int(name.split("-")[-1])

        if episodes.get(episode) is None:
            episodes[episode] = number
        else:
            if episodes[episode] < number:
                episodes[episode] = number

    order = list(episodes.keys())
    order.sort()

    for e in order:
        print(e, episodes[e])
        page = episodes[e] + 10
        if e == "000":
            continue
        shutil.copyfile(bg_path, f"{base_path}/{vol}-{e}-{page}.png")


if __name__ == "__main__":
    main()
