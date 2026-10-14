# VIDEO_WORDS：語音轉繁體字幕 + 燒錄流程

5 分鐘影片實測通過：whisper 轉寫 → 依規則校正 → SRT → ffmpeg 硬字幕。

## 環境
- Windows + ffmpeg 9（含 libass）+ Python 3.12+
- `pip install -r requirements.txt`（已鎖 `av==12.0.0`，勿升級，否則轉寫報錯）
- 中文字型：微軟正黑體（`C:\Windows\Fonts\msjh.ttc`）
- 確認：`ffmpeg -h filter=subtitles` 有輸出

## 流程
1. 抽音：`ffmpeg -y -i input.mp4 -ar 16000 -ac 1 -c:a pcm_s16le audio.wav`
2. 轉寫：`python scripts/transcribe.py --input audio.wav --json segments.json --srt raw.srt --language zh`
3. 校正：按 `SUBTITLE_RULES.md` 改為繁體、去標點、每行不超過 18 個中文字、單行、段數與初稿相同
4. 檢查：`python scripts/check_srt.py --srt final.srt`（必要時加 `--json segments.json` 對段數）
5. 燒錄：`powershell -File scripts/burn.ps1 -InputVideo input.mp4 -Srt final.srt -OutputVideo output_上字幕.mp4`

## 坑
- 中文路徑先複製到英文暫存再餵 `subtitles` 濾鏡（`burn.ps1` 已處理，勿用相對路徑）
- whisper 常出簡體，需轉繁體並修專有名詞
- 末段長靜音易幻覺，要捨去
- 校正禁併段拆段，否則全片時間漂移（見 `SUBTITLE_RULES.md` 第 0 節）
- 字幕只限單行，勿用 `\n` 雙行

## 結構
- `scripts/`：可重用腳本
- `example/example.srt`：格式範例
- 大檔 mp4 wav json 不上傳，見 `.gitignore`
