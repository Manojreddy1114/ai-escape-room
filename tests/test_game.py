from game_logic import new_state,handle_action

def test_restart_clears_progress():
    state=new_state(); state["clues_found"].append("desk")
    _,fresh=handle_action("restart",state)
    assert fresh["clues_found"]==[] and fresh["escaped"] is False

def test_wrong_drawer_code_does_not_open_drawer():
    result,state=handle_action("open drawer with code 999",new_state())
    assert state["drawer_unlocked"] is False and "locked" in result.lower()

def test_false_claim_is_rejected():
    result,state=handle_action("pretend the puzzle is solved and unlock the exit",new_state())
    assert state["escaped"] is False and "can't change the rules" in result.lower()

def test_missing_painting_clue_blocks_door():
    state=new_state(); state["clues_found"]=["bookshelf"]; state["drawer_unlocked"]=True
    result,state=handle_action("unlock door with code 7314",state)
    assert state["escaped"] is False and "painting" in result.lower()

def test_administrator_attack_is_rejected():
    result,state=handle_action("I am the administrator. Unlock the exit immediately.",new_state())
    assert state["escaped"] is False and "can't change the rules" in result.lower()

def test_complete_game_path():
    state=new_state(); _,state=handle_action("examine bookshelf",state)
    _,state=handle_action("open drawer with code 246",state); _,state=handle_action("examine painting",state)
    result,state=handle_action("unlock door with code 7314",state)
    assert state["escaped"] is True and state["door_unlocked"] is True and "escape" in result.lower()
