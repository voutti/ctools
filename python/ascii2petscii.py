#!/usr/bin/env python3
"""
ASCII to PETSCII Converter for C64OS Bundle Files

Converts text files from ASCII to PETSCII format for C64OS.
Targets the C64 shifted charset (lowercase/uppercase mode), which supports
both upper and lowercase letters — the natural choice for text files.

Key PETSCII facts (shifted/lowercase charset):
  - Lowercase a-z  (ASCII 0x61-0x7A) -> PETSCII 0x41-0x5A
  - Uppercase A-Z  (ASCII 0x41-0x5A) -> PETSCII 0xC1-0xDA
  - Digits & most punctuation (0x20-0x3F) -> same as ASCII
  - Newline: CR only (0x0D), no LF
  - 0x5C backslash -> 0xA9 (£ sign lives at 0x5C in PETSCII, avoid it)
  - 0x5E caret     -> 0xDE (up-arrow is at 0x5E in PETSCII)
  - 0x5F underscor -> 0xA4 (left-arrow is at 0x5F in PETSCII)
  - 0x60-0x7F: no direct PETSCII equivalents; mapped as best-effort below
"""

import sys
from pathlib import Path


def ascii_to_petscii(text: str) -> bytes:
    """
    Convert ASCII string to PETSCII bytes (shifted/lowercase charset).
    """
    result = bytearray()

    for char in text:
        code = ord(char)

        # Newline: LF -> CR (0x0D); skip bare CR
        if char == '\n':
            result.append(0x0D)
        elif char == '\r':
            continue

        # Lowercase a-z: ASCII 0x61-0x7A -> PETSCII 0x41-0x5A
        elif 0x61 <= code <= 0x7A:
            result.append(0x41 + (code - 0x61))

        # Uppercase A-Z: ASCII 0x41-0x5A -> PETSCII 0xC1-0xDA
        elif 0x41 <= code <= 0x5A:
            result.append(0xC1 + (code - 0x41))

        # Space and punctuation/digits 0x20-0x40: direct mapping
        elif 0x20 <= code <= 0x40:
            result.append(code)

        # Special cases in 0x41-0x5F that aren't letters:
        # Already handled A-Z above; now deal with 0x5B-0x5F
        elif code == 0x5B:  # [ -> PETSCII [ (0x5B, same)
            result.append(0x5B)
        elif code == 0x5C:  # \ -> use 0xBF (closest available; £ is at 0x5C)
            result.append(0xBF)
        elif code == 0x5D:  # ] -> PETSCII ] (0x5D, same)
            result.append(0x5D)
        elif code == 0x5E:  # ^ -> 0xDE (avoids PETSCII up-arrow at 0x5E)
            result.append(0xDE)
        elif code == 0x5F:  # _ -> 0xA4 (avoids PETSCII left-arrow at 0x5F)
            result.append(0xA4)

        # 0x60-0x7F: no clean PETSCII equivalents
        elif code == 0x60:  # backtick -> replace with single quote
            result.append(0x27)
        elif code == 0x7B:  # { -> no equivalent, use (
            result.append(0x28)
        elif code == 0x7C:  # | -> no equivalent, use !
            result.append(0x21)
        elif code == 0x7D:  # } -> no equivalent, use )
            result.append(0x29)
        elif code == 0x7E:  # ~ -> no equivalent, use -
            result.append(0x2D)
        elif code == 0x7F:  # DEL -> pass through
            result.append(0x7F)

        # Pass through anything else (control codes etc.)
        else:
            result.append(code & 0xFF)

    return bytes(result)


def convert_file(input_path: Path, output_path: Path):
    """Convert a text file from ASCII to PETSCII."""
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            text = f.read()

        petscii = ascii_to_petscii(text)

        with open(output_path, 'wb') as f:
            f.write(petscii)

        print(f"✓ Converted: {input_path.name} -> {output_path.name}")
        return True

    except Exception as e:
        print(f"✗ Error converting {input_path}: {e}")
        return False


def main():
    """Main entry point"""
    if len(sys.argv) < 2 or sys.argv[1] == '--help':
        print(__doc__)
        print("\nUsage: ascii2petscii.py <input_file> [output_file]")
        print("\nExamples:")
        print("  ascii2petscii.py about.txt about.t")
        print("  ascii2petscii.py menu.txt menu.m")
        sys.exit(0 if '--help' in sys.argv else 1)

    input_path = Path(sys.argv[1])

    if not input_path.exists():
        print(f"Error: Input file not found: {input_path}")
        sys.exit(1)

    if len(sys.argv) >= 3:
        output_path = Path(sys.argv[2])
    else:
        output_path = input_path.with_suffix('.petscii')

    if convert_file(input_path, output_path):
        print(f"\nPETSCII file created: {output_path}")
        print(f"Size: {output_path.stat().st_size} bytes")
    else:
        sys.exit(1)


if __name__ == '__main__':
    main()
