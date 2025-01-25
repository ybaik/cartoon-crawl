# -*- coding: utf-8 -*-

import os
import shutil


def main():
    base_dir = "C:/comix/etc/c"

    vol_list = [f"{v:02d}" for v in range(2, 6 + 1)]
    print(vol_list)
    # return

    for vol in vol_list:
        vol_dir = base_dir + "/" + vol
        files = os.listdir(vol_dir)

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

            src_path = f"{vol_dir}/{file}"
            dst_path = f"{vol_dir}/{info[0]}-{fixed:03d}-{info[2]}{ext}"
            os.rename(src_path, dst_path)


if __name__ == "__main__":
    main()
