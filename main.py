#!/usr/bin/env python3
"""news-image-20261117 entry: copy the held front-page image to /output/entry.png.

The image (entry.png, beside this file) sums up the world news of Tuesday
17 November 2026: Ukraine's overnight strike critically damaging the Kerch
Bridge, Iran's drones targeting a U.S. radar base in Bahrain, the
Trump-Xi-Putin three-way summit set for Shenzhen, and five EU states planning
migrant return hubs in Rwanda. Deterministic: a byte copy, so two runs write
identical bytes.
"""
import os
import shutil
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
MAX_BYTES = 1048576
MAX_SIDE = 1024


def validate(path):
    """Refuse a missing, truncated or out-of-limits image instead of copying
    a bad file: the gate rejects those, so fail loudly here. For PNG, walk
    every chunk to IEND and check each CRC; for JPEG, require the EOI marker."""
    if not os.path.isfile(path):
        raise SystemExit(f"entry image missing: {path}")
    size = os.path.getsize(path)
    if size > MAX_BYTES:
        raise SystemExit(f"entry image {size} bytes exceeds {MAX_BYTES}")
    with open(path, "rb") as f:
        data = f.read()
    if data[:8] == b"\x89PNG\r\n\x1a\n":
        import binascii
        pos, w, h, seen_iend = 8, None, None, False
        while pos + 8 <= len(data):
            ln = struct.unpack(">I", data[pos:pos + 4])[0]
            typ = data[pos + 4:pos + 8]
            end = pos + 8 + ln + 4
            if end > len(data):
                raise SystemExit("entry image is a truncated PNG")
            crc = struct.unpack(">I", data[end - 4:end])[0]
            if binascii.crc32(data[pos + 4:end - 4]) & 0xFFFFFFFF != crc:
                raise SystemExit(f"entry image PNG chunk {typ!r} has a bad CRC")
            if typ == b"IHDR":
                w, h = struct.unpack(">II", data[pos + 8:pos + 16])
            if typ == b"IEND":
                seen_iend = True
                break
            pos = end
        if not seen_iend:
            raise SystemExit("entry image PNG has no IEND chunk")
        if w > MAX_SIDE or h > MAX_SIDE:
            raise SystemExit(f"entry image {w}x{h} exceeds {MAX_SIDE}x{MAX_SIDE}")
        return "PNG"
    if data[:2] == b"\xff\xd8":
        if not data.rstrip(b"\x00").endswith(b"\xff\xd9"):
            raise SystemExit("entry image JPEG has no EOI marker")
        return "JPEG"
    raise SystemExit("entry image is neither PNG nor JPEG (magic bytes)")


def main():
    src = os.path.join(HERE, "entry.png")
    kind = validate(src)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dest)
    # Verify the copy byte for byte: a truncated write must fail loudly
    # here rather than hand the judge a corrupt image.
    import hashlib
    with open(src, "rb") as f:
        src_hash = hashlib.sha256(f.read()).hexdigest()
    with open(dest, "rb") as f:
        dest_hash = hashlib.sha256(f.read()).hexdigest()
    if src_hash != dest_hash:
        raise SystemExit("entry image copy does not match source")
    print(f"wrote entry.png ({kind}, {os.path.getsize(src)} bytes)")


if __name__ == "__main__":
    main()
