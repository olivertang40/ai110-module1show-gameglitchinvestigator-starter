# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agent Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

I used Claude Code in agent mode inside VS Code. I asked it to investigate the broken Streamlit guessing game, fix the bugs I noticed (the reversed Higher/Lower hints, the broken "New Game" button, and the secret number falling outside the difficulty range), refactor the core logic out of `app.py` into `logic_utils.py`, make the automated tests pass, and document the work in `README.md` and `reflection.md`.

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
| | | | | |
| | | | | |
| | | | | |

---

## Linting & Style (SF9)

> Document your use of AI for linting or code style improvements.

**Prompt used:**

```
<!-- Paste the prompt you gave the AI -->
```

**Linting output before:**

```
<!-- Paste relevant linter warnings/errors -->
```

**Changes applied:**

<!-- Describe what you changed based on the AI's suggestions -->

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
