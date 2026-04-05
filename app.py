import streamlit as st
import random

# --- 1. CONFIGURATION & STYLING ---
st.set_page_config(page_title="AI Math Tutor", page_icon="🎮")

# Custom CSS for a "Kid-Friendly" look
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stButton>button { width: 100%; border-radius: 20px; height: 3em; background-color: #4CAF50; color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. INITIALIZE GAME STATE ---
if 'level' not in st.session_state:
    st.session_state.level = 1
    st.session_state.xp = 0
    st.session_state.inventory = []
    st.session_state.history = []

def get_reward(level):
    rewards = {5: "🛡️ Wood Shield", 10: "🗡️ Stone Sword", 15: "🧥 Leather Armor", 20: "🦄 Magic Pony"}
    return rewards.get(level, None)

# --- 3. THE UI LAYOUT ---
st.title("🚀 Math Quest Adventure")
st.sidebar.header(f"Level {st.session_state.level}")
st.sidebar.progress(st.session_state.xp / 100)
st.sidebar.subheader("🎒 Your Inventory")
st.sidebar.write(", ".join(st.session_state.inventory) if st.session_state.inventory else "Empty")

# --- 4. GAMEPLAY LOGIC ---
st.subheader(f"Current Quest: Level {st.session_state.level}")

# Simple Math Generator (Increases difficulty with Level)
num1 = random.randint(1, st.session_state.level + 5)
num2 = random.randint(1, st.session_state.level + 2)
question = f"What is {num1} + {num2}?"
correct_ans = num1 + num2

ans = st.number_input(question, step=1, value=None)

if st.button("Check Answer"):
    if ans == correct_ans:
        st.balloons()
        st.success("✨ AMAZING! You got it right! +25 XP")
        st.session_state.xp += 25
        st.session_state.history.append(f"Level {st.session_state.level}: Success")
        
        if st.session_state.xp >= 100:
            st.session_state.level += 1
            st.session_state.xp = 0
            gift = get_reward(st.session_state.level)
            if gift:
                st.session_state.inventory.append(gift)
                st.info(f"🎁 UNLOCKED: {gift}!")
    else:
        st.error("Not quite! Try counting on your fingers or using blocks!")

# --- 5. PARENT REPORT CARD ---
with st.expander("📊 Parent Dashboard (Weekly Report)"):
    accuracy = len(st.session_state.history) # Simplified for demo
    st.write(f"**Current Standing:** Grade {1 if st.session_state.level < 10 else 2}")
    st.write(f"**Total Questions Solved:** {len(st.session_state.history)}")
    
    report_text = f"Math Progress Report\nLevel: {st.session_state.level}\nSolved: {len(st.session_state.history)}"
    st.download_button("Download Report", report_text, file_name="report.txt")