# World News — Friday 20 November 2026

A newspaper front page drawn entirely in code: one 1024x1024 PNG that
sums up 20 November 2026's world news in a single image.

## The image

A dark title bar reads **WORLD NEWS** with the date
**FRIDAY 20 NOVEMBER 2026**. Below it, a 2x3 grid of six panels, one per
story, each with a kicker tag, a bold headline, a few lines of text, and
a simple drawn motif. A footer line lists the sources.

## The six stories

1. **SUMMIT — Peace declaration.** Trump, Xi and Putin issue a joint
   declaration from Shenzhen: a nuclear war "cannot be won and must
   never be fought", plus UN reform and more refined-fuel supplies.
   No mention of Ukraine or Iran.
2. **WEATHER — Cyclone Akvan hits Odisha.** Severe Cyclonic Storm Akvan
   makes landfall near Gopalpur around noon IST, winds 90-100 km/h
   gusting to 110. Over 72,000 people evacuated; red alert in force.
3. **EUROPE — EU-UK summit in Brussels.** UK PM Andy Burnham meets
   Antonio Costa and Ursula von der Leyen on trade, youth mobility and
   energy. Burnham has said Brexit "has not worked".
4. **UKRAINE — Embassies hit in Kyiv.** Russian strikes damage the
   Dutch and Austrian embassies (1 killed, 5 hurt). The EU summons
   Russia's ambassador.
5. **TECH — Canada bets on AI data centres.** Canada embraces AI data
   centres while US projects face local pushback; investors look north.
6. **YEMEN — Voices from besieged Taiz.** BBC speaks to people trapped
   in Taiz: "I tell my son it's just fireworks."

Full sourcing is in `NEWS.md`.

## How to run

Requires Python 3. Standard library only — no network, no external
files, no dependencies.

```sh
python3 main.py
```

This writes `entry.png` to `$MAKEFUN_OUTPUT_DIR` (default `/output`).
The output is a 1024x1024 PNG under 1 MiB. Running it twice produces a
byte-identical file: no timestamps, no randomness, fixed ordering.

Everything is drawn programmatically: the program includes its own PNG
encoder (zlib + struct) and its own hand-defined 5x7 bitmap font, and
all motifs are simple geometric shapes (rectangles, circles, lines).
