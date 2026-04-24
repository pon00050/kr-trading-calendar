# CLAUDE.md — kr-trading-calendar

KRX trading-day math for Korean capital markets. Wraps `exchange_calendars` XKRX.

## Ecosystem

Part of the Korean forensic accounting toolkit.
- Hub: `../forensic-accounting-toolkit/` | [GitHub](https://github.com/pon00050/forensic-accounting-toolkit)
- Task board: https://github.com/users/pon00050/projects/1
- Role: Foundation library
- Depends on: none
- Consumed by: krff-shell (trading-day math), kr-derivatives (calendar module)

## Common Commands

```bash
# Install with dev dependencies
uv sync --extra dev

# Run tests (13 tests)
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

## Known Gaps

| Gap | Why | Status |
|-----|-----|--------|
| 임시공휴일 (ad-hoc holidays) lag by days/weeks | Depends on upstream `exchange_calendars` community PR cycle | By design — documented in `_calendar.py:11` |

## Conventions

- Calendar instance is lazy-loaded and cached (module-level `_xkrx`)
- All date inputs accept `str` or `pd.Timestamp`
- 임시공휴일 (ad-hoc holidays) may lag in exchange_calendars — see `_calendar.py` docstring
- Build system: hatchling (same as ecosystem standard)

## Commit Protocol

1. `uv run pytest tests/ -v` — all green
2. Stage specific files by name
3. Commit with descriptive message


---

**Working notes** (regulatory analysis, legal compliance research, or anything else not appropriate for this public repo) belong in the gitignored working directory of the coordination hub. Engineering docs (API patterns, test strategies, run logs) stay here.

---

## NEVER commit to this repo

This repository is **public**. Before staging or writing any new file, check the list below. If the content matches any item, route it to the gitignored working directory of the coordination hub instead, NOT to this repo.

**Hard NO list:**

1. **Any API key, token, or credential — even a truncated fingerprint.** This includes Anthropic key fingerprints (sk-ant-...), AWS keys (AKIA...), GitHub tokens (ghp_...), DART/SEIBRO/KFTC API keys, FRED keys. Even partial / display-truncated keys (e.g. "sk-ant-api03-...XXXX") leak the org-to-key linkage and must not be committed.
2. **Payment / billing data of any kind.** Card numbers (full or last-four), invoice IDs, receipt numbers, order numbers, billing-portal URLs, Stripe/Anthropic/PayPal account states, monthly-spend caps, credit balances.
3. **Vendor support correspondence.** Subject lines, body text, ticket IDs, or summaries of correspondence with Anthropic / GitHub / Vercel / DART / any vendor's support team.
4. **Named third-party outreach targets.** Specific company names, hedge-fund names, audit-firm names, regulator-individual names appearing in a planning, pitch, or outreach context. Engineering content discussing Korean financial institutions in a neutral domain context (e.g. "DART is the FSS disclosure system") is fine; planning text naming them as a sales target is not.
5. **Commercial-positioning memos.** Documents discussing buyer segments, monetization models, pricing strategy, competitor analysis, market positioning, or go-to-market plans. Research methodology and technical roadmaps are fine; commercial strategy is not.
6. **Files matching the leak-prevention .gitignore patterns** (*_prep.md, *_billing*, *_outreach*, *_strategy*, *_positioning*, *_pricing*, *_buyer*, *_pitch*, product_direction.md, etc.). If you find yourself wanting to write a file with one of these names, that is a signal that the content belongs in the hub working directory.

**When in doubt:** put the content in the hub working directory (gitignored), not this repo. It is always safe to add later. It is expensive to remove after force-pushing — orphaned commits remain resolvable on GitHub for weeks.

GitHub Push Protection is enabled on this repo and will reject pushes containing well-known credential patterns. That is a backstop, not the primary defense — write-time discipline is.
