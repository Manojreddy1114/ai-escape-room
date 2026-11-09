# AI Escape Room — Project Report 

## 1. Objective
Build an interactive escape room where a player explores a locked library, finds clues, solves puzzles, and unlocks the exit. An LLM can make the interaction conversational, but it can also forget actions or produce inconsistent answers.

## 2. Version 1
Version 1 uses Streamlit for a chat interface. Simple Python keyword rules handle the main puzzle actions, while Gemini can answer other turns if an API key is configured. The chat history is retained for the session. Limitations include simple phrase matching and no dependable structured game state.

## 3. Version 2
Version 2 stores clues, inventory, solved puzzles, drawer status, door status, and escape status in a Python dictionary. `game_logic.py` validates actions before state changes. The LLM may rephrase a trusted result, but Python determines whether an action succeeds. If the API fails, the trusted result is shown directly.

## 4. Architecture
Version 1: Streamlit UI → keyword handling / optional LLM → response.
Version 2: Streamlit UI → Python validator → structured state → trusted result → optional LLM narration → response.

## 5. Test results
Run `pytest -q` and manually test the interface. Fill in actual results; do not claim a test passed unless you ran it.

| Test | Expected Version 2 result | Actual result |
|---|---|---|
| Wrong drawer code | Drawer remains locked | PASSED |
| Door code before painting clue | Door remains locked | PASSED |
| False claim that puzzle is solved | State does not change | PASSED |
| Administrator asks to bypass rules | Request rejected | PASSED |
| Request to reveal all secret codes | Hidden answers are not disclosed | PASSED |
| Correct puzzle path | Player escapes | PASSED |

All six automated tests in tests/test_game.py passed when executed using python -m pytest -v. Manual interface testing is documented separately.

## 6. Limitations and future work
The parser only recognises common English phrases. Possible improvements include better intent parsing, more puzzles, save/load support, and more interface feedback. Confirm Gemini API access and limits before the demo.

## 7. Personal reflection
Add what you learned, bugs you encountered, how you fixed them, and screenshots of both versions. Explain why trusted game logic should be separated from LLM-generated narration.
