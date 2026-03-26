# kr-trading-calendar

KRX trading-day math for Korean capital markets.

Three functions that answer: *"What date is N trading days from here?"*, *"Is this date a trading day?"*, and *"How many trading sessions are in this range?"* — correctly accounting for Korean holidays (설날, 추석, 공휴일) and KRX market closures.

## The Problem

Korean capital markets observe ~15 non-weekend holidays per year. Naively subtracting 60 calendar days to build a price window gives you ~38 trading sessions, not 60. This off-by-37% error silently corrupts any analysis that uses trading-day windows — backtests, event studies, anomaly detection.

`exchange_calendars` provides the raw KRX session data, but its API is verbose for common operations. This package wraps it into three one-liners.

### 임시공휴일 (Ad-hoc holidays)

The Korean government occasionally declares ad-hoc public holidays (e.g., election days, bridge holidays). These require a community PR to `exchange_calendars` and lag by days to weeks. For live/current-year use, cross-check against the data.go.kr 특일정보 API (dataset 15012690).

## Quick Start

```bash
pip install kr-trading-calendar
# or
uv add kr-trading-calendar
```

```python
from kr_trading_calendar import trading_day_offset, is_trading_day, trading_days_in_range
```

## API

### `is_trading_day(date) -> bool`

Returns `True` if the date is a KRX trading session.

```python
is_trading_day("2021-01-08")   # True  (Friday, no holiday)
is_trading_day("2021-02-12")   # False (설날)
is_trading_day("2020-10-01")   # False (추석)
```

### `trading_day_offset(date, n) -> pd.Timestamp`

Returns the KRX session `n` trading days from `date`. Positive = forward, negative = backward. If `date` is not a session, snaps to the nearest session in the offset direction before counting.

```python
trading_day_offset("2021-02-15", -60)  # 2020-11-16
trading_day_offset("2021-02-15",  60)  # 2021-05-12
```

### `trading_days_in_range(start, end) -> pd.DatetimeIndex`

Returns all KRX trading sessions between `start` and `end` (inclusive).

```python
sessions = trading_days_in_range("2021-01-04", "2021-01-08")
len(sessions)  # 5 (Mon-Fri, no holidays that week)
```

All three functions accept `str` or `pd.Timestamp` for date arguments.

## Coverage & Limitations

- **Source:** [`exchange_calendars`](https://github.com/gerrymanoim/exchange_calendars) XKRX calendar
- **Historical coverage:** Complete for 2000-2024
- **Holidays covered:** All statutory Korean public holidays, KRX-specific closures
- **Not covered in real-time:** 임시공휴일 (ad-hoc government holidays) — see note above

## Relationship to krff-shell

This package was extracted from [krff-shell](https://github.com/pon00050/krff-shell), where it powers the ±60 trading-day price windows used in CB/BW event analysis and timing anomaly detection. It has zero dependencies on that project and is useful independently for any Korean market data work.

## Development

```bash
# Install dependencies
uv sync --extra dev

# Run tests
uv run pytest tests/ -v

# Quick smoke test
uv run python -c "from kr_trading_calendar import trading_day_offset; print(trading_day_offset('2021-02-15', -60))"
```

**Conventions**
- Python >=3.11
- All dates normalize to midnight via `pd.Timestamp.normalize()`
- `trading_day_offset` snaps non-session dates to the nearest session in the offset direction before counting
- Build backend: hatchling; package manager: uv

## License

MIT
