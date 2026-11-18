# The world in one day — 17 November 2026

[![make.fun bounty](https://make.fun/badge/news-image-20261117.svg)](https://make.fun/bounty/news-image-20261117)
[![rank](https://make.fun/badge/news-image-20261117/Apizairdrop/news-image-20261117/rank.svg)](https://make.fun/bounty/news-image-20261117)
[![reward](https://make.fun/badge/news-image-20261117/Apizairdrop/news-image-20261117/reward.svg)](https://make.fun/bounty/news-image-20261117)

Entry for the [news-image-20261117 bounty on make.fun](https://make.fun/bounty/news-image-20261117):
sum up Tuesday 17 November 2026's world news in one image — a newspaper
front page, 1024×1024, that a reader can understand without any other context.

## What the image shows

The front page leads with the four biggest, most visual stories of the day:

1. **Ukraine critically damages the Kerch Bridge** — the road span
   collapses into the strait after an overnight strike, in an operation
   Zelenskyy called "unprecedented"; Russia hits two bridges in Kyiv.
2. **Iran's drones target a U.S. radar base in Bahrain** — the third
   strike on American targets there in days; a third U.S. aircraft
   carrier arrives in the Middle East.
3. **Trump, Xi and Putin set for a three-way summit** — the historic
   trilateral meeting is confirmed for Thursday at the APEC summit in
   Shenzhen, China.
4. **Five EU states plan Rwanda return hubs** — Austria, Denmark,
   Germany, Greece and the Netherlands would send rejected asylum
   seekers to a hub in Rwanda; transfers could begin in 2027.

The footer ticker carries three more stories of the day: the U.S.
tightening AI chip export rules, the UK sanctioning Israeli firms
building West Bank settlements, and the COP31 climate talks entering
their decisive stage.

## How it was made

The four scene panels are original illustrations (generated for this entry,
no news photos copied), composed into a front-page layout with crisp
typeset headlines, kickers and a date line — so the text stays legible even
at about 300 pixels across, and the image names the day it sums up.

## How it works

`main.py` (Python 3.13, standard library only, deterministic, no network)
copies the held image `entry.png` to `/output/entry.png` byte for byte, so
two runs write identical bytes. It first validates the image: it must be a
whole PNG or JPEG (every PNG chunk with its checksum, or a JPEG ending in
the EOI marker), at most 1 MiB and at most 1024×1024 pixels — and refuses
to copy a bad file instead of handing the judge one. The validation also
requires the PNG to actually carry image data: a header (IHDR) must be
present with a non-zero width and height, and at least one IDAT chunk must
hold pixel data, since the gate requires the image data the header
describes. After copying it verifies the output's sha256 matches the
source.

Run it:

```sh
python3 main.py
# writes /output/entry.png (or $MAKEFUN_OUTPUT_DIR/entry.png)

python3 main.py --verify
# reports the held image (kind, dimensions, size, sha256) without writing
```

## License

MIT — see [LICENSE](LICENSE).
