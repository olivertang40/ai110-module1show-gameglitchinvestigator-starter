# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

When I first ran the game, it looked mostly normal and let me submit guesses, but several things were broken:

1. **Hints were reversed.** The `check_guess` function returned "Too High" for a guess above the secret, but paired it with the message "📈 Go HIGHER!" — the exact opposite of what a player needs. I guessed 60 when the secret was 42, got told to go *higher*, went to 80, and moved further from the answer.
2. **Cannot reset / start a new game.** After finishing a round (win or loss), pressing the "New Game" button did nothing — the game stayed stuck showing "You already won / Game over" and Submit no longer responded. The `status` field was never reset back to `"playing"`.
3. **Score rewards wrong guesses on even-numbered attempts.** When a player guesses too high on attempt 2, 4, 6, etc., `update_score` adds +5 points instead of subtracting them. A player can rack up positive score by deliberately guessing wrong on even turns.
4. **Out-of-range inputs are accepted silently.** Entering 999 in a Normal (1–100) game is accepted with no warning — it just says "Too High." There is no validation that the guess falls inside the stated range.
5. **String-cast glitch on even attempts (original starter code).** On even-numbered attempts the original code cast the secret to a string, so Python compared numbers as text (`"9" > "40"` is `True`), flipping the hint direction inconsistently between turns.

**Bug Reproduction Logs**

I played the game twice (once on Normal difficulty, once on Easy) and logged all reproducible bugs below. The "secret" value was read from the Developer Debug Info expander in the sidebar.

| Input Used | Expected Behavior | Actual Behavior | Console Error / Output |
|------------|-------------------|-----------------|------------------------|
| Guess of 60 when secret = 42 (Normal mode, attempt 1) | Outcome "Too High", hint tells me to go **LOWER** | Outcome is "Too High" but message displays "📈 Go HIGHER!" — hint direction is completely reversed, leading player away from the answer | none |
| Guess of 20 when secret = 42 (Normal mode, attempt 2) | Outcome "Too Low", hint tells me to go **HIGHER** | Outcome is "Too Low" and message correctly says "📈 Go HIGHER!" — but only because Too Low is not affected by the even-attempt score bug; the score drops -5 as expected here | none |
| Two consecutive "Too High" guesses: attempt 1 (odd) then attempt 2 (even), secret = 7 | Both wrong guesses should **decrease** score | Attempt 1 (odd): score drops -5 ✓. Attempt 2 (even): score *increases* +5 — player is rewarded for a second wrong guess | none |
| Guess of 999 when range is 1–100 (Normal mode) | Game should reject the input or display a warning that 999 is outside the valid range | Input accepted silently; treated as a normal "Too High" and counts as an attempt — wastes one of the player's limited guesses with no feedback | none |
| Click "New Game 🔁" after winning or running out of attempts | Game fully resets: new secret, cleared score/history/input, status back to "playing", Submit button works | "You already won / Game over" banner reappears immediately; Submit does nothing; input box retains old guess; player is permanently stuck until page is manually refreshed | none |
| Type "42.7" when secret = 42 | Decimal input should be rejected, or at minimum the player should see that it was rounded | Input is silently truncated to 42 (int), matches the secret, and triggers a win — player may not realise their decimal was modified | none |

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?

I used Kiro (an AI coding assistant in agent mode) inside VS Code. I had it read `app.py` and `logic_utils.py`, explain the code, find bugs, apply fixes, and run the tests with me reviewing every diff before accepting.

**Correct AI suggestion (verified true):**
- *What the AI suggested:* After I described the score going *up* after a wrong guess on attempt 2, the AI immediately pointed to the `attempt_number % 2 == 0` branch inside `update_score` in `logic_utils.py`. It explained that the branch was adding +5 on even attempts regardless of whether the outcome was correct, and suggested removing the parity check entirely so both "Too High" and "Too Low" always deduct 5 points.
- *Was it correct?* Yes, completely correct.
- *How I verified it:* I called `update_score(0, "Too High", 2)` directly in the terminal and confirmed it now returns -5 instead of +5. I also added `test_score_too_high_even_attempt` to the test suite as a permanent regression guard, and ran `pytest` to confirm 11/11 tests pass.

