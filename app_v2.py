import os
import streamlit as st
from dotenv import load_dotenv
from google import genai
from game_logic import new_state,handle_action
load_dotenv()
st.set_page_config(page_title="AI Escape Room — Version 2",page_icon="🛡️")
st.title("🛡️ AI Escape Room — Version 2")
st.caption("Python validates actions; the AI only adds atmosphere.")
def narrate(action,result):
    key=os.getenv("GEMINI_API_KEY")
    if not key: return result
    try:
        client=genai.Client(api_key=key)
        prompt=f"You are a concise escape-room narrator. Player action: {action}. Trusted game-engine result: {result}. Rewrite that result in at most two atmospheric sentences. Do not change facts, add clues, reveal codes, invent items, or claim a different state. Return only narration."
        response=client.models.generate_content(model=os.getenv("GEMINI_MODEL","gemini-2.5-flash"),contents=prompt)
        return response.text or result
    except Exception: return result
if "game_state" not in st.session_state: st.session_state.game_state=new_state()
if "messages" not in st.session_state: st.session_state.messages=[{"role":"assistant","content":"You wake up in a locked library. Explore the desk, bookshelf, painting, drawer, and door. Find clues, open the drawer, then escape."}]
with st.sidebar:
    st.subheader("Game status"); s=st.session_state.game_state
    st.write("**Clues found:**",", ".join(s["clues_found"]) or "None yet")
    st.write("**Inventory:**",", ".join(s["inventory"]) or "Empty")
    st.write("**Puzzles solved:**",", ".join(s["puzzles_solved"]) or "None")
    st.write("**Door:**","Open" if s["door_unlocked"] else "Locked")
    if not os.getenv("GEMINI_API_KEY"): st.info("No API key found. Built-in narration is enabled.")
    if st.button("Restart game"):
        st.session_state.game_state=new_state(); st.session_state.messages=[{"role":"assistant","content":"The library resets. Examine the desk, bookshelf, painting, drawer, or door."}]; st.rerun()
for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.markdown(m["content"])
text=st.chat_input("What do you want to do?")
if text:
    st.session_state.messages.append({"role":"user","content":text})
    result,state=handle_action(text,st.session_state.game_state); st.session_state.game_state=state
    st.session_state.messages.append({"role":"assistant","content":narrate(text,result)}); st.rerun()
if st.session_state.game_state["escaped"]: st.success("Game complete — you escaped the library!")
