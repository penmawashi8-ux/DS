#!/usr/bin/env python3
"""note の見出し画像（1280×670）を作る。

使い方: eisei_header.py <出力PNG> <試験名> <掲載回> [問題数]
例: eisei_header.py eisei/2026r08_2ei/header.png 第二種衛生管理者 "令和8年10月掲載分" 30
note の一覧では左右が切れることがあるので、主要な文字は中央寄せにしている。
"""
import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1280, 670
FONT = "/usr/share/fonts/opentype/ipafont-gothic/ipag.ttf"
GREEN, DARK, CREAM, ACCENT, WHITE = "#1f6f5c", "#14493d", "#fbf7ee", "#f2b33d", "#ffffff"


def font(size):
    return ImageFont.truetype(FONT, size)


def center(d, y, text, size, fill, bold=0):
    f = font(size)
    w = d.textlength(text, font=f)
    d.text(((W - w) / 2, y), text, font=f, fill=fill, stroke_width=bold, stroke_fill=fill)


def pill(d, cx, y, text, size, bg, fg):
    f = font(size)
    w = d.textlength(text, font=f)
    pad_x, pad_y = 28, 12
    box = (cx - w / 2 - pad_x, y, cx + w / 2 + pad_x, y + size + pad_y * 2)
    d.rounded_rectangle(box, radius=(size + pad_y * 2) // 2, fill=bg)
    d.text((cx - w / 2, y + pad_y - 2), text, font=f, fill=fg, stroke_width=1, stroke_fill=fg)


def main():
    out, exam, issue = sys.argv[1], sys.argv[2], sys.argv[3]
    n = sys.argv[4] if len(sys.argv) > 4 else "30"
    im = Image.new("RGB", (W, H), GREEN)
    d = ImageDraw.Draw(im)
    # 背景：斜めの帯で単調さを避ける
    d.polygon([(0, H), (W * 0.42, H), (W * 0.62, 0), (W * 0.2, 0)], fill="#237a65")
    d.rectangle((0, H - 18, W, H), fill=DARK)
    # 中央カード
    d.rounded_rectangle((110, 70, W - 110, H - 80), radius=36, fill=CREAM)

    pill(d, W / 2, 104, f"公表問題　全{n}問", 34, GREEN, WHITE)
    center(d, 200, exam, 104, DARK, bold=2)
    center(d, 335, "全選択肢を", 56, DARK, bold=1)
    # 強調語の下にマーカー線
    f = font(76)
    label = "ていねい解説"
    w = d.textlength(label, font=f)
    x = (W - w) / 2
    d.rectangle((x - 6, 470, x + w + 6, 496), fill=ACCENT)
    d.text((x, 405), label, font=f, fill=DARK, stroke_width=2, stroke_fill=DARK)
    center(d, 530, f"{issue}　／　正答照合済み", 30, "#3d5a52")
    im.save(out, optimize=True)
    print(f"wrote {out} ({W}x{H})")


if __name__ == "__main__":
    main()
