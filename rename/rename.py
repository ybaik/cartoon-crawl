# -*- coding: utf-8 -*-

import os
import shutil


def main():
    base_dir = "d:/comix/완결"
    vols = os.listdir(base_dir)
    for vol in vols:
        tag = vol.split(" ")[-1]
        new = vol.removesuffix(tag)
        if new != vol:
            os.rename(f"{base_dir}/{vol}", f"{base_dir}/{new}")


if __name__ == "__main__":
    main()
