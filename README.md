# nba-engine-lab

Lab environment for NBA data source experiments. Isolated from the governed `nba-engine` repo.

## Quick Start

```bash
pip install -r requirements.txt

# ESPN experiment
python experiments/espn_feed/run.py

# NBA Official experiment
python experiments/nba_feed/run.py

# Run tests
pytest tests/ -v
```

## Structure

```
src/data/          — Raw data fetchers (ESPN + NBA)
src/adapters/      — Normalize raw data → canonical types
src/state/         — Pure state logic (GameState, regime, bonus)
src/ui/panels/     — Display rendering
experiments/       — Self-contained experiment runners
tests/             — Unit tests
schemas/           — Data schemas (future)
docs/              — Architecture docs
```

## Layer Path

```
src/data → src/adapters → src/state → src/ui
```

## CI

GitHub Actions runs pytest and guards against imports from `nba-engine`.
