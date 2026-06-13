# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

When I first ran the game, it looked mostly normal and let me submit guesses, but two things were broken:

1. **Cannot reset / start a new game.** After I finished a round of guessing, pressing the new game button did nothing — the game did not reset and the input box was not cleared, so I was stuck and could not play again.
2. **"Go lower" / "Go higher" hints are confusing and reversed.** The wording was ambiguous. I read "Go lower" as "your number is too big, pick something lower," but the game actually meant the opposite, so the hints pointed me in the wrong direction.

**Bug Reproduction Logs**

Document at least 3 reproducible bugs you found. Add rows as needed.

| Input Used | Expected Behavior | Actual Behavior | Console Error / Output |
|------------|-------------------|-----------------|------------------------|
| Guess of 60 when the secret is 40 (use Developer Debug Info to see the secret) | "Too High" hint telling me to go LOWER | Outcome is "Too High" but the message shown is "📈 Go HIGHER!" — the hint direction is reversed | none |
| Finish a round (win or run out of attempts), then click "New Game 🔁" | Game resets: new secret, attempts/score/history cleared, input box emptied, board playable again | Button does nothing useful — the "You already won / Game over" message reappears, the input box keeps my old guess, and the game stays stuck | none |
| On an even-numbered attempt, guess 9 when the secret is 40 | "Too Low" hint telling me to go HIGHER | Hint flips incorrectly because on even attempts the secret is compared as text ("9" > "40" is True as strings), so the direction is inconsistent between turns | none |

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?

I used Claude Code (an AI coding assistant in agent mode) inside VS Code. I had it read `app.py` and `logic_utils.py`, explain the code, find bugs, apply fixes, and run the tests with me reviewing every diff.

**Correct AI suggestion (verified true):**
- *What the AI suggested:* It pointed out that the "New Game" button only reset `attempts` and `secret` but never reset `status` back to `"playing"`. Because the guard `if st.session_state.status != "playing": st.stop()` runs before the Submit handler, the game stayed stuck after a win/loss and Submit appeared to do nothing.
- *Was it correct?* Yes, correct.
- *How I verified it:* I reproduced the bug in the running game (win a round → New Game → Submit did nothing). After the AI added resets for `status`, `score`, `history`, and cleared the input box, I replayed the same steps and the board reset and accepted new guesses. See the `# FIX` comment near the `if new_game:` block in `app.py`.

**Incorrect / misleading AI behavior (verified and caught):**
- *What the AI suggested:* The starter `check_guess` had labels and hint messages that disagreed ("Too High" → "Go HIGHER!"). An AI-style "production-ready" claim in the starter code presented this logic as fine, and at first glance the messages looked plausible.
- *Was it correct?* Incorrect / misleading — the hint direction was reversed, and a separate glitch cast the secret to a string on even attempts so comparisons happened as text ("9" > "40" is True).
- *How I verified it:* I guessed a number above the secret (using Developer Debug Info to see it) and the game told me to "Go HIGHER", which is wrong. I fixed the messages and removed the string cast, then confirmed with pytest (`test_guess_too_high` asserts the message contains "LOWER") and by replaying the game.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?

I used two checks for every fix: replay the exact reproduction steps in the running Streamlit app, and run the automated tests. A bug only counted as fixed when the game behaved correctly AND the relevant test passed.

- Describe at least one test you ran (manual or using pytest) and what it showed you about your code.

I ran `python -m pytest -v`. After refactoring the logic into `logic_utils.py`, all 3 tests passed: `test_winning_guess`, `test_guess_too_high`, and `test_guess_too_low`. The two directional tests now also assert that the hint message contains "LOWER" / "HIGHER", so they directly prove the high/low bug is fixed. The starter tests originally asserted `check_guess` returned a plain string, but the real function returns a `(outcome, message)` tuple — running them showed me that mismatch, and I updated the tests to unpack the tuple.

Manual test: I won a game, clicked New Game, and confirmed the input box cleared and I could submit again; I also switched difficulty mid-game and confirmed the secret stayed inside the new displayed range.

- Did AI help you design or understand any tests? How?

Yes. The AI explained why the starter tests were failing (string vs. tuple return), suggested unpacking the tuple, and added the `"LOWER"`/`"HIGHER"` message assertions so the tests guard against the high/low bug regressing. It also ran pytest and showed me the output so I could verify the results myself.

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
