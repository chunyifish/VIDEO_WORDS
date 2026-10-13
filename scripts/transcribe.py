"""通用語音轉文字：faster-whisper + SRT 輸出
用法：
  python scripts/transcribe.py --input audio.wav --json out.json --srt out.srt
  python scripts/transcribe.py --input video.mp4 --language zh --model large-v3-turbo
"""
import argparse
import json


def fmt(t: float) -> str:
    if t < 0:
        t = 0
    h = int(t // 3600)
    m = int((t % 3600) // 60)
    s = int(t % 60)
    ms = int(round((t - int(t)) * 1000))
    if ms == 1000:
        s += 1
        ms = 0
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, help="wav/mp4 音檔或影片路徑")
    ap.add_argument("--json", default="segments.json", help="輸出 JSON 路徑")
    ap.add_argument("--srt", default="raw.srt", help="輸出初稿 SRT 路徑")
    ap.add_argument("--language", default="zh", help="主要語言，預設 zh")
    ap.add_argument("--model", default="large-v3-turbo", help="whisper 模型")
    ap.add_argument("--device", default="cpu", help="cpu 或 cuda")
    args = ap.parse_args()

    from faster_whisper import WhisperModel

    fallbacks = [args.model, "large-v3-turbo", "large-v3", "medium", "small", "base"]
    seen = []
    model = None
    for name in fallbacks:
        if name in seen:
            continue
        seen.append(name)
        try:
            print(f"TRY MODEL: {name}", flush=True)
            model = WhisperModel(name, device=args.device, compute_type="int8")
            break
        except Exception as e:  # noqa: BLE001
            print(f"FAIL {name}: {e}", flush=True)
    if model is None:
        raise SystemExit("no whisper model available")

    segments, info = model.transcribe(
        args.input, language=args.language, beam_size=5, vad_filter=True
    )
    print(f"Detected: {info.language} prob={info.language_probability}", flush=True)

    segs = []
    for i, seg in enumerate(segments, 1):
        segs.append({"id": i, "start": seg.start, "end": seg.end, "text": seg.text.strip()})

    with open(args.json, "w", encoding="utf-8") as f:
        json.dump(segs, f, ensure_ascii=False, indent=2)

    with open(args.srt, "w", encoding="utf-8") as f:
        for s in segs:
            f.write(f"{s['id']}\n{fmt(s['start'])} --> {fmt(s['end'])}\n{s['text']}\n\n")

    print(f"DONE segments={len(segs)} -> {args.srt}", flush=True)


if __name__ == "__main__":
    main()
