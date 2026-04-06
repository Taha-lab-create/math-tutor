import streamlit as st
import random

# --- 1. SET THE ADVENTURE THEME ---
st.set_page_config(page_title="Math Quest Adventure", page_icon="⚔️", layout="centered")

# Determine World Theme based on Level
def get_world_style(level):
    if level <= 10:
        return {"name": "🌲 The Green Forest", "color": "#D5F5E3", "text": "#186A3B"}
    elif level <= 20:
        return {"name": "🌊 The Blue Ocean", "color": "#D6EAF8", "text": "#1B4F72"}
    else:
        return {"name": "🌌 The Starry Galaxy", "color": "#EBDEF0", "text": "#4A235A"}

# --- 2. SESSION STATE ---
if 'level' not in st.session_state:
    st.session_state.level = 1
    st.session_state.xp = 0
    st.session_state.inventory = []
    st.session_state.num1 = random.randint(1, 5)
    st.session_state.num2 = random.randint(1, 5)
    st.session_state.input_key = 0

world = get_world_style(st.session_state.level)

# --- 3. GIANT VISUAL UI (CSS) ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: {world['color']}; }}
    .world-title {{ font-size: 50px !important; color: {world['text']}; text-align: center; font-weight: 900; text-shadow: 2px 2px #fff; }}
    .math-card {{ background: white; padding: 30px; border-radius: 30px; border: 5px solid {world['text']}; text-align: center; }}
    .quest-text {{ font-size: 60px !important; font-weight: bold; color: #2C3E50; }}
    .trophy-box {{ background: #FEF9E7; border: 3px dashed #F1C40F; padding: 15px; border-radius: 20px; text-align: center; display: inline-block; margin: 10px; width: 100px; }}
    .stButton>button {{ height: 100px; font-size: 30px !important; border-radius: 50px; background-color: {world['text']}; color: white; border: 4px solid white; }}
    </style>
    """, unsafe_allow_html=True)

# --- 4. GAME CONTENT ---
st.markdown(f'<p class="world-title">{world["name"]}</p>', unsafe_allow_html=True)

# Progress Map
cols = st.columns(10)
for i in range(10):
    with cols[i]:
        if st.session_state.level % 10 > i or st.session_state.level % 10 == 0:
            st.markdown("🟡") # Completed step
        elif st.session_state.level % 10 == i + 1:
            st.markdown("🏃") # Current position
        else:
            st.markdown("⚪") # Future step

st.markdown("---")

# The Challenge Area
with st.container():
    st.markdown(f'<div class="math-card">', unsafe_allow_html=True)
    st.markdown(f'<p class="quest-text">{st.session_state.num1} + {st.session_state.num2}</p>', unsafe_allow_html=True)
    ans = st.number_input("Write your answer:", step=1, value=None, key=f"ans_{st.session_state.input_key}")
    st.markdown('</div>', unsafe_allow_html=True)

st.write("")
if st.button("CHECK MY MAGIC ANSWER! ✨"):
    if ans is not None:
        if ans == st.session_state.num1 + st.session_state.num2:
            st.balloons()
            # Play a "Success" sound using HTML
            st.markdown('<audio autoplay><source src="https://assets.mixkit.co/active_storage/sfx/2013/2013-preview.mp3" type="audio/mpeg"></audio>', unsafe_allow_html=True)
            
            st.session_state.xp += 25
            if st.session_state.xp >= 100:
                st.session_state.level += 1
                st.session_state.xp = 0
                # Give a big visual reward
                rewards = {2: "🛡️", 5: "🗡️", 8: "👟", 10: "💎"}
                if st.session_state.level in rewards:
                    st.session_state.inventory.append(rewards[st.session_state.level])
            
            st.session_state.num1 = random.randint(1, st.session_state.level + 4)
            st.session_state.num2 = random.randint(1, st.session_state.level + 2)
            st.session_state.input_key += 1
            st.rerun()
        else:
            st.markdown('<audio autoplay><source src="https://assets.mixkit.co/active_storage/sfx/2571/2571-preview.mp3" type="audio/mpeg"></audio>', unsafe_allow_html=True)
            st.error("Try again, Brave Explorer!")

# --- 5. THE TROPHY ROOM (The "Earned" Section) ---
st.write("### 🏆 Your Treasure Chest")
if st.session_state.inventory:
    item_cols = st.columns(len(st.session_state.inventory) + 1)
    for idx, item in enumerate(st.session_state.inventory):
        with item_cols[idx]:
            st.markdown(f'<div class="trophy-box"><span style="font-size:40px;">{item}</span><br><small>Level {list({2:"Shield", 5:"Sword", 8:"Boots", 10:"Gem"}.keys())[idx]}</small></div>', unsafe_allow_html=True)
else:
    st.info("Solve 4 questions to earn your first Treasure! 📦")
