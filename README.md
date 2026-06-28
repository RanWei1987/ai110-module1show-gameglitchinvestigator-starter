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

- [V] Describe the game's purpose.
   - Guess the correct number based on the hints provided.
- [V] Detail which bugs you found.
   - 1. Clicking "New Game" did not reset the game;  
   - 2. The hints "Go HIGHER" and "Go LOWER" were opposite to the relation between the guessed value and the real answer.
- [V] Explain what fixes you applied.
   - Fixed the opposite hints and the secret-stringified-on-even-attempts convergence bug in check_guess.
   - Fixed the New Game button (the missing status = "playing" reset).
   - Refactored the logic into logic_utils.py so app.py is just app setup + input handling.
   - Added regression + unit tests in tests/ with pytest.ini and a conftest.py so pytest just works.

## 📸 Demo Walkthrough

Describe your fixed game in numbered steps so a reader can follow along without watching a video:
1. Select the difficulty level from "Easy", "Normal" and "Hard"  
1. User enters a guess of 40  
2. Game returns "Too Low"  
3. User enters a guess of 70 → "Too High"
4. Score updates correctly after each guess
5. Game ends after the correct guess, e.g. 60; or after exceeding the attempts allowed. The correct answer will be given so that you know how far you are from it. 

**Screenshot** *(optional)*: <!-- Insert a screenshot of your fixed, winning game here -->

## 🧪 Test Results

