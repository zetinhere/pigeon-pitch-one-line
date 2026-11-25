# Manual tournament record — Pigeon Pitch, One Line
## Why manual
- Proxy judge DOWN on 26 Nov 2026 ~04:30-04:50 WIB:
  - 9router gateway (100milionseek/deepseek-v4.1-flash-free): first probe OK (25s), then all
    judge calls failed — mixed "Extra data: line 1 column 1170" (gateway returns JSON + trailing
    SSE `data: [DONE]`, json.load chokes) and HTTP 503 Service Unavailable; later a plain
    curl probe hung 240s with HTTP 000 (no response at all). Gateway health endpoint still OK.
  - Direct 100milionseek route (hms.py helper): SSL read timeout ~120s on a trivial prompt;
    a judge-style direct probe was launched ~04:52 WIB and was still running at last check.
  - A sibling agent's tournament (absurd-clause contest) was hitting the same gateway at the
    same time and also logging 503s — provider-side slowness/outage, not our code.
  - Automated tournament run 1: Swiss round 1 completed with ALL games 0.50-0.50 (every call
    errored) — discarded as garbage. Process stopped.
- Per task brief: "if the judge is down entirely, do a careful manual tournament and say so."
  This file is that manual tournament, judged by the builder against the published brief,
  criteria in order: (1) on-subject pitch, (2) funnier/real joke, (3) original/surprising,
  (4) pigeon voice + city life, (5) tight, every word earning its place.

## Candidates (28, all <=200 chars)
See /tmp/pigeon/candidates.py. Criterion scores (F/O/V/T, each /5):
- statue-ads 3.5/4/3.5/4 | poop-fertilizer 3.5/3/4/3.5 | crumb-uber 4/3.5/4.5/4.5
- pigeon-post 3/2.5/3.5/4 | sidewalk 4/4.5/4.5/5 | statue-cleaning 4/4/4/4.5
- coo-ratings 4/4/4.5/4 | air-rights 3.5/4/4.5/4 | ledge-airbnb 3.5/3/4/4
- ten-thousand-staff 3.5/3/4/4 | moat 3.5/3.5/3.5/4.5 | windows 4/3/4.5/4
- no-office 3.5/3/4/4 | wing-ads 4.5/4/4.5/4 | term-sheet 3.5/3.5/4/4.5
- drone-network 4.5/4.5/4/4 | seed-round 4/3.5/4/3.5 | bench-coworking 3/3.5/4/4
- coocommerce 3.5/3.5/4/4 | bet-on-pigeon 3.5/3/4/3.5 | tam-crumbs 3.5/3.5/4/4.5
- uber-of-sky 3/2.5/3.5/3.5 | product-market-fit 3.5/3.5/4/4.5
- silent-partner 4/4/4.5/4.5 | disrupt-statues 4/4/4.5/4 | doordash 4/3.5/5/4
- hawk-churn 4.5/4.5/4.5/4 | coo-ipo 3.5/3.5/3.5/4

## Shortlist (top 6 by totals)
sidewalk (18), hawk-churn (17.5), drone-network (17), wing-ads (17),
silent-partner (17), statue-cleaning (16.5).

## Head-to-heads (top 6 round-robin, judge criteria in order)
- sidewalk loses all 5: it never names a startup/product/investors, so it falls at
  criterion 1 against every clear pitch, however funny. Dropped despite the best raw score.
- hawk-churn beats drone-network (margin 1-2: "churn problem is hawks" lands harder),
  silent-partner (margin 1), statue-cleaning (margin 2).
- wing-ads beats hawk-churn (margin 2: "impressions you can literally count in droppings"
  is funnier and the ad-space idea more original than another logistics pitch),
  drone-network (margin 1-2), silent-partner (margin 2), statue-cleaning (margin 2).
- drone-network beats silent-partner (margin 1: real joke over a pun) and statue-cleaning (margin 2).
- silent-partner beats statue-cleaning (margin 2: statue co-founder + "I'm the one doing the flying").

## Standings
1. wing-ads 4-0
2. hawk-churn 3-1
3. drone-network 2-2
4. silent-partner 1-3
5. statue-cleaning 0-4
6. sidewalk 0-5 (criterion-1 casualty)

## WINNER (manual)
wing-ads (128 chars):
"We sell ad space on pigeons: your logo, 10,000 wings, every park in the city — impressions you can literally count in droppings."

Why it wins: unambiguous pitch (criterion 1); the "impressions / droppings" double meaning
is the hardest-landing joke in the field (criterion 2); selling ad space on pigeons is a
surprising business no other candidate tries (criterion 3); 10,000 wings + every park =
unmistakably pigeon city life (criterion 4); 128 chars, no wasted word (criterion 5).
Runner-up: hawk-churn ("...Our only churn problem is hawks.") — keep as v2 candidate.

## Proxy-judge verification (26 Nov 2026, ~05:05-05:35 WIB) — OVERTURNS the manual result
- The direct 100milionseek route revived (hms.py helper). Judge: deepseek-v4.1-flash-free,
  verdict-first prompt ("FIRST line Verdict: A/B, SECOND line Margin: 1-5, then a short
  reason, under 120 words"), max_tokens 300, ~5 min per call, sequential, 580s timeout.
  Raw verdicts in proxy_verdicts.json (repo) / /tmp/pigeon/verify_final.json + verify_hawk.json.
- wing-ads vs hawk-churn: proxy picked HAWK both orders, margins 3 and 4 → game 0.85-0.15.
  Reasons: "churn problem is hawks" is a sharper, deadpan, pigeon-specific punchline;
  the droppings pun is "funny but milder and less surprising".
- hawk-churn vs drone-network: HAWK both orders, margins 3 and 4 → game 0.85-0.15.
- hawk-churn vs silent-partner: SPLIT — hawk margin 3, silent margin 3 → game 0.50-0.50.
- Proxy tally (6 calls): hawk-churn won 5, silent-partner 1. hawk-churn is the proxy
  winner and the program's pick; main.py ranks by proxy game score first.
- Note: an earlier parallel verify_top4 run (4 workers) produced only SIGTERM'd empty
  calls (rc -15) — parallel hms.py calls that night were killed; sequential calls worked.

## FINAL WINNER
hawk-churn (134 chars):
"I run a logistics company with zero vehicles, zero fuel, and 10,000 couriers who navigate by the sun. Our only churn problem is hawks."

Why it wins (proxy + manual): unambiguous logistics-company pitch (criterion 1);
the "churn problem is hawks" punchline is the hardest-landing joke in the field and
the most pigeon-specific one — only a pigeon fears hawks as a business risk
(criteria 2 + 4); the deadpan startup-metrics setup collapsing into predation is
surprising (criterion 3); 134 chars, no wasted word (criterion 5).
