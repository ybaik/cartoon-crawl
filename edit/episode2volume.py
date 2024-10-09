# -*- coding: utf-8 -*-

import os
import cv2
import shutil
import numpy as np


episode2vol = {
    16: [108, 111],
}


def gen_bg_img(h, w):
    white_image = np.full((h, w, 1), 255, dtype=np.uint8)
    return white_image


def main():
    skip_1page = False
    keep_1page_for_1st_episode = False
    skip_last_page = False
    base_dir = "c:/comix/etc/b"
    base_dir1 = "c:/comix/etc/c"
    # bgfile = "c:/comix/etc/c/white.png"
    bgfile = "c:/comix/etc/c/in_white.png"
    add_bg_file = True

    # img = gen_bg_img(1080, 720)
    # cv2.imwrite(bgfile, img)

    for k in episode2vol.keys():
        [s, e] = episode2vol.get(k)
        target = f"{base_dir1}/{k:02d}"
        os.makedirs(target, exist_ok=True)

        for episode in range(s, e + 1):
            # src_dir = f"{base_dir}/{episode:03d}"
            src_dir = f"{base_dir}/{episode}"
            if not os.path.exists(src_dir):
                print(src_dir)
                continue

            page = 3  # will be ordered later
            files = os.listdir(src_dir)
            for j, f in enumerate(files):

                if skip_1page:
                    if not keep_1page_for_1st_episode or episode != s:
                        if j < 1:
                            continue
                if skip_last_page and j == (len(files) - 1):
                    continue

                _, ext = os.path.splitext(f)

                if keep_1page_for_1st_episode and episode == s and j == 0:
                    shutil.copyfile(f"{src_dir}/{f}", f"{target}/{k:02d}-000-000{ext}")
                else:
                    shutil.copyfile(
                        f"{src_dir}/{f}",
                        f"{target}/{k:02d}-{episode:03d}-{page:03d}{ext}",
                    )
                page += 1

            if add_bg_file:
                if episode < e:
                    shutil.copyfile(
                        bgfile, f"{target}/{k:02d}-{episode:03d}-{page:03d}{ext}"
                    )

    # Ext
    # # return
    # episode2vol["ext"] = ["80.5화"]
    # if episode2vol.get("ext") is not None:
    #     dsts = episode2vol.get("ext")
    #     cnt = 1
    #     v = list(episode2vol.keys())[0]
    #     target = f"{base_dir1}/{v:02d}"
    #     for dst in dsts:
    #         src_dir = f"{base_dir}/{dst}"

    #         if not os.path.exists(src_dir):
    #             print(src_dir)
    #             continue

    #         files = os.listdir(src_dir)
    #         for f in files:
    #             _, ext = os.path.splitext(f)
    #             shutil.copyfile(
    #                 f"{src_dir}/{f}", f"{target}/{v:02d}-ext-{cnt:03d}{ext}"
    #             )
    #             cnt += 1


if __name__ == "__main__":
    main()
