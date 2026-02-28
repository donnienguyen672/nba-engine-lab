# Promotion Gate

## Requirements for promoting code from lab → nba-engine

Before any module is promoted from `nba-engine-lab` to the governed
`nba-engine` repository, ALL of the following must be true:

### 1. Tests Pass
- All unit tests in `tests/` pass (`pytest tests/ -v`)
- Coverage for promoted module ≥ 80%

### 2. Layer Compliance
- Module respects canonical layer path: `data → adapters → state → ui`
- No circular imports
- State layer modules have zero I/O

### 3. CI Green
- Lab CI workflow passes on the promoting commit
- No imports from `nba-engine` exist in lab

### 4. Adapter Verified
- Adapter output matches canonical GameState/PBPEvent schema
- At least 3 real API responses tested through adapter

### 5. Commander Approval
- Promotion request logged in `promotion_log.md`
- Explicit Commander sign-off before merge to `nba-engine`

### 6. Diff Review
- Minimal diff — no unrelated changes bundled
- No new dependencies unless pre-approved
