# -*- coding: utf-8 -*-

import os
import shutil


def main():
    base_dir = "C:/comix/etc/c/check/12"

    files = os.listdir(base_dir)

    for file in files:
        name, ext = os.path.splitext(file)
        if ext not in [".jpg"]:
            print(file)
            continue
        info = name.split("-")
        episode = info[1]

        if episode == "000":
            continue

        num = int(episode)
        fixed = num - 1

        src_path = f"{base_dir}/{file}"
        dst_path = f"{base_dir}/{info[0]}-{fixed:03d}-{info[2]}{ext}"
        os.rename(src_path, dst_path)


if __name__ == "__main__":
    main()
