# -*- coding: utf-8 -*-

import os
import shutil


def main():
    base_path = "D:\comix\연재중\카드캡터 사쿠라 클리어 카드"

    els = os.listdir(base_path)
    for i, el in enumerate(els):
        print(el)
        # if el[-1] != "권":
        #     continue
        # if len(el) == 3:
        #     os.rename(f"{base_path}/{el}", f"{base_path}/0{el}")
        # if len(el) == 2:
        #     os.rename(f"{base_path}/{el}", f"{base_path}/0{el}")
        new = el.replace("클… 카드 편 ", "")
        os.rename(f"{base_path}/{el}", f"{base_path}/{new}")


if __name__ == "__main__":
    main()
