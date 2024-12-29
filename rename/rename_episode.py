# -*- coding: utf-8 -*-

import os
import shutil


def main():
    base_path = "c:/comix/etc/c/04"

    start = 4
    dst_ep = 31
    src_eps = [34]
    # 34
    files = os.listdir(base_path)
    files.sort()
    for file in files:
        name, ext = os.path.splitext(file)

        eps = name.split("-")
        vol = int(eps[0])
        ep = int(eps[1])
        page = int(eps[2])

        if ep < src_eps[0] or ep > src_eps[-1]:
            continue

        # if ep == 16 and page > 24:
        #     continue

        new = f"{vol:02d}-{dst_ep:03d}-{start:03d}{ext}"
        # new = f"{vol:02d}-ext-{start:03d}{ext}"
        os.rename(f"{base_path}/{file}", f"{base_path}/{new}")
        start += 1


if __name__ == "__main__":
    main()
