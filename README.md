# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

**Game's purpose:** A simple Streamlit number-guessing game. The app picks a secret number within a range that depends on the difficulty (Easy 1–20, Normal 1–100, Hard 1–50). The player submits guesses, gets "Too High / Too Low" hints, earns a score, and has a limited number of attempts to win.

**Bugs I found:**
- **Reversed hints.** "Too High" told the player to "Go HIGHER" (and "Too Low" → "Go LOWER") — the hint direction was backwards.
- **Hints flipped on even attempts.** The secret was cast to a string on even-numbered attempts, so comparisons happened as text (e.g. `"9" > "40"` is `True`), making the direction inconsistent turn to turn.
- **New Game didn't work.** It reset `attempts`/`secret` but never reset `status`, so after a win/loss the guard `st.stop()` ran first and Submit did nothing. The input box also kept the old value, and score/history weren't cleared.
- **Secret could fall outside the range.** The secret was generated once and never regenerated when difficulty changed, so an Easy (1–20) game could keep a secret of 91 from a previous Normal game — making it impossible to win.
- **Hard-coded range text.** The prompt always said "between 1 and 100" regardless of the selected difficulty.

**Fixes I applied:**
- Swapped the hint messages so they match the outcome (Too High → 📉 Go LOWER, Too Low → 📈 Go HIGHER).
- Removed the string-cast glitch so the secret stays an int every turn.
- Made New Game a full reset: `status` → `playing`, plus `score`, `history`, attempts, a new secret, and a cleared input box.
- Regenerate the secret (and reset the round) whenever difficulty changes, so the secret always stays inside the displayed range.
- Replaced the hard-coded prompt with the actual `low`/`high` range.
- Refactored the core logic (`get_range_for_difficulty`, `parse_guess`, `check_guess`, `update_score`) out of `app.py` into `logic_utils.py`, and updated the tests to match the `(outcome, message)` return value.

## 📸 Demo Walkthrough

A sample game on **Normal** difficulty (range 1–100, 8 attempts) where the secret number is **63**:

1. The page shows "Guess a number between 1 and 100. Attempts left: 8".
2. User enters a guess of **40** and clicks **Submit Guess 🚀** → game returns **"Too Low → 📈 Go HIGHER!"**.
3. User enters **80** → **"Too High → 📉 Go LOWER!"**. (Hints now point the correct direction.)
4. User enters **60** → **"Too Low → 📈 Go HIGHER!"**. The score updates after each guess and "Attempts left" decreases.
5. User enters **63** → **"🎉 Correct!"**, balloons appear, and the win message shows the secret and final score. The game status becomes "won".
6. User clicks **New Game 🔁** → the input box clears, a fresh secret is chosen in range, score/history reset, and the board is playable again.
7. (Bonus) User switches difficulty to **Easy** mid-game → a fresh game starts in the 1–20 range and the prompt updates to "between 1 and 20", so the secret can never be out of range.

**Screenshot** *(optional)*: <!-- Insert a screenshot of your fixed, winning game here -->

## 🧪 Test Results

```
$ python -m pytest tests/ -v
============================= test session starts =============================
platform win32 -- Python 3.11.9, pytest-9.0.3, pluggy-1.6.0
rootdir: ...\ai110-module1show-gameglitchinvestigator-starter
collected 12 items

tests/test_game_logic.py::test_winning_guess PASSED                      [  8%]
tests/test_game_logic.py::test_guess_too_high PASSED                     [ 16%]
tests/test_game_logic.py::test_guess_too_low PASSED                      [ 25%]
tests/test_game_logic.py::test_score_too_high_odd_attempt PASSED         [ 33%]
tests/test_game_logic.py::test_score_too_high_even_attempt PASSED        [ 41%]
tests/test_game_logic.py::test_score_too_low_always_subtracts PASSED     [ 50%]
tests/test_game_logic.py::test_score_win_decreases_with_attempts PASSED  [ 58%]
tests/test_game_logic.py::test_parse_guess_too_high_rejects PASSED       [ 66%]
tests/test_game_logic.py::test_parse_guess_too_low_rejects PASSED        [ 75%]
tests/test_game_logic.py::test_parse_guess_boundary_low_accepts PASSED   [ 83%]
tests/test_game_logic.py::test_parse_guess_boundary_high_accepts PASSED  [ 91%]
tests/test_game_logic.py::test_parse_guess_no_range_accepts_any_int PASSED [100%]

============================== 12 passed in 0.09s ==============================
```

The original 3 starter tests cover correct win detection and hint direction. The 9 new tests added in Phase 2/3 guard both fixed bugs: 4 tests for the score-asymmetry fix (parity bug on even attempts) and 5 tests for the range-validation fix (boundary values, out-of-range rejection, legacy no-range call).

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
