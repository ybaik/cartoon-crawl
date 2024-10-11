# -*- coding: utf-8 -*-

import os
import shutil


def main():

    base_path = "c:/comix/etc/a"
    save_path = "c:/comix/etc/a"

    start_index = 52
    end_index = start_index + 1
    end_range = 2

    for i in range(start_index, end_index):
        target = f"{save_path}/{i}화"
        os.makedirs(target, exist_ok=True)

        idx = 1
        for j in range(1, end_range + 1):
            src_path = f"{base_path}/{i}-{j}화"
            # for j in ["전", "후"]:
            #     src_path = f"{base_path}/{i}권 - {j}"
            dir_list = os.listdir(src_path)
            for f in dir_list:
                shutil.copyfile(f"{src_path}/{f}", f"{target}/{idx:03d}.jpg")
                idx += 1

        ful = len(os.listdir(target))
        sum = 0
        for j in range(1, end_range + 1):
            src_path = f"{base_path}/{i}-{j}화"
            # for j in ["전", "후"]:
            #     src_path = f"{base_path}/{i}권 - {j}"
            sum += len(os.listdir(src_path))
        print(i, ful, sum)
        if ful != sum:
            print(i)
            continue
        continue


def merge():
    base_path = "c:/comix/etc/a"
    save_path = "c:/comix/etc/b"

    target = 13
    target = f"{save_path}/{target:02d}"
    os.makedirs(target, exist_ok=True)

    idx = 1
    for j in [21]:
        src_path = f"{base_path}/{j:02d}화"
        dir_list = os.listdir(src_path)
        for f in dir_list:
            shutil.copyfile(f"{src_path}/{f}", f"{target}/{idx:03d}.jpg")
            idx += 1


if __name__ == "__main__":
    main()
    # merge()
