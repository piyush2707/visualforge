#!/usr/bin/env python3
"""Basic, dependency-free checks for image asset paths and file signatures."""
import argparse
import struct
from pathlib import Path

SIGNATURES = {
    ".png": (b"\x89PNG\r\n\x1a\n", "PNG"),
    ".jpg": (b"\xff\xd8\xff", "JPEG"),
    ".jpeg": (b"\xff\xd8\xff", "JPEG"),
    ".gif": (b"GIF87a", "GIF87a"),
    ".webp": (b"RIFF", "RIFF/WEBP"),
}

def inspect(path: Path) -> bool:
    if not path.exists():
        print(f"MISSING  {path}")
        return False
    if not path.is_file():
        print(f"NOTFILE  {path}")
        return False
    suffix = path.suffix.lower()
    if suffix == ".svg":
        data = path.read_text(encoding="utf-8", errors="replace")[:4096].lower()
        ok = "<svg" in data
        print(f"{'OK' if ok else 'CHECK'}      {path} ({path.stat().st_size} bytes; SVG signature {'found' if ok else 'not found'})")
        return ok
    signature = SIGNATURES.get(suffix)
    if not signature:
        print(f"CHECK    {path} (unknown extension; existence verified, format not checked)")
        return True
    with path.open("rb") as f:
        head = f.read(24)
    ok = head.startswith(signature[0])
    extra = ""
    if ok and suffix == ".png" and len(head) >= 24:
        width, height = struct.unpack(">II", head[16:24]) if len(head) >= 24 else (0, 0)
        extra = f", {width}x{height}"
    if ok and suffix == ".webp":
        ok = head[8:12] == b"WEBP"
    print(f"{'OK' if ok else 'FAIL'}      {path} ({path.stat().st_size} bytes{extra})")
    return ok

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", help="Files or directories to inspect")
    args = parser.parse_args()
    files = []
    for item in args.paths:
        p = Path(item)
        if p.is_dir():
            files.extend(x for x in p.rglob("*") if x.is_file())
        else:
            files.append(p)
    if not files:
        print("No files found.")
        raise SystemExit(1)
    results = [inspect(p) for p in files]
    print(f"\nChecked {len(results)} file(s): {sum(results)} passed, {len(results) - sum(results)} failed.")
    raise SystemExit(0 if all(results) else 1)

if __name__ == "__main__":
    main()
