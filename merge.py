# -*- coding: utf-8 -*-

import os
import shutil


def main():

    base_path = "D:\comix\기타작업/트라이건"
    save_path = "D:\comix\기타작업/트라이건"

    start_index = 1
    end_index = start_index + 2
    end_range = 3

    for i in range(start_index, end_index):
        target = f"{save_path}/{i}권"
        os.makedirs(target, exist_ok=True)

        idx = 1
        for j in range(1, end_range + 1):
            # for j in ["전", "후"]:
            src_path = f"{base_path}/{i}-{j}권"
            dir_list = os.listdir(src_path)
            for f in dir_list:
                shutil.copyfile(f"{src_path}/{f}", f"{target}/{idx:03d}.jpg")
                idx += 1

        ful = len(os.listdir(target))
        sum = 0
        for j in range(1, end_range + 1):
            # for j in ["전", "후"]:
            src_path = f"{base_path}/{i}-{j}권"
            sum += len(os.listdir(src_path))
        print(i, ful, sum)
        if ful != sum:
            print(i)
            continue
        continue


if __name__ == "__main__":
    main()
