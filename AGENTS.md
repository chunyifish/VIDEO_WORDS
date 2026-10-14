# AGENTS

給其他 agent 的使用說明。

## 先讀
- `README.md`：完整流程
- `SUBTITLE_RULES.md`：校正時必須遵守
- `example/example.srt`：輸出格式範例

## 工作順序
1. 讀 `README.md` 確認環境
2. 用 `scripts/transcribe.py` 產初稿，不改腳本寫死路徑
3. 按 `SUBTITLE_RULES.md` 校正，不編造原意；段數與初稿相同、單行、時間原樣照抄
4. 用 `scripts/check_srt.py` 驗證，max_cjk 不超過 18 且無標點（必要時加 `--json` 對段數）
5. 需燒錄才用 `scripts/burn.ps1`

## 不做
- 不上傳 mp4 wav json 與私人路徑
- 不提交含個資的完整 SRT，只留 example
- 不改需求的字幕規則
