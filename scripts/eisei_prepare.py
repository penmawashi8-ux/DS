#!/usr/bin/env python3
"""公表問題PDFから正答（選択肢番号の前の「○」）を抜き出し、○を塗りつぶしたページ画像を作る。

使い方: eisei_prepare.py <PDF> <回ID> <画像出力先ディレクトリ>
  - eisei/<回ID>/seitou.json に {問番号: 正答番号} を書く（解答作成が終わるまで開かない）
  - 画像出力先に ○ を白塗りした page-NN.png を書く（解答作成はこちらを見て行う）
標準出力には件数しか出さない。
"""
import json
import re
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw

DPI = 150
WORD_RE = re.compile(r'<page width="[\d.]+" height="[\d.]+">|<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">([^<]*)</word>')
CHOICE_RE = re.compile(r"^(○?)（([１-５])）")
ZEN = "１２３４５"


def main():
    pdf, exam_id, img_dir = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3])
    out = Path(__file__).resolve().parent.parent / "eisei" / exam_id
    out.mkdir(parents=True, exist_ok=True)
    img_dir.mkdir(parents=True, exist_ok=True)
    bbox = subprocess.run(["pdftotext", "-bbox", str(pdf), "-"], capture_output=True, text=True, check=True).stdout

    page, marks, answers, q, last_choice = 0, {}, {}, 0, 0
    for m in WORD_RE.finditer(bbox):
        if m.group(1) is None:
            page += 1
            continue
        x0, y0, x1, y1, text = float(m[1]), float(m[2]), float(m[3]), float(m[4]), m[5]
        cm = CHOICE_RE.match(text)
        if not cm or x0 > 100:  # 行頭の選択肢番号だけを見る
            continue
        n = ZEN.index(cm[2]) + 1
        if n == 1 and last_choice != 1:
            q += 1
        last_choice = n
        if cm[1]:
            answers.setdefault(q, []).append(n)
            # ○ は「（」の左側 約13pt に描かれている
            marks.setdefault(page, []).append((x0 - 1, y0 - 1, x0 + 13, y1 + 1))

    bad = {k: v for k, v in answers.items() if len(v) != 1}
    (out / "seitou.json").write_text(
        json.dumps({str(k): v[0] for k, v in sorted(answers.items()) if len(v) == 1}, ensure_ascii=False, indent=1) + "\n",
        encoding="utf-8")

    subprocess.run(["pdftoppm", "-r", str(DPI), "-png", str(pdf), str(img_dir / "page")], check=True)
    s = DPI / 72
    for png in sorted(img_dir.glob("page-*.png")):
        p = int(re.search(r"(\d+)", png.stem)[1])
        if p not in marks:
            continue
        im = Image.open(png).convert("RGB")
        d = ImageDraw.Draw(im)
        for x0, y0, x1, y1 in marks[p]:
            d.rectangle([x0 * s, y0 * s, x1 * s, y1 * s], fill="white")
        im.save(png)
    print(f"questions={q} answered={len(answers)} irregular={sorted(bad)} masked_pages={sorted(marks)}")


if __name__ == "__main__":
    main()
