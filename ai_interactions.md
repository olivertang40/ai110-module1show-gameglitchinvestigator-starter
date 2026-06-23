# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agent Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

I used Claude Code (an AI coding assistant in agent mode) inside VS Code. I asked it to investigate the broken Streamlit guessing game, fix the bugs I noticed (the reversed Higher/Lower hints, the broken "New Game" button, and the secret number falling outside the difficulty range), refactor the core logic out of `app.py` into `logic_utils.py`, make the automated tests pass, and document the work in `README.md` and `reflection.md`.

**What did the agent do?**

- Read `app.py`, `logic_utils.py`, and `tests/test_game_logic.py` and explained how Streamlit reruns and `st.session_state` worked.
- Fixed the reversed hint messages in `check_guess` (Too High → Go LOWER, Too Low → Go HIGHER) and removed a glitch that cast the secret to a string on even attempts.
- Rewrote the "New Game" handler to reset `status`, `score`, `history`, and the input box (not just `attempts`/`secret`), which is what actually unstuck the game.
- Added logic to regenerate the secret when difficulty changes so it stays inside the displayed range, and replaced the hard-coded "1 and 100" prompt with the real range.
- Moved `get_range_for_difficulty`, `parse_guess`, `check_guess`, and `update_score` into `logic_utils.py` and imported them in `app.py`.
- Updated the tests, ran `pytest` (3 passed) and `py_compile`, added `# FIX` comments, and wrote the README and reflection content.
- Staged the relevant files, wrote a detailed commit message, and pushed to `main`.

**What did you have to verify or fix manually?**

- I replayed the bugs in the running app after each fix to confirm the behavior actually changed (e.g., winning a game, clicking New Game, and submitting again).
- The agent edited the test file to unpack the new `(outcome, message)` tuple return value. I reviewed that change carefully to make sure it wasn't just bending the tests to pass, and confirmed it was the correct fix (plus it added "LOWER"/"HIGHER" assertions that guard the bug).
- When the agent was about to commit straight to `main`, I stopped it and asked which branch it was using before approving — I wanted to understand the Git workflow rather than commit blindly.
- I reviewed every diff before it was committed and pushed.

---

## Test Generation (SF7)

> Document how you used AI to help generate or improve tests.

| Edge Case | Prompt Used | AI-Suggested Test | Did It Pass? | Your Reasoning |
|-----------|-------------|-------------------|--------------|----------------|
| Score stays negative on even-numbered "Too High" attempt | "The score goes UP when I guess wrong on attempt 2. Generate a pytest case that would catch this bug — call update_score(0, 'Too High', 2) and assert the result is -5." | `assert update_score(0, "Too High", 2) == -5` in `test_score_too_high_even_attempt` | Yes — after removing the `% 2` branch | This test is the core regression guard. If anyone reintroduces the parity logic it fails immediately and the assert message explains why. |
| Out-of-range input rejected with a message | "parse_guess silently accepts 999 in a 1–100 game. Write a test that passes '999' with low=1, high=100 and asserts ok is False and the error mentions 100." | `ok, value, err = parse_guess("999", low=1, high=100); assert ok is False; assert "100" in err` | Yes | Directly reproduces the bug from the Bug Reproduction Logs table — same input, same expected vs. actual I wrote in Phase 1. |
| Boundary value low (1) accepted | "Add a test that confirms the lowest valid input is accepted, not rejected — parse_guess('1', 1, 100) should return ok=True." | `ok, value, err = parse_guess("1", low=1, high=100); assert ok is True; assert value == 1` | Yes | Fence-post case. The range check uses `< low` so value == low must be accepted; this test would catch an off-by-one if someone changed `<` to `<=`. |
| Boundary value high (100) accepted | "Same idea for the upper bound — parse_guess('100', 1, 100) should return ok=True." | `ok, value, err = parse_guess("100", low=1, high=100); assert ok is True; assert value == 100` | Yes | Mirrors the lower boundary test. Guards against `> high` accidentally becoming `>= high`. |
| No range passed — any integer accepted (legacy call) | "The old call site in the starter had no low/high args. Write a test that calls parse_guess('999') with no range and confirms it still returns ok=True so we don't break backward compatibility." | `ok, value, err = parse_guess("999"); assert ok is True; assert value == 999` | Yes | Ensures the optional-parameter design doesn't accidentally break any call site that omits the range. |
| Too Low on any attempt always subtracts | "Write a test that calls update_score with 'Too Low' on attempts 1, 2, and 10 and asserts each returns -5." | `assert update_score(0, "Too Low", 1) == -5` (repeated for 2 and 10) | Yes | Confirms the parity bug only affected "Too High" — Too Low was already correct, and this test locks that in. |

