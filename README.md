# DS

- `index.html` … 統計検定DSエキスパート対策（GitHub Pages 用の単一HTML）
- `sc/` … 情報処理安全確保支援士 午後 過去問解説サイト（令和3年度春期〜令和7年度秋期の5年分。令和5年度春期までは午後I・午後IIを別の回として掲載）
  - `sc/index.html` … サイト本体。`sc/manifest.json` と各回の Markdown を読み込んで表示する
  - `sc/<回ID>/mondai_q1〜q4.md` … 問題文の書き起こし（IPA公開の画像PDFから）
  - `sc/<回ID>/fig/` … 問題文の図（IPA公開の問題冊子PDFから切り出した画像。`scripts/crop_sc_figures.py` で生成）
  - `sc/<回ID>/kaitou_kaisetsu.md` … 解答と解説（公式解答例と照合し，ずれていた箇所は公式に沿って修正済み）
  - `sc/<回ID>/shougou.md` … IPA公式解答例との照合結果（旧形式の回は公式解答例・出題趣旨・採点講評）
  - 回ID は IPA のファイル名に合わせた `2024r06h`（h＝春期、a＝秋期）形式。旧形式は `2023r05h-pm1`（午後I）／`2023r05h-pm2`（午後II）
- `sc/mock/` … 午後 模試（CBT想定：画面で問題を読み，キーボードで記述。時間計測・問題選択・字数カウント・見直し印・公式解答例との自己採点）
- `sc/am2/` … 情報処理安全確保支援士 午前II 道場（模擬試験・一問一答）
  - `sc/am2/index.html` … 本体。`sc/am2/bank.json` を読み込む。過去問と新規問題の割合・問題数・制限時間を選んで模試にできる
  - `sc/am2/data/<回ID>.json` … 過去問の書き起こし（問題文・選択肢・分野・解説）
  - `sc/am2/data/original.json` … オリジナル新規問題（正解 `a` は 0=ア〜3=エ）
- `pdf/` … IPA公開の問題・解答例PDF（`.github/workflows/fetch-sc-pdf.yml` で取得）
  - `pdf/am2/` … 午前IIの問題・解答例PDF（`.github/workflows/fetch-sc-am2-pdf.yml` で取得）
- `scripts/build_sc_manifest.py` … `sc/` 配下を走査して `sc/manifest.json` を再生成する
- `scripts/build_sc_am2.py` … `sc/am2/data/` と午前II解答例PDFの正解から `sc/am2/bank.json` を再生成する（要 `pdftotext`）

ローカル確認：`python3 -m http.server` をリポジトリ直下で起動し、`http://localhost:8000/sc/` を開く。
