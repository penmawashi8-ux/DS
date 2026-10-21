#!/usr/bin/env python3
"""sc/am2/data/*.json と午前II解答例PDFから sc/am2/bank.json を生成する。

- 過去問: sc/am2/data/<exam-id>.json（問題文・選択肢・解説）。正解は
  pdf/am2/<exam-id>_sc_am2_ans.pdf を pdftotext で読んで付ける。
  PDFからテキストが取れない回は JSON の "answers"（例: "ウイエ…" 25文字）を使う。
- 新規問題: sc/am2/data/original.json（各問に "a" = 0〜3 を持つ）。
"""
import json
import re
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DATA = REPO / "sc" / "am2" / "data"
PDF = REPO / "pdf" / "am2"
OUT = REPO / "sc" / "am2" / "bank.json"
KANA = "アイウエ"

# テーマ別の問題集（過去問だけ）。同じ問題が別の回に再出題されている場合は1つだけ載せる
TOPICS = [
    {"id": "calc", "label": "計算問題", "desc": "可用性・スループット・費用・場合の数など，手を動かして解く問題",
     "ids": ["2025r07a-24", "2025r07h-24", "2023r05h-18", "2017h29a-19", "2021r03a-20", "2017h29a-20",
             "2022r04a-24", "2020r02o-24", "2022r04h-04", "2019h31h-24"]},
    {"id": "addr", "label": "アドレス・ネットワーク", "desc": "IPアドレス，サブネット，ブロードキャスト／マルチキャスト，DHCP・ARPなど",
     "ids": ["2023r05a-18", "2021r03a-20", "2017h29a-20", "2023r05h-20", "2020r02o-18", "2023r05a-19",
             "2022r04a-19", "2021r03h-20", "2023r05a-20", "2016h28h-19", "2022r04a-18", "2025r07h-18",
             "2024r06h-18", "2025r07a-07", "2019r01a-19", "2019h31h-12", "2018h30h-18", "2016h28h-15",
             "2016h28a-18"]},
]


def answers_from_pdf(exam_id):
    pdf = PDF / f"{exam_id}_sc_am2_ans.pdf"
    if not pdf.exists():
        return {}
    text = subprocess.run(["pdftotext", "-layout", str(pdf), "-"],
                          stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True).stdout
    return {int(n): a for n, a in re.findall(r"問\s*(\d+)\s+([アイウエ])", text)}


def load_past(path):
    exam = json.loads(path.read_text(encoding="utf-8"))
    eid = exam["id"]
    key = answers_from_pdf(eid)
    if len(key) != 25 and exam.get("answers"):
        key = {i + 1: a for i, a in enumerate(exam["answers"])}
    out = []
    for q in exam["questions"]:
        n = q["no"]
        if n not in key:
            raise SystemExit(f"{eid} 問{n}: 正解が見つからない")
        if len(q["c"]) != 4:
            raise SystemExit(f"{eid} 問{n}: 選択肢が4つでない")
        out.append({
            "id": f"{eid}-{n:02d}", "src": f"{exam['label']} 問{n}", "exam": eid,
            "cat": q["cat"], "q": q["q"], "c": q["c"], "a": KANA.index(key[n]),
            "exp": q.get("exp", ""), "pdf": f"{eid}_sc_am2_qs.pdf",
        })
    return exam["label"], out


def main():
    exams, past = [], []
    # 新しい回から。同じ年度は秋期(a)を春期(h)より後の回として扱う
    newest_first = sorted(DATA.glob("20*.json"), key=lambda p: (p.stem[:7], p.stem[7] == "a"), reverse=True)
    for path in newest_first:
        label, qs = load_past(path)
        exams.append({"id": path.stem, "label": label, "count": len(qs)})
        past += qs
    orig_doc = json.loads((DATA / "original.json").read_text(encoding="utf-8"))
    orig = [{
        "id": f"orig-{q['no']:03d}", "src": f"オリジナル {q['no']}", "exam": "original",
        "cat": q["cat"], "q": q["q"], "c": q["c"], "a": q["a"], "exp": q.get("exp", ""),
    } for q in orig_doc["questions"]]
    known = {q["id"] for q in past}
    for t in TOPICS:
        missing = [i for i in t["ids"] if i not in known]
        if missing:
            raise SystemExit(f"テーマ {t['id']}: 未登録の問題 {missing}")
    bank = {"exams": exams, "past": past, "original": orig, "topics": TOPICS}
    OUT.write_text(json.dumps(bank, ensure_ascii=False, indent=0) + "\n", encoding="utf-8")
    print(f"{OUT.relative_to(REPO)}: 過去問 {len(past)}問（{len(exams)}回）, 新規 {len(orig)}問")


if __name__ == "__main__":
    main()
