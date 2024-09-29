# -*- coding: utf-8 -*-

import os
import shutil


def main():
    base_path = "c:/comix/etc/b"
    # base_path = "D:/comix/etc/b/3권"

    els = os.listdir(base_path)
    for i, el in enumerate(els):
        new = el
        # print(el)
        # if el[-1] != "권":
        #     continue
        # if len(el) == 3:
        #     os.rename(f"{base_path}/{el}", f"{base_path}/0{el}")
        if len(el) == 2:
            new = f"0{el}"
        # new = el.replace("권", "")
        # new = f"{el}권"
        if new != el:
            os.rename(f"{base_path}/{el}", f"{base_path}/{new}")


if __name__ == "__main__":
    main()
