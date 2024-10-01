# -*- coding: utf-8 -*-

import os
import shutil


def main():
    base_path = "c:/comix/etc/a"
    # base_path = "D:/comix/etc/b/3권"

    els = os.listdir(base_path)
    for i, el in enumerate(els):
        new = el
        new = new.replace(" ", "")
        new = new.replace("마법기사레이어스", "")
        if new != el:
            os.rename(f"{base_path}/{el}", f"{base_path}/{new}")


if __name__ == "__main__":
    main()
