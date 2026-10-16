#!/usr/bin/env python3
"""自作解答（kaitou_kaisetsu.md の解答一覧）と公式正答（seitou.json）を突き合わせ、shougou.md を作る。

使い方: eisei_shougou.py <回ID> [参考扱いにする問番号 ...]
"""
import json
import re
import sys
from pathlib import Path

ROW_RE = re.compile(r"^\|\s*(\d+)\s*\|\s*(\d)\s*\|\s*$")


def main():
    exam_id = sys.argv[1]
    peeked = {int(x) for x in sys.argv[2:]}
    d = Path(__file__).resolve().parent.parent / "eisei" / exam_id
    mine = {}
    for line in (d / "kaitou_kaisetsu.md").read_text(encoding="utf-8").splitlines():
        m = ROW_RE.match(line)
        if m:
            mine[int(m[1])] = int(m[2])
    official = {int(k): v for k, v in json.loads((d / "seitou.json").read_text(encoding="utf-8")).items()}

    rows, wrong = [], []
    for q in sorted(official):
        ok = mine.get(q) == official[q]
        mark = "◎" if ok else "×"
        note = "（正答を見た状態で作成）" if q in peeked else ""
        rows.append(f"| 問{q} | {official[q]} | {mine.get(q, '－')} | {mark} | {note} |")
        if not ok:
            wrong.append(q)
    blind = [q for q in official if q not in peeked]
    blind_ok = sum(mine.get(q) == official[q] for q in blind)

    md = [
        f"# 照合結果（{exam_id}）",
        "",
        "> 照合元：PDF内で選択肢番号の前に「○」が付いた選択肢（協会の公表する正答）",
        "> 自作解答（`kaitou_kaisetsu.md`）は照合前にコミット済みで、照合後も書き換えていない。",
        "",
        "## サマリ",
        "",
        f"- 全{len(official)}問中 **{len(official) - len(wrong)}問一致**",
        f"- 正答を見ずに解いた{len(blind)}問では **{blind_ok}/{len(blind)}問一致**",
        f"- 不一致：{'、'.join(f'問{q}' for q in wrong) if wrong else 'なし'}",
        "",
        "| 問 | 公式正答 | 自作 | 判定 | 備考 |",
        "|---|---|---|---|---|",
        *rows,
        "",
    ]
    (d / "shougou.md").write_text("\n".join(md), encoding="utf-8")
    print("\n".join(md[6:10]))


if __name__ == "__main__":
    main()
