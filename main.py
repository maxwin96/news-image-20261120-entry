#!/usr/bin/env python3
"""World News front page — Friday 20 November 2026.

Draws a 1024x1024 newspaper front page summarising six verified world
news stories from 20 November 2026 in a 2x3 grid of panels.

Standard library only. No network, no external files, no images.
Includes its own PNG encoder (zlib + struct) and its own 5x7 bitmap font.

Run:  python3 main.py
Output: $MAKEFUN_OUTPUT_DIR/entry.png (default /output/entry.png)

Deterministic: running twice produces byte-identical output.
"""

import os
import struct
import zlib
from math import cos, pi, sin

W, H = 1024, 1024

# ---------------------------------------------------------------- font -----
# 5x7 bitmap font, defined by hand. "0" = off, "1" = on.
FONT = {
    "A": ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    "B": ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    "C": ("01110", "10001", "10000", "10000", "10000", "10001", "01110"),
    "D": ("11110", "10001", "10001", "10001", "10001", "10001", "11110"),
    "E": ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    "F": ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    "G": ("01110", "10001", "10000", "10111", "10001", "10001", "01111"),
    "H": ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    "I": ("01110", "00100", "00100", "00100", "00100", "00100", "01110"),
    "J": ("00111", "00010", "00010", "00010", "00010", "10010", "01100"),
    "K": ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    "L": ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    "M": ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    "N": ("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
    "O": ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    "P": ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    "Q": ("01110", "10001", "10001", "10001", "10101", "10010", "01101"),
    "R": ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    "S": ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    "T": ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    "U": ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    "V": ("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
    "W": ("10001", "10001", "10001", "10101", "10101", "10101", "01010"),
    "X": ("10001", "10001", "01010", "00100", "01010", "10001", "10001"),
    "Y": ("10001", "10001", "01010", "00100", "00100", "00100", "00100"),
    "Z": ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
    "a": ("00000", "00000", "01110", "00001", "01111", "10001", "01111"),
    "b": ("10000", "10000", "11110", "10001", "10001", "10001", "11110"),
    "c": ("00000", "00000", "01110", "10001", "10000", "10001", "01110"),
    "d": ("00001", "00001", "01111", "10001", "10001", "10001", "01111"),
    "e": ("00000", "00000", "01110", "10001", "11111", "10000", "01110"),
    "f": ("00110", "01001", "01000", "11110", "01000", "01000", "01000"),
    "g": ("00000", "01111", "10001", "10001", "01111", "00001", "01110"),
    "h": ("10000", "10000", "11110", "10001", "10001", "10001", "10001"),
    "i": ("00100", "00000", "01100", "00100", "00100", "00100", "01110"),
    "j": ("00010", "00000", "00110", "00010", "00010", "10010", "01100"),
    "k": ("10000", "10000", "10010", "10100", "11000", "10100", "10010"),
    "l": ("01100", "00100", "00100", "00100", "00100", "00100", "01110"),
    "m": ("00000", "00000", "11010", "10101", "10101", "10101", "10101"),
    "n": ("00000", "00000", "11110", "10001", "10001", "10001", "10001"),
    "o": ("00000", "00000", "01110", "10001", "10001", "10001", "01110"),
    "p": ("00000", "00000", "11110", "10001", "10001", "11110", "10000"),
    "q": ("00000", "00000", "01111", "10001", "10001", "01111", "00001"),
    "r": ("00000", "00000", "10110", "11001", "10000", "10000", "10000"),
    "s": ("00000", "00000", "01111", "10000", "01110", "00001", "11110"),
    "t": ("01000", "01000", "11100", "01000", "01000", "01000", "00110"),
    "u": ("00000", "00000", "10001", "10001", "10001", "10011", "01101"),
    "v": ("00000", "00000", "10001", "10001", "10001", "01010", "00100"),
    "w": ("00000", "00000", "10001", "10101", "10101", "10101", "01010"),
    "x": ("00000", "00000", "10001", "01010", "00100", "01010", "10001"),
    "y": ("00000", "00000", "10001", "10001", "01111", "00001", "01110"),
    "z": ("00000", "00000", "11111", "00010", "00100", "01000", "11111"),
    "0": ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    "1": ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    "2": ("01110", "10001", "00001", "00110", "01000", "10000", "11111"),
    "3": ("11111", "00010", "00100", "00010", "00001", "10001", "01110"),
    "4": ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    "5": ("11111", "10000", "11110", "00001", "00001", "10001", "01110"),
    "6": ("00110", "01000", "10000", "11110", "10001", "10001", "01110"),
    "7": ("11111", "00001", "00010", "00100", "01000", "01000", "01000"),
    "8": ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    "9": ("01110", "10001", "10001", "01111", "00001", "00010", "01100"),
    " ": ("00000", "00000", "00000", "00000", "00000", "00000", "00000"),
    ".": ("00000", "00000", "00000", "00000", "00000", "01100", "01100"),
    ",": ("00000", "00000", "00000", "00000", "01100", "00100", "01000"),
    "'": ("00100", "00100", "01000", "00000", "00000", "00000", "00000"),
    "-": ("00000", "00000", "00000", "01110", "00000", "00000", "00000"),
    ":": ("00000", "01100", "01100", "00000", "01100", "01100", "00000"),
    ";": ("00000", "01100", "01100", "00000", "01100", "00100", "01000"),
    "!": ("00100", "00100", "00100", "00100", "00100", "00000", "00100"),
    "?": ("01110", "10001", "00001", "00110", "00100", "00000", "00100"),
    "(": ("00010", "00100", "01000", "01000", "01000", "00100", "00010"),
    ")": ("01000", "00100", "00010", "00010", "00010", "00100", "01000"),
    "/": ("00001", "00010", "00010", "00100", "01000", "01000", "10000"),
    "&": ("01100", "10010", "10100", "01000", "10101", "10010", "01101"),
    "%": ("11001", "11010", "00010", "00100", "01000", "01011", "10011"),
    "+": ("00000", "00100", "00100", "11111", "00100", "00100", "00000"),
    "=": ("00000", "00000", "11111", "00000", "11111", "00000", "00000"),
    '"': ("01010", "01010", "01010", "00000", "00000", "00000", "00000"),
}

# ------------------------------------------------------------- canvas ------
# RGB pixel buffer, row-major.
PIX = bytearray(W * H * 3)


def px(x, y, color):
    if 0 <= x < W and 0 <= y < H:
        i = (y * W + x) * 3
        PIX[i], PIX[i + 1], PIX[i + 2] = color


def rect(x, y, w, h, color):
    for yy in range(y, y + h):
        for xx in range(x, x + w):
            px(xx, yy, color)


def line(x0, y0, x1, y1, color):
    dx = abs(x1 - x0)
    dy = -abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx + dy
    while True:
        px(x0, y0, color)
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 >= dy:
            err += dy
            x0 += sx
        if e2 <= dx:
            err += dx
            y0 += sy


def disc(cx, cy, r, color):
    for yy in range(cy - r, cy + r + 1):
        for xx in range(cx - r, cx + r + 1):
            if (xx - cx) ** 2 + (yy - cy) ** 2 <= r * r:
                px(xx, yy, color)


def circle(cx, cy, r, color):
    steps = max(24, r * 6)
    for i in range(steps):
        a = 2 * pi * i / steps
        px(int(cx + r * cos(a)), int(cy + r * sin(a)), color)


def triangle(x0, y0, x1, y1, x2, y2, color):
    # Fill by scanline between edges.
    ys = sorted([y0, y1, y2])
    for yy in range(ys[0], ys[2] + 1):
        xs = []
        for (ax, ay, bx, by) in ((x0, y0, x1, y1), (x1, y1, x2, y2),
                                 (x2, y2, x0, y0)):
            if ay == by:
                continue
            if min(ay, by) <= yy <= max(ay, by):
                xs.append(ax + (bx - ax) * (yy - ay) / (by - ay))
        if len(xs) >= 2:
            for xx in range(int(min(xs)), int(max(xs)) + 1):
                px(xx, yy, color)


# -------------------------------------------------------------- text -------
def char_w(scale):
    return 5 * scale + scale  # glyph + one space of tracking


def text_w(text, scale):
    if not text:
        return 0
    return len(text) * char_w(scale) - scale


def draw_text(text, x, y, scale, color):
    cx = x
    for ch in text:
        glyph = FONT.get(ch, FONT[" "])
        for row in range(7):
            bits = glyph[row]
            for col in range(5):
                if bits[col] == "1":
                    rect(cx + col * scale, y + row * scale,
                         scale, scale, color)
        cx += char_w(scale)
    return cx


def draw_text_centered(text, cx, y, scale, color):
    draw_text(text, cx - text_w(text, scale) // 2, y, scale, color)


def wrap(text, scale, max_w):
    """Greedy word wrap using the bitmap font metrics."""
    lines = []
    for word in text.split(" "):
        if not lines:
            lines.append(word)
            continue
        trial = lines[-1] + " " + word
        if text_w(trial, scale) <= max_w:
            lines[-1] = trial
        else:
            lines.append(word)
    return lines


# -------------------------------------------------------------- PNG --------
def png_bytes():
    raw = bytearray()
    for y in range(H):
        raw.append(0)  # filter: none
        raw += PIX[y * W * 3:(y + 1) * W * 3]
    ihdr = struct.pack(">IIBBBBB", W, H, 8, 2, 0, 0, 0)

    def chunk(typ, data):
        out = struct.pack(">I", len(data)) + typ + data
        out += struct.pack(">I", zlib.crc32(typ + data) & 0xFFFFFFFF)
        return out

    return (b"\x89PNG\r\n\x1a\n"
            + chunk(b"IHDR", ihdr)
            + chunk(b"IDAT", zlib.compress(bytes(raw), 9))
            + chunk(b"IEND", b""))


# ------------------------------------------------------------ colours ------
NAVY = (20, 33, 61)
RED = (178, 34, 34)
INK = (24, 24, 24)
GREY = (90, 90, 90)
WHITE = (255, 255, 255)
PAPER = (250, 248, 240)
PANEL_LINE = (40, 40, 40)

# ------------------------------------------------------------ stories ------
# (kicker, headline, body, motif band colour)
PANELS = [
    ("SUMMIT",
     "PEACE DECLARATION",
     "Trump, Xi and Putin vow nuclear war 'must never be fought'. "
     "No mention of Ukraine or Iran.",
     (219, 234, 254)),
    ("WEATHER",
     "CYCLONE AKVAN HITS ODISHA",
     "Landfall near Gopalpur at noon, winds to 110 km/h. "
     "Over 72,000 evacuated; red alert.",
     (207, 250, 254)),
    ("EUROPE",
     "EU-UK SUMMIT IN BRUSSELS",
     "PM Burnham meets Costa and von der Leyen on trade and energy. "
     "Brexit 'has not worked'.",
     (254, 243, 199)),
    ("UKRAINE",
     "EMBASSIES HIT IN KYIV",
     "EU summons Russia's envoy after Kyiv strikes hit Dutch and "
     "Austrian embassies. One killed.",
     (254, 249, 195)),
    ("TECH",
     "CANADA BETS ON AI DATA CENTRES",
     "Canada embraces AI data centres as US projects face pushback. "
     "Investors look north.",
     (224, 231, 255)),
    ("YEMEN",
     "VOICES FROM BESIEGED TAIZ",
     "'I tell my son it's just fireworks,' says a mother trapped in "
     "besieged Taiz.",
     (253, 230, 138)),
]


# ------------------------------------------------------------ motifs -------
def motif_summit(bx, by, bw, bh):
    # Three leaders as three circles, with an olive branch below.
    cy = by + 46
    for cx, color in ((bx + 130, (30, 58, 138)),
                      (bx + bw // 2, (178, 34, 34)),
                      (bx + bw - 130, (180, 140, 40))):
        disc(cx, cy, 24, color)
        disc(cx, cy, 24, color)
        # face hint
        disc(cx, cy - 4, 15, (245, 220, 190))
        rect(cx - 15, cy + 8, 30, 12, color)
    line(bx + 40, by + 74, bx + bw - 40, by + 74, (34, 120, 60))
    for lx in range(bx + 60, bx + bw - 50, 26):
        disc(lx, by + 70, 5, (34, 120, 60))


def motif_cyclone(bx, by, bw, bh):
    cx, cy = bx + bw // 2, by + 44
    for r in (12, 22, 32):
        circle(cx, cy, r, (8, 120, 150))
    disc(cx, cy, 6, (8, 120, 150))
    # spiral arms
    for start in (0.0, 2.1, 4.2):
        px0, py0 = cx, cy
        for t in range(1, 13):
            a = start + t * 0.35
            r = 4 + t * 2.4
            nx, ny = int(cx + r * cos(a)), int(cy + r * sin(a))
            line(px0, py0, nx, ny, (8, 120, 150))
            px0, py0 = nx, ny
    # rain
    for rx in range(bx + 24, bx + bw - 20, 30):
        line(rx, by + bh - 12, rx - 5, by + bh - 2, (8, 120, 150))


def motif_europe(bx, by, bw, bh):
    # EU circle of stars on blue, flanked by two small flags.
    rect(bx, by, bw, bh, (30, 58, 138))
    cx, cy = bx + bw // 2, by + 46
    for i in range(12):
        a = 2 * pi * i / 12 - pi / 2
        disc(int(cx + 32 * cos(a)), int(cy + 32 * sin(a)), 4, (250, 210, 0))
    disc(cx, cy, 3, (250, 210, 0))
    # mini Union Jack on the left
    fx, fy = bx + 16, by + bh - 30
    rect(fx, fy, 34, 20, WHITE)
    rect(fx + 14, fy, 6, 20, RED)
    rect(fx, fy + 7, 34, 6, RED)
    # mini EU flag on the right, on a white card so it stands out
    fx = bx + bw - 50
    rect(fx - 2, fy - 2, 38, 24, WHITE)
    rect(fx, fy, 34, 20, (30, 58, 138))
    for i in range(6):
        a = 2 * pi * i / 6 - pi / 2
        disc(int(fx + 17 + 7 * cos(a)), int(fy + 10 + 7 * sin(a)), 1,
             (250, 210, 0))


def motif_ukraine(bx, by, bw, bh):
    # Embassy building with a crack, blue/yellow flag on a pole.
    rect(bx + 30, by + 26, 120, bh - 26, (148, 148, 148))
    rect(bx + 30, by + 26, 120, 8, (90, 90, 90))
    for wy in (by + 44, by + 62):
        for wx in (bx + 44, bx + 74, bx + 104, bx + 128):
            rect(wx, wy, 12, 10, (255, 244, 180))
    # crack zig-zag down the facade
    pts = [(bx + 96, by + 26), (bx + 88, by + 40), (bx + 102, by + 54),
           (bx + 90, by + 68), (bx + 100, by + 84)]
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        line(x0, y0, x1, y1, (40, 40, 40))
    # flag pole + Ukrainian flag, right side of the band
    line(bx + bw - 120, by + 10, bx + bw - 120, by + bh, (60, 60, 60))
    rect(bx + bw - 118, by + 12, 56, 12, (0, 91, 187))
    rect(bx + bw - 118, by + 24, 56, 12, (255, 213, 0))
    # ground line
    line(bx + 10, by + bh - 2, bx + bw - 10, by + bh - 2, (90, 90, 90))


def motif_tech(bx, by, bw, bh):
    # Three server racks with blinking lights, joined by cables.
    starts = (bx + 84, bx + bw // 2 - 31, bx + bw - 118)
    for i, sx in enumerate(starts):
        rect(sx, by + 12, 62, bh - 24, (40, 44, 66))
        for row in range(3):
            ry = by + 22 + row * 20
            rect(sx + 8, ry, 46, 12, (70, 78, 105))
            disc(sx + 14, ry + 6, 3, (0, 200, 120) if row != 1 else (250, 210, 0))
            disc(sx + 24, ry + 6, 3, (0, 180, 220))
    # cables between racks
    line(starts[0] + 62, by + 34, starts[1], by + 34, (0, 180, 220))
    line(starts[1] + 62, by + 40, starts[2], by + 40, (0, 180, 220))


def motif_yemen(bx, by, bw, bh):
    # Dusk skyline, crescent moon, and a speech bubble.
    rect(bx, by, bw, bh, (253, 230, 138))
    disc(bx + bw - 52, by + 26, 14, WHITE)
    disc(bx + bw - 44, by + 22, 12, (253, 230, 138))
    # skyline silhouettes spanning the band
    heights = (34, 52, 40, 62, 46, 56, 38)
    step = (bw - 28) // len(heights)
    x = bx + 14
    for hh in heights:
        rect(x, by + bh - hh, step - 16, hh, (90, 70, 50))
        x += step
    # speech bubble with three dots
    sx, sy = bx + bw // 2 - 10, by + 10
    rect(sx, sy, 96, 30, WHITE)
    triangle(sx + 12, sy + 30, sx + 26, sy + 30, sx + 14, sy + 42, WHITE)
    for dx in (18, 44, 70):
        disc(sx + dx, sy + 15, 4, (90, 70, 50))


MOTIFS = [motif_summit, motif_cyclone, motif_europe,
          motif_ukraine, motif_tech, motif_yemen]


# ------------------------------------------------------------ layout -------
def draw_panel(px0, py0, pw, ph, panel, motif_fn):
    kicker, headline, body, band = panel
    rect(px0, py0, pw, ph, WHITE)
    # border
    rect(px0, py0, pw, 2, PANEL_LINE)
    rect(px0, py0 + ph - 2, pw, 2, PANEL_LINE)
    rect(px0, py0, 2, ph, PANEL_LINE)
    rect(px0 + pw - 2, py0, 2, ph, PANEL_LINE)
    # motif band
    rect(px0 + 2, py0 + 2, pw - 4, 100, band)
    motif_fn(px0 + 2, py0 + 2, pw - 4, 100)
    # kicker tag, top-left over the band
    rect(px0 + 10, py0 + 10, text_w(kicker, 2) + 12, 20, NAVY)
    draw_text(kicker, px0 + 16, py0 + 14, 2, WHITE)
    # headline, up to 2 lines, scale 3
    tx = px0 + 14
    max_w = pw - 28
    head_lines = wrap(headline, 3, max_w)
    assert len(head_lines) <= 2, "headline too long: %r" % (headline,)
    hy = py0 + 114
    for ln in head_lines:
        draw_text(ln, tx, hy, 3, INK)
        hy += 26
    # rule under headline
    line(tx, hy + 2, px0 + pw - 14, hy + 2, (200, 200, 200))
    # body, up to 4 lines, scale 2
    body_lines = wrap(body, 2, max_w)
    assert len(body_lines) <= 4, "body too long: %r -> %r" % (body, body_lines)
    by = hy + 12
    for ln in body_lines:
        draw_text(ln, tx, by, 2, (60, 60, 60))
        by += 16


def main():
    rect(0, 0, W, H, PAPER)

    # ---- title bar ----
    rect(0, 0, W, 116, NAVY)
    rect(0, 116, W, 6, RED)
    draw_text_centered("WORLD NEWS", W // 2, 16, 9, WHITE)
    draw_text_centered("FRIDAY 20 NOVEMBER 2026", W // 2, 86, 3, (255, 220, 120))

    # ---- 2x3 grid: 2 columns, 3 rows ----
    gx, gy = 21, 134
    pw, ph = 484, 263
    gap = 14
    for i, panel in enumerate(PANELS):
        col, row = i % 2, i // 2
        draw_panel(gx + col * (pw + gap), gy + row * (ph + gap),
                   pw, ph, panel, MOTIFS[i])

    # ---- footer ----
    draw_text_centered(
        "Sources: Reuters / Devdiscourse / IMD / EU Council / BBC News",
        W // 2, 966, 2, GREY)
    draw_text_centered("All stories reported on Friday 20 November 2026.",
                       W // 2, 990, 2, GREY)

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.png")
    with open(path, "wb") as f:
        f.write(png_bytes())
    print("wrote %s (%dx%d)" % (path, W, H))


if __name__ == "__main__":
    main()