**Incorrect / misleading AI behavior (verified and caught):**
- *What the AI suggested:* When I first asked it to add range validation to `parse_guess`, the AI initially suggested raising a `ValueError` exception instead of returning the existing `(ok, value, error)` tuple pattern the function already used. This would have broken the call site in `app.py`, which unpacks three values and checks `ok` — it doesn't catch exceptions.
- *Was it correct?* Incorrect / misleading — the suggestion was technically a valid Python pattern but did not match the function's established return contract, so it would have crashed the Streamlit app on any out-of-range guess.
- *How I verified it:* I looked at how `app.py` calls `parse_guess` (`ok, guess_int, err = parse_guess(...)`) and saw it would throw an unhandled `ValueError`. I pointed this out to the AI, and it revised the suggestion to return `(False, None, error_message)` instead, which fit cleanly into the existing pattern. I then ran `parse_guess("999", 1, 100)` in the terminal and confirmed `ok=False` with a readable error message.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?

I applied a two-gate rule for every fix: first reproduce the bug with an exact input in the terminal or running app, then run `pytest` and confirm the new test targeting that specific bug passes alongside all existing tests. A fix only counted as done when both gates cleared — "looks right in the code" wasn't enough.

- Describe at least one test you ran (manual or using pytest) and what it showed you about your code.

For the score asymmetry bug I ran `python -m pytest tests/ -v` after adding `test_score_too_high_even_attempt`. The test calls `update_score(0, "Too High", 2)` and asserts the result is -5. Before the fix this test would have failed (result was +5); after removing the `attempt_number % 2 == 0` branch it passes. The test is intentionally narrow — it targets exactly the line that was wrong — so if anyone reintroduces the parity logic later, this test will immediately fail and explain why.

For the range validation bug I ran `parse_guess("999", 1, 100)` directly in the terminal and confirmed `ok=False` with the message "Please enter a number between 1 and 100." I then added four boundary tests (`test_parse_guess_too_high_rejects`, `test_parse_guess_boundary_low_accepts`, etc.) and ran `pytest` to confirm all 11 tests pass with zero failures.

Final full run: `python -m pytest tests/ -v` → **11 passed in 0.03s**.

- Did AI help you design or understand any tests? How?

Yes. I described the two bugs and asked the AI to suggest test cases that would have *caught* them before the fix. For the score bug it suggested testing both odd and even attempt numbers with the same outcome to show the asymmetry; for the range bug it suggested testing both boundary values (1 and 100) as well as values just outside the range (0 and 999) to cover the fence-post cases. I reviewed each suggested assertion before accepting it — the boundary acceptance tests in particular were something I might have skipped without the prompt.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

Streamlit re-runs your entire script from top to bottom every single time you interact with the page — click a button, type in a box, change a dropdown. So any normal variable resets to its starting value on every interaction, which is why the secret number kept "changing" — it was being regenerated on each rerun. `st.session_state` is a dictionary that survives those reruns, so it's where you store anything that must persist (the secret, score, attempts, game status). The bugs in this project taught me that the *order* of code matters too: the `New Game` button has to reset `status` back to `"playing"` before the guard `if status != "playing": st.stop()` runs, otherwise the script stops early and the rest of the page never executes. In short: reruns = the script restarts on every click; session_state = the memory that lets the game remember what happened before.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.

I want to keep the habit of verifying every fix two ways — reproducing the bug in the running app AND running `pytest` — before calling it done. Writing a small reproduction case first (exact input, expected vs. actual) made it obvious whether a change actually worked instead of just looking right.

- What is one thing you would do differently next time you work with AI on a coding task?

Next time I would read the AI's diffs more carefully before accepting them, and ask it to change only one thing at a time. A few times the AI wanted to "clean up" extra code or modify the test file, and I had to stop and check whether that was actually correct (for example, it edited the tests to match the tuple return value — I had to confirm that was the right call rather than blindly accepting it). I also rejected a commit-straight-to-main step until I understood whether it was the right Git workflow.

- In one or two sentences, describe how this project changed the way you think about AI generated code.

I no longer trust "production-ready" AI code at face value — the starter was full of confident, plausible-looking bugs. AI is a fast teammate for finding and fixing issues, but I'm the one who has to reproduce, test, and verify before anything is really fixed.
