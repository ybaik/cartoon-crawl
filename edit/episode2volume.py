# -*- coding: utf-8 -*-

import os
import shutil


episode2vol = {
    23: [378, 378],
}


def main():
    skip_1page = True
    keep_1page_for_1st_episode = True
    skip_last_page = False
    base_dir = "c:/comix/etc/a"
    base_dir1 = "c:/comix/etc/c"
    bgfile = "c:/comix/etc/c/bg.jpg"
    add_bg_file = False

    for k in episode2vol.keys():
        [s, e] = episode2vol.get(k)
        target = f"{base_dir1}/{k:02d}"
        os.makedirs(target, exist_ok=True)

        for episode in range(s, e + 1):
            src_dir = f"{base_dir}/{episode:03d}"
            # src_dir = f"{base_dir}/{episode}화"
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
