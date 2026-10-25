#!/usr/bin/env python3
import sys
from pathlib import Path

src = Path(sys.argv[1])
name = sys.argv[2]

if len(name.encode("ascii")) > 16:
    raise SystemExit("C64 filename must be at most 16 ASCII bytes")

# PC64/CBM wrapper header: 26 bytes
header = bytearray(26)
header[0:8] = b"C64File\0"
header[8:24] = name.encode("ascii").ljust(16, b"\0")
header[24:26] = b"\0\0"

out = src.with_suffix(".S00")
out.write_bytes(header + src.read_bytes())

print(f"Created {out}")
