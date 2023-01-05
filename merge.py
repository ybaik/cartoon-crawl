# -*- coding: utf-8 -*-

import os
import shutil


def main():

    base_path = "D:\comix\기타작업/창천항로"
    save_path = "D:\comix\기타작업/창천항로"

    for i in range(31, 32):
        target = f"{save_path}/{i:02d}권"
        ful = len(os.listdir(target))

        sum = 0
        for j in range(1, 4):
            src_path = f"{base_path}/{i}권 - {j}부"
            sum += len(os.listdir(src_path))
        print(ful, sum)
        if ful != sum:
            print(i)
            continue
        continue
        target = f"{save_path}/{i:02d}권"
        os.makedirs(target, exist_ok=True)

        idx = 1
        for j in range(1, 4):
            src_path = f"{base_path}/{i}권 - {j}부"
            dir_list = os.listdir(src_path)
            for f in dir_list:
                shutil.copyfile(f"{src_path}/{f}", f"{target}/{idx:03d}.jpg")
                idx += 1


if __name__ == "__main__":
    main()
