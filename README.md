# DS

- `index.html` … 統計検定DSエキスパート対策（GitHub Pages 用の単一HTML）
- `sc/` … 情報処理安全確保支援士 午後 過去問解説サイト（新形式：令和5年度秋期〜）
  - `sc/index.html` … サイト本体。`sc/manifest.json` と各回の Markdown を読み込んで表示する
  - `sc/<回ID>/mondai_q1〜q4.md` … 問題文の書き起こし（IPA公開の画像PDFから）
  - `sc/<回ID>/kaitou_kaisetsu.md` … 公式解答を見る前に作成した解答と解説
  - `sc/<回ID>/shougou.md` … IPA公式解答例との照合結果
  - 回ID は IPA のファイル名に合わせた `2024r06h`（h＝春期、a＝秋期）形式
- `pdf/` … IPA公開の問題・解答例PDF（`.github/workflows/fetch-sc-pdf.yml` で取得）
- `scripts/build_sc_manifest.py` … `sc/` 配下を走査して `sc/manifest.json` を再生成する

ローカル確認：`python3 -m http.server` をリポジトリ直下で起動し、`http://localhost:8000/sc/` を開く。
