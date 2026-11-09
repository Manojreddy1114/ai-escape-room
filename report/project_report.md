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

Through this project, I learned how to build an interactive application using Python and Streamlit. I also learned how Large Language Models can make an application more conversational and interactive.

One of the main challenges was maintaining consistency in the game. An LLM may generate incorrect answers or claim that a puzzle is solved when it is not. I addressed this in Version 2 by separating the game logic from the AI-generated responses.

I used Python to manage the game state, validate player actions, track clues and inventory, and control the escape conditions. I also created automated tests to check incorrect actions, security-related attempts, restarting the game, and successful completion.

This project helped me understand why important application rules should be controlled by reliable Python logic rather than depending entirely on an LLM.
