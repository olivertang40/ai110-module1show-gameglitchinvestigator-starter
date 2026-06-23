def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 50
    return 1, 100


def parse_guess(raw: str, low: int = None, high: int = None):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None or raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    # FIX: Added range validation in collaboration with AI.
    # I identified the bug (out-of-range inputs silently accepted, wasting an
    # attempt with no feedback), and AI suggested making low/high optional
    # parameters so existing callers without range info still work.
    # Verified: parse_guess("999", 1, 100) returns ok=False; pytest clean.
    if low is not None and high is not None:
        if value < low or value > high:
            msg = f"Please enter a number between {low} and {high}."
            return False, None, msg

    return True, value, None


def check_guess(guess, secret):
    """
    Compare guess to secret and return (outcome, message).

    outcome examples: "Win", "Too High", "Too Low"
    """
    # FIX: The original hints were reversed ("Too High" told the player to go
    # HIGHER). AI flagged the swap; messages now match the outcome direction.
    if guess == secret:
        return "Win", "🎉 Correct!"
    if guess > secret:
        return "Too High", "📉 Go LOWER!"
    return "Too Low", "📈 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    if outcome == "Win":
        points = 100 - 10 * (attempt_number + 1)
        if points < 10:
            points = 10
        return current_score + points

    # FIX: Removed parity-based scoring in collaboration with AI.
    # I spotted the asymmetry by watching the score go UP after a wrong guess
    # on attempt 2. AI confirmed the `attempt_number % 2 == 0` branch was the
    # cause and suggested removing it so both wrong outcomes subtract 5.
    # Verified: update_score(0, "Too High", 2) now returns -5; pytest clean.
    if outcome == "Too High":
        return current_score - 5

    if outcome == "Too Low":
        return current_score - 5

    return current_score
