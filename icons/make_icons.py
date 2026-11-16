#!/usr/bin/env python3
"""Writes the neutral server icon (icons/server.png): three stacked server units with status lights, drawn for this
repository, no third-party material. Dedicated to the public domain (CC0-1.0). Pure standard library, deterministic.
Used by every `kind = "server"` entry until a maker gives a licence for its own logo (ADR 0077 section 4).
Run: python3 -I icons/make_icons.py"""
import os
import struct
import zlib

HERE = os.path.dirname(os.path.abspath(__file__))
SIZE = 128
BG = (255, 255, 255)
BODY = (52, 64, 84)
EDGE = (30, 38, 52)
SLOT = (96, 110, 132)
LIGHT = (90, 200, 120)


def inside_round(x, y, x0, y0, x1, y1, r):
    if not (x0 <= x < x1 and y0 <= y < y1):
        return False
    cx = min(max(x, x0 + r), x1 - 1 - r)
    cy = min(max(y, y0 + r), y1 - 1 - r)
    return (x - cx) ** 2 + (y - cy) ** 2 <= r * r


def pixel(x, y):
    for i in range(3):
        y0 = 14 + i * 38
        y1 = y0 + 30
        if inside_round(x, y, 10, y0, 118, y1, 6):
            if not inside_round(x, y, 12, y0 + 2, 116, y1 - 2, 4):
                return EDGE
            if (x - 28) ** 2 + (y - (y0 + 15)) ** 2 <= 16:
                return LIGHT
            if 48 <= x < 104 and y0 + 11 <= y < y0 + 14 or 48 <= x < 104 and y0 + 17 <= y < y0 + 20:
                return SLOT
            return BODY
    return BG


def write(path):
    raw = b"".join(b"\x00" + b"".join(bytes(pixel(x, y)) for x in range(SIZE)) for y in range(SIZE))

    def chunk(tag, data):
        body = tag + data
        return struct.pack(">I", len(data)) + body + struct.pack(">I", zlib.crc32(body))

    data = b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", SIZE, SIZE, 8, 2, 0, 0, 0)) + chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b"")
    with open(path, "wb") as f:
        f.write(data)


if __name__ == "__main__":
    write(os.path.join(HERE, "server.png"))
