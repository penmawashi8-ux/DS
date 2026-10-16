#!/usr/bin/env python3
"""安全衛生技術試験協会のサイトを巡回し、衛生管理者の公表問題PDFを eisei/pdf/ に保存する。

GitHub Actions 上で実行する（開発環境からは exam.or.jp に到達できないため）。
巡回したページ・見つけたPDFの一覧は eisei/pdf/_crawl.txt に残す。
"""
import re
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = "https://www.exam.or.jp/"
OUT = Path(__file__).resolve().parent.parent / "eisei" / "pdf"
UA = {"User-Agent": "Mozilla/5.0"}
LATEST = "令和8年10月"
LINK_RE = re.compile(r'<a\s[^>]*href="([^"]+)"[^>]*>(.*?)</a>', re.I | re.S)
TAG_RE = re.compile(r"<[^>]+>")


def get(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()


def decode(raw):
    for enc in ("utf-8", "cp932", "euc-jp"):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            pass
    return raw.decode("utf-8", "replace")


def links(url, html):
    for href, text in LINK_RE.findall(html):
        yield urllib.parse.urljoin(url, href), TAG_RE.sub("", text).strip()


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    log = []
    seen, queue, pdfs = set(), [ROOT], {}
    while queue and len(seen) < 60:
        url = queue.pop(0)
        if url in seen:
            continue
        seen.add(url)
        try:
            html = decode(get(url))
        except Exception as e:  # noqa: BLE001
            log.append(f"ERR {url} {e}")
            continue
        log.append(f"PAGE {url}")
        if "lckohyo" in url:
            (OUT / "_lckohyo.html").write_text(html, encoding="utf-8")
        for u, text in links(url, html):
            if "exam.or.jp" not in u:
                continue
            if u.lower().endswith(".pdf"):
                # 免許試験の公表問題（LC*.pdf）のうち最新掲載分を取る。
                # リンク文字列は掲載日だけなので、試験種別は後で中身から判別する
                if re.search(r"/LC\d+[-\d]*\.pdf$", u) and LATEST in text:
                    pdfs[u] = text
                log.append(f"  PDF {u} [{text}]")
            elif ("kohyo" in u.lower() or "公表" in text) and u not in seen:
                queue.append(u)
        if url == ROOT:
            # トップから公表問題ページへの導線が見つからない場合に備える
            queue += [urllib.parse.urljoin(ROOT, p) for p in ("exmin/kohyo.html", "exmin/H_kohyo.html")]
        time.sleep(1)

    for u, text in sorted(pdfs.items()):
        name = Path(urllib.parse.urlparse(u).path).name
        dst = OUT / name
        if dst.exists():
            continue
        try:
            dst.write_bytes(get(u))
            log.append(f"SAVED {name} [{text}]")
        except Exception as e:  # noqa: BLE001
            log.append(f"ERR {u} {e}")
        time.sleep(1)

    (OUT / "_crawl.txt").write_text("\n".join(log) + "\n", encoding="utf-8")
    print("\n".join(log))


if __name__ == "__main__":
    main()