```
(codepath) rwei@EpiRan:~/CodePath/Week2/ai110-module1show-gameglitchinvestigator-starter$ pytest
============================================ test session starts =============================================
platform linux -- Python 3.14.5, pytest-9.1.1, pluggy-1.6.0 -- /home/rwei/miniforge3/envs/codepath/bin/python3.14
cachedir: .pytest_cache
rootdir: /home/rwei/CodePath/Week2/ai110-module1show-gameglitchinvestigator-starter
configfile: pytest.ini
testpaths: tests
plugins: anyio-4.13.0
collected 56 items

tests/test_game_logic.py::test_guess_below_secret_says_go_higher PASSED                                [  1%]
tests/test_game_logic.py::test_guess_above_secret_says_go_lower PASSED                                 [  3%]
tests/test_game_logic.py::test_correct_guess_wins PASSED                                               [  5%]
tests/test_game_logic.py::test_hint_direction_regression[12-2-Too High-LOWER] PASSED                   [  7%]
tests/test_game_logic.py::test_hint_direction_regression[13-2-Too High-LOWER] PASSED                   [  8%]
tests/test_game_logic.py::test_hint_direction_regression[1-2-Too Low-HIGHER] PASSED                    [ 10%]
tests/test_game_logic.py::test_hint_direction_regression[1-20-Too Low-HIGHER] PASSED                   [ 12%]
tests/test_game_logic.py::test_hint_direction_regression[20-1-Too High-LOWER] PASSED                   [ 14%]
tests/test_game_logic.py::test_hint_direction_regression[100-99-Too High-LOWER] PASSED                 [ 16%]
tests/test_game_logic.py::test_following_hints_always_reaches_the_secret[1] PASSED                     [ 17%]
tests/test_game_logic.py::test_following_hints_always_reaches_the_secret[2] PASSED                     [ 19%]
tests/test_game_logic.py::test_following_hints_always_reaches_the_secret[3] PASSED                     [ 21%]
tests/test_game_logic.py::test_following_hints_always_reaches_the_secret[4] PASSED                     [ 23%]
tests/test_game_logic.py::test_following_hints_always_reaches_the_secret[5] PASSED                     [ 25%]
tests/test_game_logic.py::test_following_hints_always_reaches_the_secret[6] PASSED                     [ 26%]
tests/test_game_logic.py::test_following_hints_always_reaches_the_secret[7] PASSED                     [ 28%]
tests/test_game_logic.py::test_following_hints_always_reaches_the_secret[8] PASSED                     [ 30%]
tests/test_game_logic.py::test_following_hints_always_reaches_the_secret[9] PASSED                     [ 32%]
tests/test_game_logic.py::test_following_hints_always_reaches_the_secret[10] PASSED                    [ 33%]
tests/test_game_logic.py::test_following_hints_always_reaches_the_secret[11] PASSED                    [ 35%]
tests/test_game_logic.py::test_following_hints_always_reaches_the_secret[12] PASSED                    [ 37%]
tests/test_game_logic.py::test_following_hints_always_reaches_the_secret[13] PASSED                    [ 39%]
tests/test_game_logic.py::test_following_hints_always_reaches_the_secret[14] PASSED                    [ 41%]
tests/test_game_logic.py::test_following_hints_always_reaches_the_secret[15] PASSED                    [ 42%]
tests/test_game_logic.py::test_following_hints_always_reaches_the_secret[16] PASSED                    [ 44%]
tests/test_game_logic.py::test_following_hints_always_reaches_the_secret[17] PASSED                    [ 46%]
tests/test_game_logic.py::test_following_hints_always_reaches_the_secret[18] PASSED                    [ 48%]
tests/test_game_logic.py::test_following_hints_always_reaches_the_secret[19] PASSED                    [ 50%]
tests/test_game_logic.py::test_following_hints_always_reaches_the_secret[20] PASSED                    [ 51%]
tests/test_game_logic.py::test_new_game_resets_status_to_playing PASSED                                [ 53%]
tests/test_game_logic.py::test_new_game_clears_score_history_and_attempts PASSED                       [ 55%]
tests/test_game_logic.py::test_new_game_returns_all_tracked_keys PASSED                                [ 57%]
tests/test_game_logic.py::test_new_game_secret_respects_difficulty_range[Easy] PASSED                  [ 58%]
tests/test_game_logic.py::test_new_game_secret_respects_difficulty_range[Normal] PASSED                [ 60%]
tests/test_game_logic.py::test_new_game_secret_respects_difficulty_range[Hard] PASSED                  [ 62%]
tests/test_game_logic.py::test_new_game_restarts_a_finished_game PASSED                                [ 64%]
tests/test_logic_functions.py::test_parse_guess_valid_inputs[42-expected0] PASSED                      [ 66%]
tests/test_logic_functions.py::test_parse_guess_valid_inputs[0-expected1] PASSED                       [ 67%]
tests/test_logic_functions.py::test_parse_guess_valid_inputs[-5-expected2] PASSED                      [ 69%]
tests/test_logic_functions.py::test_parse_guess_valid_inputs[ 7 -expected3] PASSED                     [ 71%]
tests/test_logic_functions.py::test_parse_guess_valid_inputs[3.9-expected4] PASSED                     [ 73%]
tests/test_logic_functions.py::test_parse_guess_valid_inputs[-3.9-expected5] PASSED                    [ 75%]
tests/test_logic_functions.py::test_parse_guess_missing_input[None] PASSED                             [ 76%]
tests/test_logic_functions.py::test_parse_guess_missing_input[] PASSED                                 [ 78%]
tests/test_logic_functions.py::test_parse_guess_non_numeric[abc] PASSED                                [ 80%]
tests/test_logic_functions.py::test_parse_guess_non_numeric[1,000] PASSED                              [ 82%]
tests/test_logic_functions.py::test_parse_guess_non_numeric[twelve] PASSED                             [ 83%]
tests/test_logic_functions.py::test_parse_guess_non_numeric[  ] PASSED                                 [ 85%]
tests/test_logic_functions.py::test_parse_guess_non_numeric[1.2.3] PASSED                              [ 87%]
tests/test_logic_functions.py::test_win_awards_points_based_on_attempt PASSED                          [ 89%]
tests/test_logic_functions.py::test_win_adds_to_existing_score PASSED                                  [ 91%]
tests/test_logic_functions.py::test_win_points_have_a_floor_of_10 PASSED                               [ 92%]
tests/test_logic_functions.py::test_too_low_loses_5_points PASSED                                      [ 94%]
tests/test_logic_functions.py::test_unknown_outcome_leaves_score_unchanged PASSED                      [ 96%]
tests/test_logic_functions.py::test_too_high_gains_5_on_even_attempt PASSED                            [ 98%]
tests/test_logic_functions.py::test_too_high_loses_5_on_odd_attempt PASSED                             [100%]

============================================= 56 passed in 0.06s =============================================
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
