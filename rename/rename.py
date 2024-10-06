# -*- coding: utf-8 -*-

import os
import shutil


def main():
    base_path = "c:/comix/etc/a"
    target_path = "c:/comix/etc/e/"

    els = os.listdir(base_path)
    for el in els:
        new = el.replace(" ", "")
        if new != el:
            os.rename(f"{base_path}/{el}", f"{base_path}/{new}")


if __name__ == "__main__":
    main()
