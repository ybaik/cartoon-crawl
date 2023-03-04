# -*- coding: utf-8 -*-

import os
import shutil

episode2vol = {
    1: [4, 5],
    # 2: [8, 17],
}


def main():
    base_path = "D:/comix/etc/바질리스크 오우카인법첩"
    base_path1 = "D:/comix/etc/바질리스크a"

    for k in episode2vol.keys():
        [s, e] = episode2vol.get(k)
        target = f"{base_path1}/{k:02d}"
        os.makedirs(target, exist_ok=True)

        # first_start_index = True
        for i in range(s, e + 1):
            src_dir = f"{base_path}/{i}화"

            if not os.path.exists(src_dir):
                print(src_dir)
                continue

            files = os.listdir(src_dir)

            for j, f in enumerate(files):

                # if j == 0:
                #     if not first_start_index:
                #         continue
                #     first_start_index = False

                [id, ext] = f.split(".")
                if i < 1000:
                    shutil.copyfile(
                        f"{src_dir}/{f}", f"{target}/{k:02d}-{i:03d}-{id}.{ext}"
                    )
                else:
                    shutil.copyfile(
                        f"{src_dir}/{f}", f"{target}/{k:02d}-last-ball-{id}.{ext}"
                    )


if __name__ == "__main__":
    main()
