# -*- coding: utf-8 -*-

import os
import shutil

episode2vol = {
    9: [57, 62]
    # 45: [395, 402]
    # 107: [1077, 1088],
    # 21: [192, 201],  # 66
}


def main():
    skip_1page = False
    base_dir = "c:/comix/etc/a"
    base_dir1 = "c:/comix/etc/c"
    bgfile = "c:/comix/etc/c/white.png"
    add_bg_file = False

    for k in episode2vol.keys():
        [s, e] = episode2vol.get(k)
        target = f"{base_dir1}/{k:02d}"
        os.makedirs(target, exist_ok=True)

        for vol_idx, i in enumerate(range(s, e + 1)):
            # src_dir = f"{base_dir}/{i:02d}화"
            src_dir = f"{base_dir}/{i}화"
            if not os.path.exists(src_dir):
                print(src_dir)
                continue

            idx = 3  # will be ordered later
            files = os.listdir(src_dir)
            for j, f in enumerate(files):
                if skip_1page and j < 1:
                    continue
                [id, ext] = f.split(".")
                shutil.copyfile(
                    f"{src_dir}/{f}", f"{target}/{k:02d}-{i:03d}-{idx:03d}.{ext}"
                )
                idx += 1

            # if add_bg_file:
            #     if i < e:
            #         shutil.copyfile(bgfile, f"{target}/{k:03d}-{i:04d}-{idx:03d}.{ext}")

    # Ext
    return
    episode2vol["ext"] = ["2권 번외편"]
    if episode2vol.get("ext") is not None:
        dsts = episode2vol.get("ext")
        cnt = 1
        v = list(episode2vol.keys())[0]
        target = f"{base_dir1}/{v:02d}"
        for dst in dsts:
            src_dir = f"{base_dir}/{dst}"

            if not os.path.exists(src_dir):
                print(src_dir)
                continue

            files = os.listdir(src_dir)

            for j, f in enumerate(files):
                if j == 0:
                    continue
                [id, ext] = f.split(".")
                shutil.copyfile(
                    f"{src_dir}/{f}", f"{target}/{v:02d}-ext-{cnt:03d}.{ext}"
                )
                cnt += 1


if __name__ == "__main__":
    main()