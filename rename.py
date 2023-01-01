# -*- coding: utf-8 -*-

import os
import shutil


def main():
    base_path = "D:\comix\신의 물방울"

    els = os.listdir(base_path)
    for el in els:
        print(el)
        if el[-1] != "권":
            continue
        # if len(el) == 3:
        #     os.rename(f"{base_path}/{el}", f"{base_path}/0{el}")
        if len(el) == 2:
            os.rename(f"{base_path}/{el}", f"{base_path}/0{el}")


if __name__ == "__main__":
    main()
