# nba-engine-lab — Architecture

## Purpose

Lab environment for experimenting with NBA data sources before promotion
to the governed `nba-engine` repository.

## Canonical Layer Path

```
src/data → src/adapters → src/state → src/ui
```

| Layer | Responsibility | Rules |
|---|---|---|
| `src/data/` | Raw data fetching (HTTP only) | No normalization. No state. |
| `src/adapters/` | Normalize raw → canonical types | Depends on data + state layers. |
| `src/state/` | Pure state + logic (dataclasses) | No I/O. No imports from data/. |
| `src/ui/panels/` | Display rendering | Depends on state only. |

## Data Sources

| Source | Module | Endpoint |
|---|---|---|
| ESPN Public API | `src/data/espn_scoreboard.py` | `site.api.espn.com` |
| ESPN PBP | `src/data/espn_playbyplay.py` | `site.api.espn.com` |
| NBA Official CDN | `src/data/nba_scoreboard.py` | `cdn.nba.com` |
| NBA Official PBP | `src/data/nba_playbyplay.py` | `cdn.nba.com` |

## Experiments

Experiments live in `experiments/` and are self-contained.
They may violate layer rules internally but must not leak
dependencies into `src/`.

- `experiments/espn_feed/run.py` — ESPN scoreboard experiment
- `experiments/nba_feed/run.py` — NBA official scoreboard experiment

## Promotion Path

Code promoted from lab → `nba-engine` must:
1. Pass all lab CI checks
2. Be logged in `promotion_log.md`
3. Meet `PROMOTION_GATE.md` criteria
4. Receive Commander approval

## Guardrails

- CI fails if any file imports from `nba-engine`
- Lab has no cloud/GCS dependencies
- All state logic is pure (no I/O)
