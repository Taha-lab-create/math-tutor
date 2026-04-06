import streamlit as st
import random

# --- 1. THE "GAME ENGINE" STYLING ---
st.set_page_config(page_title="Math Galaxy Quest", page_icon="🚀", layout="wide")

st.markdown("""
    <style>
    /* Background & Global Font */
    .stApp {
        background: #0f172a;
        color: #f8fafc;
        font-family: 'Comic Sans MS', cursive, sans-serif;
    }
    
    /* Center the Main Content */
    .main-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }

    /* The Math Card - High Finish */
    .math-card {
        background: rgba(30, 41, 59, 0.7);
        border: 4px solid #38bdf8;
        border-radius: 40px;
        padding: 40px;
        width: 350px;
        text-align: right;
        box-shadow: 0 20px 50px rgba(0,0,0,0.5), 0 0 20px rgba(56, 189, 248, 0.2);
        margin-bottom: 20px;
    }
    .num-display { font-size: 110px; font-weight: 900; line-height: 1; }
    .op-display { font-size: 70px; color: #fb7185; float: left; margin-top: 20px; }
    .math-line { border-bottom: 10px solid #f8fafc; border-radius: 10px; margin: 15px 0; }

    /* Button & Input Polish */
    div[data-testid="stForm"] { border: none !important; padding: 0 !important; }
    .stButton>button {
        width: 100% !important;
        height: 90px !important;
        background: linear-gradient(135deg, #38bdf8 0%, #2563eb 100%) !important;
        color: white !important;
        font-size: 32px !important;
        border-radius: 25px !important;
        border: 4px solid #ffffff !important;
        box-shadow: 0 10px 20px rgba(0,0,0,0.3);
    }
    
    /* Feedback Messages */
    .success-text { font-size: 40px; color: #4ade80; text-align: center; font-weight: bold; }
    .error-text { font-size: 30px; color: #fb7185; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. STATE MANAGEMENT ---
if 'level' not in st.session_state:
    st.session_state.update({
        'level': 1, 'xp': 0, 'inventory': [],
        'num1': random.randint(1, 5), 'num2': random.randint(1, 5),
        'input_key': 0, 'last_result': None
    })

# --- 3. SIDEBAR (The Mission Map) ---
with st.sidebar:
    st.title("👨‍🚀 Mission Log")
    worlds = [("🌲 Forest", 1), ("🌊 Ocean", 5), ("🌋 Volcano", 10), ("🚀 Space", 15)]
    for name, start in worlds:
        color = "🟢" if st.session_state.level >= start else "⚪"
        st.markdown(f"### {color} {name}")
    
    st.markdown("---")
    st.write(f"### ⭐ XP: {st.session_state.xp}")
    st.write(f"### 🎒 Loot: {' '.join(st.session_state.inventory) if st.session_state.inventory else '???'}")

# --- 4. THE MAIN QUEST ---
st.markdown(f"<h1 style='text-align: center; color: #38bdf8;'>Quest Level {st.session_state.level}</h1>", unsafe_allow_html=True)

# Visual Cue: Progress to next level
progress_val = st.session_state.xp / 100
st.write("Progress to next Reward:")
st.progress(progress_val)

col1, col2, col3 = st.columns([1, 1.2, 1])

with col2:
    # THE MATH CARD
    st.markdown(f"""
        <div class="math-card">
            <div class="num-display" style="color: #fb7185;">{st.session_state.num1}</div>
            <div class="op-display">+</div>
            <div class="num-display" style="color: #38bdf8;">{st.session_state.num2}</div>
            <div class="math-line"></div>
        </div>
        """, unsafe_allow_html=True)

    # THE FORM (Fixes Enter to Submit)
    with st.form(key=f"math_form_{st.session_state.input_key}", clear_on_submit=True):
        ans = st.number_input("Your Answer:", step=1, value=None, label_visibility="collapsed")
        submit = st.form_submit_button("CHECK ANSWER 🚀")
        
        if submit:
            correct_ans = st.session_state.num1 + st.session_state.num2
            if ans == correct_ans:
                st.session_state.last_result = "correct"
                st.session_state.xp += 25
                # Logic for Reward Enhancement
                if st.session_state.xp >= 100:
                    st.session_state.level += 1
                    st.session_state.xp = 0
                    prizes = {2: "🔭", 3: "🛰️", 4: "🛸", 5: "🪐"}
                    if st.session_state.level in prizes:
                        st.session_state.inventory.append(prizes[st.session_state.level])
                
                # Setup next turn
                st.session_state.num1 = random.randint(1, st.session_state.level + 4)
                st.session_state.num2 = random.randint(1, st.session_state.level + 2)
                st.session_state.input_key += 1
                st.rerun()
            else:
                st.session_state.last_result = "wrong"

    # VISUAL FEEDBACK BANNERS
    if st.session_state.last_result == "correct":
        st.markdown('<p class="success-text">✨ EXCELLENT! +25 XP ✨</p>', unsafe_allow_html=True)
        st.balloons()
    elif st.session_state.last_result == "wrong":
        st.markdown('<p class="error-text">Almost! Keep trying, Hero! 💡</p>', unsafe_allow_html=True)

# --- 5. PARENT DATA ---
with st.expander("📊 Objective Progress Report"):
    st.write(f"Total Level: {st.session_state.level}")
    st.write(f"Items Collected: {len(st.session_state.inventory)}")
    st.download_button("Download Mastery Data", f"Level: {st.session_state.level}, Items: {st.session_state.inventory}", file_name="math_success.txt")
