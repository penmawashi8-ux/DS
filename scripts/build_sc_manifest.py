#!/usr/bin/env python3
"""sc/<exam-id>/ 配下の Markdown を走査して sc/manifest.json を生成する。

exam-id は IPA のファイル名に合わせた "2024r06h"（h=春期, a=秋期）形式。
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "sc"
SEASON = {"h": "春期", "a": "秋期"}
JUDGE_RE = re.compile(r"\|\s*\**\s*(◎|○|△|×)\s*\**\s*\|\s*$")


def exam_label(exam_id):
    m = re.fullmatch(r"(\d{4})r(\d{2})([ha])", exam_id)
    if not m:
        return exam_id
    year, reiwa, season = m.groups()
    return f"令和{int(reiwa)}年度 {SEASON[season]}（{year}）"


def theme_of(md):
    m = re.search(r"問\s*\d\s*[ 　]+(.+?)に関する次の記述", md)
    return m.group(1).strip() if m else ""


def lead_of(md):
    """本文最初の段落の1文目（題材の会社・状況）。"""
    for line in md.splitlines():
        s = line.strip()
        if not s or s.startswith(("#", ">", "**", "|", "`", "-", "<")):
            continue
        return re.split(r"(?<=。)", s)[0]
    return ""


def split_by_question(md):
    """'## 問N' 見出しごとに分割して {N: 本文} を返す。"""
    parts = {}
    cur = None
    for line in md.splitlines(keepends=True):
        m = re.match(r"^##\s*問\s*(\d)", line)
        if m:
            cur = int(m.group(1))
            parts[cur] = ""
        if cur is not None:
            parts[cur] += line
    return parts


def judge_counts(section):
    counts = {"◎": 0, "○": 0, "△": 0, "×": 0}
    for line in section.splitlines():
        m = JUDGE_RE.search(line)
        if m:
            counts[m.group(1)] += 1
    return counts


def main():
    exams = []
    for d in sorted((p for p in ROOT.iterdir() if p.is_dir()), reverse=True):
        qfiles = sorted(d.glob("mondai_q*.md"))
        if not qfiles:
            continue
        shougou = (d / "shougou.md").read_text(encoding="utf-8") if (d / "shougou.md").exists() else ""
        judged = split_by_question(shougou)
        questions = []
        for f in qfiles:
            n = int(re.search(r"q(\d)", f.name).group(1))
            md = f.read_text(encoding="utf-8")
            questions.append({
                "no": n,
                "theme": theme_of(md),
                "lead": lead_of(md),
                "judge": judge_counts(judged.get(n, "")),
            })
        exams.append({
            "id": d.name,
            "label": exam_label(d.name),
            "hasAnswer": (d / "kaitou_kaisetsu.md").exists(),
            "hasCompare": bool(shougou),
            "questions": questions,
        })
    out = ROOT / "manifest.json"
    out.write_text(json.dumps({"exams": exams}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"wrote {out} ({len(exams)} exams)")


if __name__ == "__main__":
    main()
