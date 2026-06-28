"""
Regression tests for the Game Glitch Investigator bug fixes.

These target two bugs that were fixed in the guessing game:

1. Opposite / parity-broken hints
   - The "Go HIGHER!" / "Go LOWER!" hint text was swapped relative to the
     comparison, and on alternating attempts the secret was stringified so the
     comparison ran lexicographically (e.g. secret=2: guess 12 -> "Go HIGHER",
     guess 13 -> "Go LOWER", never converging).
   - The hints must always point the player toward the secret.

2. New Game button did nothing
   - The reset left ``status`` as "won"/"lost", so the next run hit ``st.stop()``
     and the new game never started. A new game must reset every tracked value,
     including ``status`` back to "playing".
"""

import os
import sys

# Make the project root importable no matter where pytest is invoked from.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest

from logic_utils import check_guess, make_new_game_state, get_range_for_difficulty


# ---------------------------------------------------------------------------
# Bug 1: hint direction must lead the guess toward the secret
# ---------------------------------------------------------------------------

def test_guess_below_secret_says_go_higher():
    outcome, message = check_guess(20, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message


def test_guess_above_secret_says_go_lower():
    outcome, message = check_guess(80, 50)
    assert outcome == "Too High"
    assert "LOWER" in message


def test_correct_guess_wins():
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"
    assert "Correct" in message


@pytest.mark.parametrize(
    "guess, secret, expected_outcome, expected_word",
    [
        # The exact scenario reported: Easy mode, secret=2.
        # Both 12 and 13 are above 2, so both must say "Too High" / "Go LOWER".
        (12, 2, "Too High", "LOWER"),
        (13, 2, "Too High", "LOWER"),
        (1, 2, "Too Low", "HIGHER"),
        (1, 20, "Too Low", "HIGHER"),
        (20, 1, "Too High", "LOWER"),
        (100, 99, "Too High", "LOWER"),
    ],
)
def test_hint_direction_regression(guess, secret, expected_outcome, expected_word):
    outcome, message = check_guess(guess, secret)
    assert outcome == expected_outcome
    assert expected_word in message


@pytest.mark.parametrize("secret", range(1, 21))
def test_following_hints_always_reaches_the_secret(secret):
    """
    Simulate a player who only follows the on-screen hint text. Doing a binary
    search guided purely by "Go HIGHER" / "Go LOWER" must converge on the
    secret. If the hints were reversed (or the comparison broken), the search
    would walk away from the answer and never win.
    """
    low, high = 1, 20
    lo, hi = low, high

    for _ in range(50):  # plenty of steps for a range of 20
        guess = (lo + hi) // 2
        outcome, message = check_guess(guess, secret)

        if outcome == "Win":
            assert guess == secret
            break

        if "HIGHER" in message:
            lo = guess + 1
        elif "LOWER" in message:
            hi = guess - 1
        else:
            pytest.fail(f"Unexpected hint message: {message!r}")

        assert lo <= hi, "Hints led the search past the secret (wrong direction)"
    else:
        pytest.fail(f"Never converged on secret {secret} by following the hints")


# ---------------------------------------------------------------------------
# Bug 2: New Game must fully reset the game
# ---------------------------------------------------------------------------

def test_new_game_resets_status_to_playing():
    # This is THE fix: a finished game (won/lost) must be able to restart.
    state = make_new_game_state(1, 20)
    assert state["status"] == "playing"


def test_new_game_clears_score_history_and_attempts():
    state = make_new_game_state(1, 20)
    assert state["score"] == 0
    assert state["history"] == []
    assert state["attempts"] == 0


def test_new_game_returns_all_tracked_keys():
    state = make_new_game_state(1, 20)
    assert set(state.keys()) == {"secret", "attempts", "score", "status", "history"}


@pytest.mark.parametrize("difficulty", ["Easy", "Normal", "Hard"])
def test_new_game_secret_respects_difficulty_range(difficulty):
    low, high = get_range_for_difficulty(difficulty)
    for _ in range(200):  # secret is random; sample enough to trust the bounds
        state = make_new_game_state(low, high)
        assert low <= state["secret"] <= high


def test_new_game_restarts_a_finished_game():
    """End-to-end style: starting from a 'won' game, a new game is playable."""
    finished = {"secret": 7, "attempts": 5, "score": 80, "status": "won",
                "history": [3, 9, 7]}

    fresh = make_new_game_state(1, 20)
    finished.update(fresh)  # mimics app.py applying the new-game state

    assert finished["status"] == "playing"
    assert finished["score"] == 0
    assert finished["history"] == []
    assert finished["attempts"] == 0
