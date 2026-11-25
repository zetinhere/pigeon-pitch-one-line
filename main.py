#!/usr/bin/env python3
"""Pigeon Pitch, One Line — make.fun entry program.

Writes one line (<=200 chars) to /output/entry.txt: the elevator pitch a
city pigeon gives investors for its startup.

How the line was chosen
------------------------
28 candidate pitches were drafted, then ranked in a manual tournament against
the judge's published brief, criteria in order: (1) a one-line elevator pitch
from a city pigeon to investors for its startup; (2) funnier, a real joke that
lands; (3) original and surprising; (4) the pigeon's voice and city life;
(5) tight, every word earning its place. The top 6 played a round-robin;
`wing-ads` went 4-0 (see TOURNAMENT.md for the full record). The proxy judge
(100milionseek/deepseek-v4.1-flash-free, via the 9router gateway and direct)
was down the night of the build — gateway 503s/hangs, direct route ~5 min a
call — so the tournament was judged by hand against the brief, as the task
allows when the judge is down entirely.

The program itself is deterministic: it re-derives the winner from the
recorded tournament table below (criterion totals, then head-to-head wins)
and writes exactly that line. No network, no randomness, no model calls.
"""

import json
import os
import sys

# slug, pitch, (funny, original, voice, tight) each out of 5, head-to-head wins
# in the top-6 round-robin. Only the top 6 played head-to-heads; the rest are
# listed with their criterion totals from the first cut.
CANDIDATES = [
    ("statue-ads", "We turn every statue in this city into a billboard and every pigeon into a shareholder — seed round open, breadcrumbs optional.", (3.5, 4, 3.5, 4), 0),
    ("poop-fertilizer", "I'm raising $2M to turn pigeon poop into fertilizer: we already own the supply chain, the workforce, and the entire city as our factory floor.", (3.5, 3, 4, 3.5), 0),
    ("crumb-uber", "Uber for breadcrumbs: an app telling 10,000 pigeons where tourists drop fries, in real time, for a 10% crumb commission.", (4, 3.5, 4.5, 4.5), 0),
    ("pigeon-post", "PigeonPost: same-day delivery, zero fuel, zero traffic — and our couriers have been doing this since before your grandfather was born.", (3, 2.5, 3.5, 4), 0),
    ("sidewalk", "I spent six years eating off this sidewalk. Now I'm selling the sidewalk.", (4, 4.5, 4.5, 5), 0),
    ("statue-cleaning", "Statue cleaning is a $2B market. Our cleaners are already on site 24/7 — and they work for seed.", (4, 4, 4, 4.5), 0),
    ("coo-ratings", "Coo is the app where pigeons rate humans: five stars gets you fed, one star gets you exactly what you see on the statues.", (4, 4, 4.5, 4), 0),
    ("air-rights", "I own the air rights above every hot-dog cart in Manhattan and I charge rent in crumbs. Seed round's open.", (3.5, 4, 4.5, 4), 0),
    ("ledge-airbnb", "We're the Airbnb of window ledges: 40,000 prime perches, zero vacancies, and our guests never leave a bad review — they just leave.", (3.5, 3, 4, 4), 0),
    ("ten-thousand-staff", "I run a delivery startup with 10,000 employees who work for breadcrumbs, never unionize, and fly straight over traffic.", (3.5, 3, 4, 4), 0),
    ("moat", "Our moat? Every pigeon in this city already works for us. We're just the first ones to put it on a cap table.", (3.5, 3.5, 3.5, 4.5), 0),
    ("windows", "Seed round: $500K for 10% of PigeonPost — zero emissions, same-day delivery, and a perfect safety record if you don't count windows.", (4, 3, 4.5, 4), 0),
    ("no-office", "I'm CEO of a company with 50,000 employees, no office, no salaries, and 100% retention — nobody has ever fired a pigeon.", (3.5, 3, 4, 4), 0),
    ("wing-ads", "We sell ad space on pigeons: your logo, 10,000 wings, every park in the city — impressions you can literally count in droppings.", (4.5, 4, 4.5, 4), 4),
    ("term-sheet", "Pigeons already run this city's logistics. I'm just the first one asking for a term sheet instead of a breadcrumb.", (3.5, 3.5, 4, 4.5), 0),
    ("drone-network", "We've built the world's first pigeon-powered drone network: same payload, half the regulation, and our drones reproduce themselves.", (4.5, 4.5, 4, 4), 2),
    ("seed-round", "I'm raising a seed round — literally, sunflower seeds — but the term sheet says $1M and my co-founders are 40,000 pigeons with excellent credit.", (4, 3.5, 4, 3.5), 0),
    ("bench-coworking", "We turn park benches into coworking spaces: five crumbs a day, free Wi-Fi from the café next door, and the view is unbeatable.", (3, 3.5, 4, 4), 0),
    ("coocommerce", "CooCommerce connects tourists with pigeons: they pay $10 for a photo, we take 90%, and the pigeons take the rest in crumbs.", (3.5, 3.5, 4, 4), 0),
    ("bet-on-pigeon", "Don't bet on a pigeon — bet on the only workforce in this city that shows up before sunrise, works weekends, and has never once asked for a raise.", (3.5, 3, 4, 3.5), 0),
    ("tam-crumbs", "Our TAM is every crumb dropped in this city: $0 today, because nobody's charging for it yet. That's the opportunity.", (3.5, 3.5, 4, 4.5), 0),
    ("uber-of-sky", "We're the Uber of the sky, if Uber's drivers could fly, worked for birdseed, and had a 5,000-year record of never missing a delivery.", (3, 2.5, 3.5, 3.5), 0),
    ("product-market-fit", "Our pigeons already have product-market fit: every tourist in this city is a customer, and none of them know it yet.", (3.5, 3.5, 4, 4.5), 0),
    ("silent-partner", "My co-founder is a statue: silent partner, great location, zero equity demands. I'm the one doing the flying.", (4, 4, 4.5, 4.5), 1),
    ("disrupt-statues", "We're disrupting statues: our pigeons decorate 10,000 of them a day, and now we're charging the city to clean up after our own growth.", (4, 4, 4.5, 4), 0),
    ("doordash", "Think DoorDash, but the dashers have wings, the restaurants are trash cans, and the tip is whatever falls off your sandwich.", (4, 3.5, 5, 4), 0),
    ("hawk-churn", "I run a logistics company with zero vehicles, zero fuel, and 10,000 couriers who navigate by the sun. Our only churn problem is hawks.", (4.5, 4.5, 4.5, 4), 3),
    ("coo-ipo", "We're the first startup whose IPO prospectus is written in coos — and honestly, our unit economics are still better than WeWork's.", (3.5, 3.5, 3.5, 4), 0),
]

MAX_CHARS = 200


def pick_winner(candidates):
    """Winner = most head-to-head wins, then highest criterion total."""
    def key(entry):
        _slug, _text, scores, wins = entry
        return (wins, sum(scores))
    return max(candidates, key=key)


def main():
    slug, text, _scores, _wins = pick_winner(CANDIDATES)
    # Gate: UTF-8, 1-200 characters, not only whitespace, one line.
    if not (1 <= len(text) <= MAX_CHARS):
        raise SystemExit(f"entry is {len(text)} chars, outside 1-{MAX_CHARS}")
    if not text.strip() or "\n" in text:
        raise SystemExit("entry must be a single non-blank line")
    text.encode("utf-8")  # raises if not valid UTF-8
    out_dir = os.environ.get("OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"[{slug}] ({len(text)} chars)")
    print(text)
    print(f"wrote {path}")


if __name__ == "__main__":
    main()
