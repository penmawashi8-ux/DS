#!/usr/bin/env python3
"""mondai.md と kaitou_kaisetsu.md を問ごとに組み合わせ、note に貼る下書きを作る。

使い方: eisei_note.py <回ID> [無料公開する問の数（既定 3）]
  - note_draft.md   … 下書き（確認用）
  - note_draft.html … ブラウザで開いて全選択→コピー→note エディタに貼り付ける用
note のエディタは表・HTMLの折りたたみに対応しないので、表は1行ずつの文に直す。
有料ラインの位置には目印を入れる（実際のラインは note エディタ上で設定する）。
"""
import html
import re
import sys
from pathlib import Path

Q_RE = re.compile(r"^###\s*問(\d+)", re.M)
PAY_MARK = "▼▼▼ ここに有料ラインを設定 ▼▼▼"


def split(md):
    parts = {}
    ms = list(Q_RE.finditer(md))
    for i, m in enumerate(ms):
        end = ms[i + 1].start() if i + 1 < len(ms) else len(md)
        body = re.split(r"^##\s", md[m.end():end], flags=re.M)[0]  # 次の科目見出しは含めない
        parts[int(m[1])] = body.strip()
    return parts


def for_note(body):
    """選択肢の番号付きリストを試験と同じ（1）表記に、表を1行ずつの文に直す。"""
    out, header = [], None
    for line in body.splitlines():
        s = line.strip()
        if s.startswith("|"):
            cells = [c.strip() for c in s.strip("|").split("|")]
            if set("".join(cells)) <= set("-: "):
                continue
            if header is None:
                header = cells
                continue
            label, vals = cells[0], cells[1:]
            out.append(f"{label}　" + "　".join(f"{h}：{v}" for h, v in zip(header[1:], vals)))
            continue
        header = None
        m = re.match(r"^(\d)\.\s+(.*)", s)
        out.append(f"（{m[1]}）{m[2]}" if m else line.rstrip())
    return "\n".join(out)


def inline(s):
    s = html.escape(s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    return re.sub(r"(https?://\S+)", r'<a href="\1">\1</a>', s)


def to_html(md):
    """note に貼る用の最小限の変換（見出し・段落・箇条書き・引用・区切り線・太字）。"""
    out, para, ul, quote = [], [], [], []

    def flush():
        if para:
            out.append("<p>" + "<br>".join(inline(x) for x in para) + "</p>")
            para.clear()
        if ul:
            out.append("<ul>" + "".join(f"<li>{inline(x)}</li>" for x in ul) + "</ul>")
            ul.clear()
        if quote:
            out.append("<blockquote><p>" + "<br>".join(inline(x) for x in quote) + "</p></blockquote>")
            quote.clear()

    for line in md.splitlines():
        s = line.strip()
        if not s:
            flush()
        elif m := re.match(r"^(#{1,3})\s+(.*)", s):
            flush()
            out.append(f"<h{len(m[1])}>{inline(m[2])}</h{len(m[1])}>")
        elif s == "---":
            flush()
            out.append("<hr>")
        elif s.startswith(">"):
            quote.append(s.lstrip("> ").strip())
        elif s.startswith("- "):
            ul.append(s[2:])
        else:
            para.append(s)
    flush()
    return "\n".join(out)


def main():
    exam_id = sys.argv[1]
    free = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    d = Path(__file__).resolve().parent.parent / "eisei" / exam_id
    mondai = (d / "mondai.md").read_text(encoding="utf-8")
    kaisetsu = (d / "kaitou_kaisetsu.md").read_text(encoding="utf-8")
    source = "\n".join(l for l in mondai.splitlines()[:5] if l.startswith(">") and "書き起こし" not in l)
    qs, ks = split(mondai), split(kaisetsu)

    out = [
        "安全衛生技術試験協会が公表している第二種衛生管理者試験の問題を、1問ずつ"
        "「どこが誤りか」「正しくは何か」まで、すべての選択肢について解説します。",
        "",
        source,
        "",
        f"問1〜問{free}は無料で読めます。続きの問{free + 1}〜問{len(qs)}は有料です。",
        "",
    ]
    for q in sorted(qs):
        title, _, body = ks[q].partition("\n")
        out += [f"## 問{q}　{title.split('―')[0].strip()}", "", for_note(qs[q]), "",
                "### 解答と解説", "",
                f"**解答：{title.split('解答')[-1].strip()}**", "", body.strip(), ""]
        if q == free:
            out += ["---", "", PAY_MARK, "", "---", ""]
    out += ["---", "",
            "※ 解説は作成者の見解です。正答は協会の公表問題（○印）と照合済みです。"
            "法令は令和7年12月31日時点の内容で、その後の改正は反映していません。", ""]
    md = "\n".join(out)
    (d / "note_draft.md").write_text(md, encoding="utf-8")

    page = (
        "<!doctype html><html lang=\"ja\"><head><meta charset=\"utf-8\">"
        "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">"
        "<title>note 貼り付け用</title><style>body{max-width:720px;margin:24px auto;padding:0 16px;"
        "font-family:sans-serif;line-height:1.8}</style></head><body>\n"
        "<p style=\"background:#fffbe6;padding:8px\">この下を全選択（Ctrl+A / ⌘A）→ コピー → note の本文に貼り付け。"
        "タイトルは別欄に入力。この黄色い案内文は貼り付け後に消す。</p>\n"
        + to_html(md) + "\n</body></html>\n"
    )
    (d / "note_draft.html").write_text(page, encoding="utf-8")
    print(f"wrote note_draft.md / note_draft.html ({len(qs)} questions, free={free})")


if __name__ == "__main__":
    main()
