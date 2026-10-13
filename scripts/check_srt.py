"""檢查 SRT 是否符合字幕規則：每行不超過 18 個中文字、內容無標點
用法：python scripts/check_srt.py --srt example/example.srt
"""
import argparse
import re
from pathlib import Path

PUNCT = set("，。？！、；：『』「」（）《》〈〉,.?!;:")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--srt", required=True)
    args = ap.parse_args()
    text = Path(args.srt).read_text(encoding="utf-8")
    bad = []
    maxlen = 0
    for i, line in enumerate(text.splitlines(), 1):
        s = line.strip()
        if re.match(r"^\d+$", s) or "-->" in s or not s:
            continue
        cjk = len(re.findall(r"[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff]", s))
        maxlen = max(maxlen, cjk)
        if cjk > 18:
            bad.append((i, f"cjk={cjk}", s))
        if any(ch in PUNCT for ch in s):
            bad.append((i, "punct", s))
    print(f"max_cjk={maxlen} issues={len(bad)}")
    for b in bad[:30]:
        print(b)
    raise SystemExit(1 if bad else 0)


if __name__ == "__main__":
    main()
