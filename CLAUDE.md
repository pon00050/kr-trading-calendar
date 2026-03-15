# CLAUDE.md — kr-trading-calendar

KRX trading-day math for Korean capital markets. Wraps `exchange_calendars` XKRX.

## Ecosystem

Part of the Korean forensic accounting toolkit.
- Hub: `../forensic-accounting-toolkit/` | [GitHub](https://github.com/pon00050/forensic-accounting-toolkit)
- Task board: https://github.com/users/pon00050/projects/1
- Role: Foundation library
- Depends on: none
- Consumed by: kr-forensic-finance (trading-day math), kr-derivatives (calendar module)

## Common Commands

```bash
# Install with dev dependencies
uv sync --extra dev

# Run tests
uv run pytest tests/ -v
```

## Architecture

Three public functions wrapping `exchange_calendars` XKRX:

```
src/kr_trading_calendar/
    __init__.py       — re-exports public API
    _calendar.py      — lazy-loaded XKRX calendar + 3 functions
```

| Function | Purpose |
|----------|---------|
| `is_trading_day(date)` | Returns True if date is a KRX session |
| `trading_days_in_range(start, end)` | Returns DatetimeIndex of all sessions in range |
| `trading_day_offset(date, n)` | Returns session n trading days forward/backward |

## Conventions

- Calendar instance is lazy-loaded and cached (module-level `_xkrx`)
- All date inputs accept `str` or `pd.Timestamp`
- 임시공휴일 (ad-hoc holidays) may lag in exchange_calendars — see `_calendar.py` docstring
- Build system: hatchling (same as ecosystem standard)

## Commit Protocol

1. `uv run pytest tests/ -v` — all green
2. Stage specific files by name
3. Commit with descriptive message
