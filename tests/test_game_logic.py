from logic_utils import check_guess, update_score, parse_guess


def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"


def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High" -> go LOWER
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert "LOWER" in message


def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low" -> go HIGHER
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message


# --- Tests for Bug Fix 1: score asymmetry on even attempts ---
# Before the fix, update_score gave +5 for "Too High" on even attempt numbers,
# rewarding the player for a wrong guess. All wrong guesses should deduct.


def test_score_too_high_odd_attempt():
    # Odd attempt (1): Too High should subtract 5 points
    result = update_score(0, "Too High", 1)
    assert result == -5, f"Expected -5 but got {result}"


def test_score_too_high_even_attempt():
    # Even attempt (2): Too High should STILL subtract 5 points (not add +5)
    # This is the core regression guard for the parity bug.
    result = update_score(0, "Too High", 2)
    assert result == -5, f"Expected -5 but got {result}"


def test_score_too_low_always_subtracts():
    # Too Low should always subtract 5 regardless of attempt number
    assert update_score(0, "Too Low", 1) == -5
    assert update_score(0, "Too Low", 2) == -5
    assert update_score(0, "Too Low", 10) == -5


def test_score_win_decreases_with_attempts():
    # Win score should decrease the longer the player takes, floor of 10
    early_win = update_score(0, "Win", 1)  # 100 - 10*(1+1) = 80
    late_win = update_score(0, "Win", 9)   # 100 - 10*(9+1) = 0 -> floor 10
    assert early_win == 80
    assert late_win == 10


# --- Tests for Bug Fix 2: out-of-range input not validated ---
# Before the fix, parse_guess accepted any integer even outside the game range,
# silently wasting an attempt with no feedback to the player.


def test_parse_guess_too_high_rejects():
    # 999 is above the Normal range of 1-100
    ok, value, err = parse_guess("999", low=1, high=100)
    assert ok is False
    assert value is None
    assert err is not None and "100" in err


def test_parse_guess_too_low_rejects():
    # 0 is below the minimum of 1
    ok, value, err = parse_guess("0", low=1, high=100)
    assert ok is False
    assert value is None
    assert err is not None


def test_parse_guess_boundary_low_accepts():
    # Exactly 1 should be valid in a 1-100 range
    ok, value, err = parse_guess("1", low=1, high=100)
    assert ok is True
    assert value == 1


def test_parse_guess_boundary_high_accepts():
    # Exactly 100 should be valid in a 1-100 range
    ok, value, err = parse_guess("100", low=1, high=100)
    assert ok is True
    assert value == 100


def test_parse_guess_no_range_accepts_any_int():
    # When no range is passed (legacy call), any integer is accepted
    ok, value, err = parse_guess("999")
    assert ok is True
    assert value == 999
