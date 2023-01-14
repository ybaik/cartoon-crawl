# -*- coding: utf-8 -*-

import os
import shutil


def main():
    base_path = "D:/comix/기타작업/인고시마"

    dirs = os.listdir(base_path)
    for folder in enumerate(dirs):
        tp = f"{base_path}/{folder}"
        if not os.path.isdir(tp):
            continue
        fs = os.listdir(tp)

        if len(fs) == 0:
            print(folder)
    print("done")

if __name__ == "__main__":
    main()
