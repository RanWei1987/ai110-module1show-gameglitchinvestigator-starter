"""
Unit tests for the supporting pure functions in logic_utils.py:
``parse_guess`` and ``update_score``.

These are characterization tests: they pin down the current intended behavior
so future refactors can be checked against them. Where the current behavior
looks suspicious, it is called out in a comment rather than silently locked in.
"""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest

from logic_utils import parse_guess, update_score


# ---------------------------------------------------------------------------
# parse_guess
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "raw, expected",
    [
        ("42", (True, 42, None)),
        ("0", (True, 0, None)),
        ("-5", (True, -5, None)),
        (" 7 ", (True, 7, None)),        # int() tolerates surrounding whitespace
        ("3.9", (True, 3, None)),        # "." path: int(float("3.9")) truncates
        ("-3.9", (True, -3, None)),      # truncates toward zero
    ],
)
def test_parse_guess_valid_inputs(raw, expected):
    assert parse_guess(raw) == expected


@pytest.mark.parametrize("raw", [None, ""])
def test_parse_guess_missing_input(raw):
    ok, value, error = parse_guess(raw)
    assert ok is False
    assert value is None
    assert error == "Enter a guess."


@pytest.mark.parametrize("raw", ["abc", "1,000", "twelve", "  ", "1.2.3"])
def test_parse_guess_non_numeric(raw):
    ok, value, error = parse_guess(raw)
    assert ok is False
    assert value is None
    assert error == "That is not a number."


# ---------------------------------------------------------------------------
# update_score
# ---------------------------------------------------------------------------

def test_win_awards_points_based_on_attempt():
    # points = 100 - 10 * (attempt_number + 1); attempt 1 -> 80
    assert update_score(current_score=0, outcome="Win", attempt_number=1) == 80


def test_win_adds_to_existing_score():
    assert update_score(current_score=20, outcome="Win", attempt_number=1) == 100


def test_win_points_have_a_floor_of_10():
    # Late win: 100 - 10 * (10 + 1) = -10, clamped up to 10.
    assert update_score(current_score=0, outcome="Win", attempt_number=10) == 10


def test_too_low_loses_5_points():
    assert update_score(current_score=50, outcome="Too Low", attempt_number=3) == 45


def test_unknown_outcome_leaves_score_unchanged():
    assert update_score(current_score=42, outcome="Whatever", attempt_number=2) == 42


# NOTE: "Too High" scoring depends on attempt-number parity (+5 on even attempts,
# -5 on odd attempts). This is unusual and may itself be a latent glitch worth
# investigating. These tests characterize the CURRENT behavior, not necessarily
# the desired one.
def test_too_high_gains_5_on_even_attempt():
    assert update_score(current_score=50, outcome="Too High", attempt_number=2) == 55


def test_too_high_loses_5_on_odd_attempt():
    assert update_score(current_score=50, outcome="Too High", attempt_number=3) == 45
