#!/usr/bin/env python3
import sys
from pathlib import Path

src = Path(sys.argv[1])
name = sys.argv[2]

if len(name.encode("ascii")) > 16:
    raise SystemExit("C64 filename must be at most 16 ASCII bytes")

payload = src.read_bytes()
if len(payload) < 2:
    raise SystemExit("Input must be a PRG containing its two-byte load address")

header = bytearray(26)
header[0:8] = b"C64File\0"
header[8:24] = name.encode("ascii").ljust(16, b"\0")
header[24:26] = b"\0\0"

out = src.with_suffix(".P00")
out.write_bytes(header + payload)

print(f"Created {out}")