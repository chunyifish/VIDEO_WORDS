"""檢查 SRT 是否符合字幕規則：單行、每行不超過 18 個中文字、內容無標點
用法：python scripts/check_srt.py --srt example/example.srt
      python scripts/check_srt.py --srt final.srt --json segments.json
"""
import argparse
import json
import re
from pathlib import Path

PUNCT = set("，。？！、；：『』「」（）《》〈〉…—～·,.?!;:")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--srt", required=True)
    ap.add_argument("--json", default=None, help="轉寫 JSON，對段數用")
    args = ap.parse_args()
    text = Path(args.srt).read_text(encoding="utf-8")
    bad = []
    maxlen = 0
    events = 0
    blocks = re.split(r"\n\s*\n", text.strip())
    for b in blocks:
        lines = b.splitlines()
        if len(lines) < 3:
            bad.append(("結構", b[:60]))
            continue
        events += 1
        addrs = lines[2:]
        if len(addrs) != 1:
            bad.append((f"事件{events}", f"非單行({len(addrs)}行)", " | ".join(addrs)[:60]))
        for s in addrs:
            s = s.strip()
            cjk = len(re.findall(r"[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff]", s))
            maxlen = max(maxlen, cjk)
            if cjk > 18:
                bad.append((f"事件{events}", f"cjk={cjk}", s))
            if any(ch in PUNCT for ch in s):
                bad.append((f"事件{events}", "punct", s))
    if args.json:
        segs = json.loads(Path(args.json).read_text(encoding="utf-8"))
        n = len(segs) if isinstance(segs, list) else len(segs.get("segments", segs))
        if n != events:
            bad.append(("段數", f"srt={events} json={n}", "時間會錯位，先對齊"))
    print(f"events={events} max_cjk={maxlen} issues={len(bad)}")
    for b in bad[:30]:
        print(b)
    raise SystemExit(1 if bad else 0)


if __name__ == "__main__":
    main()
