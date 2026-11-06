import os
import streamlit as st
from dotenv import load_dotenv
from google import genai

load_dotenv()
st.set_page_config(page_title="AI Escape Room — Version 1", page_icon="🗝️")
st.title("🗝️ AI Escape Room — Version 1")
st.caption("A simple LLM-powered library escape game")
INTRO = "You wake up in a locked library. You see a desk, bookshelf, painting, locked drawer, and a door with a four-digit keypad. Explore, find clues, solve puzzles, and escape. Type 'restart' to begin again."
SYSTEM_PROMPT = """You are the Game Master for a fictional library escape room. Objects: desk, bookshelf, painting, locked drawer, door. The bookshelf reveals drawer code 246. The desk note says to inspect the painting. The painting reveals final door code 7314. The drawer contains a brass key. Keep the story concise, do not invent objects or change codes, and do not claim the player escaped unless they enter 7314 for the door. Version 1 is a baseline and may be less reliable than a validated game engine."""

def ask_gemini(messages):
    key=os.getenv("GEMINI_API_KEY")
    if not key: return None
    try:
        client=genai.Client(api_key=key)
        history="\n".join(f"{m['role'].upper()}: {m['content']}" for m in messages[-12:])
        response=client.models.generate_content(model=os.getenv("GEMINI_MODEL","gemini-2.5-flash"), contents=SYSTEM_PROMPT+"\nConversation:\n"+history+"\nRespond to the latest player message.")
        return response.text
    except Exception as exc:
        return f"The AI service could not respond ({type(exc).__name__}). Try again."

if "messages" not in st.session_state: st.session_state.messages=[{"role":"assistant","content":INTRO}]
if "escaped" not in st.session_state: st.session_state.escaped=False
with st.sidebar:
    st.subheader("How to play")
    st.write("Try: examine the bookshelf, look at the desk, inspect the painting, or enter a code.")
    if not os.getenv("GEMINI_API_KEY"): st.warning("Add GEMINI_API_KEY to .env to enable Gemini. Built-in responses still work.")
    if st.button("Restart game"):
        st.session_state.messages=[{"role":"assistant","content":INTRO}]; st.session_state.escaped=False; st.rerun()
for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.markdown(m["content"])
user_text=st.chat_input("What do you want to do?")
if user_text:
    if user_text.strip().lower()=="restart":
        st.session_state.messages=[{"role":"assistant","content":INTRO}]; st.session_state.escaped=False; st.rerun()
    st.session_state.messages.append({"role":"user","content":user_text})
    t=user_text.lower()
    if "bookshelf" in t or "books" in t: answer="Three books have handwritten digits: 2, 4, and 6. This may be the drawer code."
    elif "desk" in t: answer="Under a paper on the desk, you find a note: 'A picture can reveal what words hide.'"
    elif "painting" in t or "picture" in t: answer="Behind the painting is the four-digit sequence 7314. Remember it for the door."
    elif "246" in t and "drawer" in t: answer="The drawer clicks open. Inside is a small brass key and a note about the picture."
    elif "7314" in t and "door" in t:
        answer="The keypad flashes green and the library door opens. You escaped! 🎉"; st.session_state.escaped=True
    else: answer=ask_gemini(st.session_state.messages) or "Try examining the desk, bookshelf, or painting. You can also try code 246 on the drawer or 7314 on the door."
    st.session_state.messages.append({"role":"assistant","content":answer}); st.rerun()
if st.session_state.escaped: st.success("Game complete — you escaped the library.")
