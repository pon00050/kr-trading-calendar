"""kr-trading-calendar — KRX trading-day math for Korean capital markets."""

from kr_trading_calendar._calendar import (
    is_trading_day,
    trading_day_offset,
    trading_days_in_range,
)

__all__ = ["is_trading_day", "trading_day_offset", "trading_days_in_range"]
__version__ = "0.1.0"
