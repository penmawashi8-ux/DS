#!/usr/bin/env python3
"""mondai.md と kaitou_kaisetsu.md を問ごとに組み合わせ、note に貼る下書き note_draft.md を作る。

使い方: eisei_note.py <回ID> [無料公開する問の数（既定 3）]
有料部分の開始位置に「ここから有料」の目印を入れる（note の有料ラインはエディタ上で手動設定）。
"""
import re
import sys
from pathlib import Path

Q_RE = re.compile(r"^###\s*問(\d+)", re.M)


def split(md):
    parts = {}
    ms = list(Q_RE.finditer(md))
    for i, m in enumerate(ms):
        end = ms[i + 1].start() if i + 1 < len(ms) else len(md)
        body = md[m.end():end]
        body = re.split(r"^##\s", body, flags=re.M)[0]  # 次の科目見出しは含めない
        parts[int(m[1])] = body.strip()
    return parts


def main():
    exam_id = sys.argv[1]
    free = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    d = Path(__file__).resolve().parent.parent / "eisei" / exam_id
    mondai = (d / "mondai.md").read_text(encoding="utf-8")
    kaisetsu = (d / "kaitou_kaisetsu.md").read_text(encoding="utf-8")
    source = "\n".join(l for l in mondai.splitlines()[:5] if l.startswith(">"))
    qs, ks = split(mondai), split(kaisetsu)

    out = [
        "# 【全30問・全選択肢解説】第二種衛生管理者 公表問題（令和8年10月掲載分）",
        "",
        "安全衛生技術試験協会が公表している第二種衛生管理者試験の問題を、1問ずつ"
        "「どこが誤りか」「正しくは何か」まで選択肢ごとに解説します。",
        "",
        source,
        "",
        f"問1〜問{free}は無料で読めます。",
        "",
    ]
    for q in sorted(qs):
        title, _, body = ks[q].partition("\n")
        out += [f"## 問{q}　{title.split('―')[0].strip()}", "", qs[q], "",
                # note はHTMLを表示できないので、折りたたみは使わず見出しで区切る
                "### ▶ 解答と解説", "",
                f"**解答：{title.split('解答')[-1].strip()}**", "", body.strip(), ""]
        if q == free:
            out += ["---", "", "**▼ ここから有料（note エディタで有料ラインを設定）**", "", "---", ""]
    out += ["---", "",
            "※ 解説は作成者の見解です。正答は協会の公表問題（○印）と照合済みです。"
            "法令は令和7年12月31日時点の内容で、その後の改正は反映していません。", ""]
    (d / "note_draft.md").write_text("\n".join(out), encoding="utf-8")
    print(f"wrote {d / 'note_draft.md'} ({len(qs)} questions, free={free})")


if __name__ == "__main__":
    main()
