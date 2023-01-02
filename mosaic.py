# -*- coding: utf-8 -*-

import cv2

patterns = [  # dh, dw, sh, sw
    [0, 0, 0, 4],
    [0, 1, 1, 4],
    [0, 2, 3, 1],
    [0, 3, 3, 4],
    [0, 4, 1, 2],
    [1, 0, 0, 2],
    [1, 1, 3, 0],
    [1, 2, 4, 0],
    [1, 3, 0, 1],
    [1, 4, 1, 0],
    [2, 0, 3, 3],
    [2, 1, 2, 3],
    [2, 2, 3, 2],
    [2, 3, 1, 3],
    [2, 4, 4, 2],
    [3, 0, 4, 3],
    [3, 1, 0, 0],
    [3, 2, 2, 4],
    [3, 3, 4, 4],
    [3, 4, 2, 1],
    [4, 0, 2, 2],
    [4, 1, 4, 1],
    [4, 2, 0, 3],
    [4, 3, 2, 0],
    [4, 4, 1, 1],
]


def main():
    base_path = "D:\comix\download/147"
    save_path = "D:\comix\download/147-1"

    vertical_align = False

    for i in range(1, 21):
        src = f"{base_path}/{i:03}.jpg"
        # 5, 5
        img = cv2.imread(src)
        h, w, c = img.shape
        block_h = int(h / 5)
        block_w = int(w / 5)
        # cv2.imwrite(f"{save_path}/test.png", img[0:72, :, :])
        # cv2.imwrite(f"{save_path}/test.png", img[72:180, :, :])
        # cv2.imwrite(f"{save_path}/test.png", img[180:216, :, :])
        # cv2.imwrite(f"{save_path}/test.png", img[216:360, :, :])
        # cv2.imwrite(f"{save_path}/test.png", img[360:540 :, :])
        # cv2.imwrite(f"{save_path}/test.png", img[540:648:, :])
        # cv2.imwrite(f"{save_path}/test.png", img[648:864:, :])
        # cv2.imwrite(f"{save_path}/test.png", img[864:, :, :])
        img_dst = img.copy()

        # vertical align
        if vertical_align:
            img_dst[0:144, :, :] = img[216:360, :, :]
            img_dst[144:216, :, :] = img[0:72, :, :]
            img_dst[216:324, :, :] = img[72:180, :, :]
            img_dst[324:432, :, :] = img[540:648, :, :]
            img_dst[432:612, :, :] = img[360:540, :, :]
            img_dst[612:648, :, :] = img[180:216, :, :]
            dst = f"{save_path}/{i:03}.png"
            img = cv2.imwrite(dst, img_dst)
            continue

        # pattern align
        for pattern in patterns:
            dpos = pattern[:2]
            spos = pattern[2:]

            sh = spos[0] * block_h
            sw = spos[1] * block_w
            dh = dpos[0] * block_h
            dw = dpos[1] * block_w
            img_dst[dh : dh + block_h, dw : dw + block_w, :] = img[
                sh : sh + block_h, sw : sw + block_w, :
            ]

        # cv2.imshow("t", img_dst)
        # cv2.waitKey(0)
        # continue
        dst = f"{save_path}/{i:03}.jpg"
        img = cv2.imwrite(dst, img_dst)


if __name__ == "__main__":
    main()
