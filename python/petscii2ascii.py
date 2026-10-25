#!/usr/bin/env python3
"""
PETSCII to ASCII Converter for C64OS Bundle Files

Converts binary PETSCII files back to ASCII text format.
Assumes the C64 shifted charset (lowercase/uppercase mode).

Inverse mappings from the corrected ascii2petscii.py:
  - PETSCII 0x41-0x5A -> lowercase a-z  (ASCII 0x61-0x7A)
  - PETSCII 0xC1-0xDA -> uppercase A-Z  (ASCII 0x41-0x5A)
  - PETSCII 0x20-0x40 -> direct (digits, punctuation)
  - PETSCII 0x0D      -> newline (LF)
  - PETSCII 0x5B      -> [
  - PETSCII 0xBF      -> backslash
  - PETSCII 0x5D      -> ]
  - PETSCII 0xDE      -> ^
  - PETSCII 0xA4      -> _
  Note: backtick, {, |, }, ~ had no true PETSCII equivalents and were
  replaced with approximations on encode, so they cannot be recovered.
"""

import sys
from pathlib import Path


def petscii_to_ascii(data: bytes) -> str:
    """
    Convert PETSCII bytes to ASCII string (shifted/lowercase charset).
    """
    result = []

    for byte in data:

        # CR -> newline
        if byte == 0x0D:
            result.append('\n')

        # PETSCII 0x41-0x5A -> lowercase a-z
        elif 0x41 <= byte <= 0x5A:
            result.append(chr(0x61 + (byte - 0x41)))

        # PETSCII 0xC1-0xDA -> uppercase A-Z
        elif 0xC1 <= byte <= 0xDA:
            result.append(chr(0x41 + (byte - 0xC1)))

        # Space, digits, punctuation 0x20-0x40: direct mapping
        elif 0x20 <= byte <= 0x40:
            result.append(chr(byte))

        # Special cases
        elif byte == 0x5B:   # [
            result.append('[')
        elif byte == 0xBF:   # backslash (was remapped from 0x5C)
            result.append('\\')
        elif byte == 0x5D:   # ]
            result.append(']')
        elif byte == 0xDE:   # ^ (was remapped from 0x5E)
            result.append('^')
        elif byte == 0xA4:   # _ (was remapped from 0x5F)
            result.append('_')
        elif byte == 0x7F:   # DEL
            result.append('\x7F')

        # Everything else: not representable in ASCII, replace with ?
        else:
            result.append('?')

    return ''.join(result)


def convert_file(input_path: Path, output_path: Path):
    """Convert a PETSCII binary file to an ASCII text file."""
    try:
        with open(input_path, 'rb') as f:
            data = f.read()

        text = petscii_to_ascii(data)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(text)

        print(f"✓ Converted: {input_path.name} -> {output_path.name}")
        return True

    except Exception as e:
        print(f"✗ Error converting {input_path}: {e}")
        return False


def main():
    """Main entry point"""
    if len(sys.argv) < 2 or sys.argv[1] == '--help':
        print(__doc__)
        print("\nUsage: petscii2ascii.py <input_file> [output_file]")
        print("\nExamples:")
        print("  petscii2ascii.py about.t about.txt")
        print("  petscii2ascii.py menu.m menu.txt")
        sys.exit(0 if '--help' in sys.argv else 1)

    input_path = Path(sys.argv[1])

    if not input_path.exists():
        print(f"Error: Input file not found: {input_path}")
        sys.exit(1)

    if len(sys.argv) >= 3:
        output_path = Path(sys.argv[2])
    else:
        output_path = input_path.with_suffix('.txt')

    if convert_file(input_path, output_path):
        print(f"\nASCII file created: {output_path}")
        print(f"Size: {output_path.stat().st_size} bytes")
    else:
        sys.exit(1)


if __name__ == '__main__':
    main()