---

## Linting & Style (SF9)

> Document your use of AI for linting or code style improvements.

**Prompt used:**

```
Install flake8 and run it against logic_utils.py, app.py, and
tests/test_game_logic.py. Show me the raw output, then fix every
violation and show me a clean run. Explain each type of error you fix.
```

**Linting output before:**

```
app.py:57:80: E501 line too long (81 > 79 characters)
app.py:58:80: E501 line too long (82 > 79 characters)
app.py:98:80: E501 line too long (80 > 79 characters)
logic_utils.py:29:80: E501 line too long (80 > 79 characters)
logic_utils.py:30:80: E501 line too long (83 > 79 characters)
logic_utils.py:32:80: E501 line too long (85 > 79 characters)
logic_utils.py:33:80: E501 line too long (83 > 79 characters)
logic_utils.py:36:80: E501 line too long (82 > 79 characters)
logic_utils.py:67:80: E501 line too long (80 > 79 characters)
tests/test_game_logic.py:3:1: E302 expected 2 blank lines, found 1
tests/test_game_logic.py:8:1: E302 expected 2 blank lines, found 1
tests/test_game_logic.py:14:1: E302 expected 2 blank lines, found 1
tests/test_game_logic.py:23:80: E501 line too long (81 > 79 characters)
tests/test_game_logic.py:30:1: E302 expected 2 blank lines, found 1
tests/test_game_logic.py:34:80: E501 line too long (100 > 79 characters)
tests/test_game_logic.py:36:1: E302 expected 2 blank lines, found 1
tests/test_game_logic.py:42:1: E302 expected 2 blank lines, found 1
tests/test_game_logic.py:45:13: E221 multiple spaces before operator
tests/test_game_logic.py:45:80: E501 line too long (81 > 79 characters)
tests/test_game_logic.py:61:1: E302 expected 2 blank lines, found 1
tests/test_game_logic.py:68:1: E302 expected 2 blank lines, found 1
tests/test_game_logic.py:74:1: E302 expected 2 blank lines, found 1
tests/test_game_logic.py:80:1: E302 expected 2 blank lines, found 1
```

**Linting output after (clean run):**

```
$ python -m flake8 logic_utils.py app.py tests/test_game_logic.py
$
(no output — exit code 0)
```

**Changes applied:**

Three categories of violations were fixed:

- **E302 — missing blank lines before function definitions.** PEP 8 requires two blank lines between top-level functions. The test file had only one blank line between each `def`. Fixed by adding a second blank line before every top-level function definition in `tests/test_game_logic.py`.

- **E501 — lines exceeding 79 characters.** The main source was long `# FIX` inline comments in `logic_utils.py` and `app.py`. Fixed by rewrapping multi-sentence comments so each line stays within 79 characters. One long f-string return in `parse_guess` was split into a two-line assignment (`msg = ...; return False, None, msg`).

- **E221 — multiple spaces before an operator.** In `test_score_win_decreases_with_attempts`, the alignment padding (`early_win =` vs `late_win  =`) used an extra space to visually align the `=` signs. Removed the extra space to match PEP 8's single-space rule.

---

## Model Comparison (SF11)

> Compare two AI models on the same task.

**Task given to both models:**

<!-- Describe what you asked each model to do -->

| | Model A | Model B |
|-|---------|---------|
| **Model name** | | |
| **Response summary** | | |
| **More Pythonic?** | | |
| **Clearer explanation?** | | |

**Which did you prefer and why?**

<!-- Your conclusion -->
