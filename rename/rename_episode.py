# -*- coding: utf-8 -*-

import os
import shutil


def main():
    base_path = "c:/comix/etc/c/22"

    src_epi = 183
    start = 4
    dst_epi = 229

    pages = os.listdir(base_path)
    for page in pages:
        name, ext = os.path.splitext(page)

        eps = name.split("-")

        if int(eps[1]) != src_epi:
            continue

        p = int(eps[2])

        if p < start:
            continue

        new = f"{eps[0]}-{dst_epi:03d}-{eps[2]}{ext}"
        print(new)
        os.rename(f"{base_path}/{page}", f"{base_path}/{new}")


if __name__ == "__main__":
    main()
