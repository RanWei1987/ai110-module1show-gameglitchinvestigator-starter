# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
It is a guesser game. The gamer types in a number and the game gives hint if this input is larger or smaller than the correct answer. The user adjusts the guess accordingly and the goal is to get the correct within the number of attempts allowed.   

- List at least two concrete bugs you noticed at the start  
The hints were backwards.  
Button "New Game" did not start a new game.

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
|guess of 60|"Go HIGHER!" hint|"Go LOWER!" hint shown|none|
|click "New Game"|new game started|still at the old game|none|
|select difficulty as "Easy"|final answer is between 1 and 20|The final answer is 51|none|

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
Claude
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
  - Fix the problem that clicking "New Game" button would not reset the game.  
The AI suggested: 
```
Root cause: The game tracks five session-state values (secret, attempts, score, status, history), but the New Game handler only reset two of them. Critically, it never reset status. After a game ends, status is "won" or "lost", and the script has an early guard:


if st.session_state.status != "playing":
    ...
    st.stop()
Because status was left as "won"/"lost", every rerun after clicking New Game hit st.stop() immediately and halted before a new game could be played. Secondary issues: score and history carried over, and the secret was hardcoded to random.randint(1, 100) instead of respecting the selected difficulty range.

The fix: I centralized the reset into a single pure helper, make_new_game_state(low, high) in logic_utils.py, which returns all five values reset together — with status set back to "playing" and the secret drawn from the active difficulty's (low, high) range. The button handler in app.py now applies that state:


if new_game:
    for key, value in make_new_game_state(low, high).items():
        st.session_state[key] = value
    st.success("New game started.")
    st.rerun()
Setting status = "playing" is what actually unblocks the st.stop() guard, so the fresh game runs.

Why this approach: Putting the reset in one helper means there's a single source of truth for "what a new game looks like," it respects difficulty, and — unlike inline Streamlit code — it's unit-testable. That let me add regression tests (tests/test_game_logic.py) verifying a new game resets status to "playing", clears score/history/attempts, and keeps the secret within the difficulty range. 
```
The suggestion was verified by applying the revisions, refreshing the game app and clicking the New Game after one round of game ends or during the game.  
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).  
  - The AI did not give incorrect suggestions, but it did give a solution that only partially solved the problem and hence requires further investigation and discussion.  
  - When fixing the problem of opposite hints being given during the guess, I first suspected the logic of check_guess() was wrong and labeled it as "CRIME SCENE" to direct the AI to the problematic code block. However, after its fixation, though most times the app runs properly, sometimes the guess fell into the loop of "GO HIGHER" for value of a and then "GO LOWER" for value a+1. So I described this problem to AI and asked to find out potential causes. AI successfully identified the bug and fixed it after my review.  
---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?   
  - Repeat the test that originaly led to incorrect behavior of the app.   
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.  
  - Selected Difficulty level Easy and did one round of guess. See if I can find the correct answer based on following the hint.  
- Did AI help you design or understand any tests? How?  
  - Yes. For testing the check_guess(), it explains to me what the test input is and what the expected output value is, which is defined in the assert clause.  
---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?  
  - Streamlit re-runs your entire script from top to bottom every time the user interacts with the page — typing, clicking a button, or toggling something. Because of this, normal variables are recreated and forgotten on each rerun, so they can't remember anything between interactions. Session state solves this: it's a per-session storage area that persists across reruns, where you keep the things your app needs to remember. The usual pattern is to set a value only the first time and then read or update it on later reruns. This is exactly why our reset bug happened — a leftover value persisted across reruns and kept the game in its finished state until we explicitly cleared it.
---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - Label the potentially problematic code block to direct the AI to focus on it. 
- What is one thing you would do differently next time you work with AI on a coding task?
  - I did not notice there had been a test folder setup for the pytest already. The AI created a different "tests" folder with the pytest scripts and settings and I had to ask AI to move the contents to the "test" folder afterhand. Next time I will review the file structure before asking AI to generate new a branch/folder/file.
- In one or two sentences, describe how this project changed the way you think about AI generated code.
  - Before, I first thought AI was like a wishing well — you tell what you need and the AI generates the code for you, then thought it should be a tool whose power would be unleashed using prompt engineering skills. But now it seems it is something in the middle — use natural language, but a clear understanding of project structure and code functions is needed, and requires skills to direct the thinking process of the AI.  
