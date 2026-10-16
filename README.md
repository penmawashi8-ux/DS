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
- `eisei/` … 衛生管理者など 安全衛生技術試験協会の公表試験問題の解説（note 販売の試作）
  - `eisei/pdf/` … 協会公開の公表問題PDF（`.github/workflows/fetch-eisei-pdf.yml` で取得。開発環境からは exam.or.jp に届かないため）
  - `eisei/<回ID>/mondai.md` … 問題文の書き起こし（PDFの文字データが崩れているため画像から）
  - `eisei/<回ID>/kaitou_kaisetsu.md` … 公式正答を見る前に作成した解答と、選択肢ごとの解説
  - `eisei/<回ID>/seitou.json` / `shougou.md` … 公式正答（PDF内の○）と、自作解答との照合結果
  - `eisei/<回ID>/note_draft.md` … note に貼る下書き（無料部分＋有料部分）
  - `eisei/<回ID>/header.png` … note の見出し画像（1280×670、`scripts/eisei_header.py` で生成）
  - `eisei/pdf/` の取得対象回は `scripts/fetch_eisei.py` の `ISSUES` で指定
  - 手順：`scripts/eisei_prepare.py`（正答抽出＋○を白塗りした画像作成）→ 画像を見て解答・解説作成 → `scripts/eisei_shougou.py`（照合）→ `scripts/eisei_note.py`（下書き生成）→ `scripts/eisei_header.py`（見出し画像）
