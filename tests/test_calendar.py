"""Tests for kr_trading_calendar.

Ported from the pre-split forensic monolith (now this standalone library).
All date expectations verified against exchange_calendars XKRX v4.13.2.
"""

import pandas as pd

from kr_trading_calendar import is_trading_day, trading_day_offset, trading_days_in_range


class TestIsTradingDay:
    """is_trading_day checks against KRX holidays."""

    def test_known_session(self):
        """2021-01-08 (Friday, no holiday) is a KRX trading session."""
        assert is_trading_day("2021-01-08") is True

    def test_new_year(self):
        """2021-01-01 (신정) is NOT a trading session."""
        assert is_trading_day("2021-01-01") is False

    def test_seollal(self):
        """2021-02-12 (설날) is NOT a trading session."""
        assert is_trading_day("2021-02-12") is False

    def test_seollal_eve(self):
        """2021-02-11 (설날 연휴 시작) is NOT a trading session."""
        assert is_trading_day("2021-02-11") is False

    def test_chuseok(self):
        """2020-10-01 (추석) is NOT a trading session."""
        assert is_trading_day("2020-10-01") is False


class TestTradingDayOffset:
    """trading_day_offset counts trading days, not calendar days."""

    def test_backward(self):
        """60 trading days before 2021-02-15 should be 2020-11-16."""
        result = trading_day_offset("2021-02-15", -60)
        assert result == pd.Timestamp("2020-11-16")

    def test_forward(self):
        """60 trading days after 2021-02-15 should be 2021-05-12."""
        result = trading_day_offset("2021-02-15", 60)
        assert result == pd.Timestamp("2021-05-12")


    def test_non_session_input_forward(self):
        """Offset from a holiday snaps forward before counting.

        2021-02-12 (설날) is a holiday.
        searchsorted returns the index of 2021-02-15 (next session).
        +1 from there gives 2021-02-16 (one step beyond the snap target).
        """
        result = trading_day_offset("2021-02-12", 1)
        assert result == pd.Timestamp("2021-02-16")

    def test_non_session_input_backward(self):
        """Offset from a holiday going backward.

        2021-02-12 (설날) is a holiday.
        searchsorted returns the index of 2021-02-15 (next session).
        -1 from there gives 2021-02-10 (session before the holiday week).
        """
        result = trading_day_offset("2021-02-12", -1)
        assert result == pd.Timestamp("2021-02-10")

    def test_non_session_input_zero(self):
        """Offset of 0 from a holiday returns next session (snap forward)."""
        result = trading_day_offset("2021-02-12", 0)
        assert result == pd.Timestamp("2021-02-15")


class TestTradingDaysInRange:
    """trading_days_in_range returns sessions within a date range."""

    def test_basic(self):
        """Mon-Fri with no holidays = 5 sessions."""
        sessions = trading_days_in_range("2021-01-04", "2021-01-08")
        assert len(sessions) == 5

    def test_window_gives_121_sessions(self):
        """True +/-60 trading-day window around 2021-02-15 = 121 sessions."""
        start = trading_day_offset("2021-02-15", -60)
        end = trading_day_offset("2021-02-15", 60)
        sessions = trading_days_in_range(start, end)
        assert len(sessions) == 121

    def test_calendar_days_differ_from_trading_days(self):
        """Documents that 60 calendar days != 60 trading days.

        +/-60 calendar days around 2021-02-15 gives only 38 sessions per side,
        not 60. This is the off-by-N error that this library was extracted to fix.
        """
        old_start = pd.Timestamp("2020-12-17")  # 2021-02-15 - 60 calendar days
        issue_date = pd.Timestamp("2021-02-15")
        sessions_one_side = trading_days_in_range(old_start, issue_date)
        assert len(sessions_one_side) == 38
