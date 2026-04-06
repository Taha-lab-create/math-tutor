import streamlit as st
import random
import time

# --- 1. PROFESSIONAL THEME & ANIMATIONS ---
st.set_page_config(page_title="Galaxy Academy Pro", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;700;900&display=swap');
    
    html, body, [class*="st-"] { font-family: 'Outfit', sans-serif; background: #020617; }
    
    .stApp {
        background: radial-gradient(circle at 50% 50%, #0f172a 0%, #020617 100%);
        color: #f8fafc;
    }

    /* Professional Glassmorphism Card */
    .main-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(56, 189, 248, 0.3);
        border-radius: 40px;
        padding: 60px;
        text-align: center;
        box-shadow: 0 0 40px rgba(56, 189, 248, 0.1);
        margin: 20px auto;
        animation: subtle-float 6s ease-in-out infinite;
    }

    @keyframes subtle-float {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }

    /* Space Orbs for Age 4 Identification */
    .orb-container {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 20px;
        margin: 40px 0;
    }
    .space-orb {
        width: 60px;
        height: 60px;
        background: radial-gradient(circle at 30% 30%, #38bdf8, #1e40af);
        border-radius: 50%;
        box-shadow: 0 0 30px rgba(56, 189, 248, 0.5);
        animation: pulse 2s infinite alternate;
    }

    @keyframes pulse {
        from { transform: scale(1); opacity: 0.8; }
        to { transform: scale(1.1); opacity: 1; }
    }

    /* Professional Button Styling */
    .stButton>button {
        background: linear-gradient(135deg, #38bdf8 0%, #2563eb 100%) !important;
        border: none !important;
        border-radius: 20px !important;
        color: white !important;
        font-weight: 800 !important;
        font-size: 24px !important;
        height: 70px !important;
        width: 100% !important;
        box-shadow: 0 10px 20px rgba(37, 99, 235, 0.3);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 15px 30px rgba(37, 99, 235, 0.5);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. THE PEDAGOGICAL ENGINE ---
def get_new_quest(age, level):
    if age <= 4:
        # Number Identification for toddlers
        count = random.randint(1, 10)
        return {"mode": "identify", "val": count, "q": "How many Orbs are in the Galaxy?"}
    else:
        # Standard Math for older kids
        n1 = random.randint(1, 10 + level)
        n2 = random.randint(1, 5 + level)
        return {"mode": "math", "val": n1 + n2, "q": f"{n1} + {n2}"}

# --- 3. ROBUST STATE INITIALIZATION ---
if 'initialized' not in st.session_state:
    st.session_state.update({
        'initialized': False,
        'age': 4,
        'lvl': 1,
        'xp': 0,
        'quest': None,
        'inventory': [],
        'start_time': time.time()
    })

# --- 4. THE ONBOARDING GATE ---
if not st.session_state.initialized:
    _, col, _ = st.columns([1, 1.5, 1])
    with col:
        st.markdown("<h1 style='text-align:center; font-size: 48px; margin-top:50px;'>Galaxy Academy</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; color: #94a3b8;'>Select the hero's age to calibrate systems.</p>", unsafe_allow_html=True)
        
        age_select = st.select_slider("", options=list(range(3, 13)), value=4)
        
        if st.button("INITIALIZE SYSTEMS 🚀"):
            # Set values first, then flip the initialized bit
            st.session_state.age = age_select
            st.session_state.quest = get_new_quest(age_select, 1)
            st.session_state.initialized = True
            st.rerun()
    st.stop()

# --- 5. THE MISSION HUD ---
c1, c2, c3 = st.columns([1, 2, 1])
with c1:
    st.markdown(f"**RANK:** LEVEL {st.session_state.lvl}")
with c2:
    st.progress(st.session_state.xp / 100)
with c3:
    st.markdown(f"**INVENTORY:** {' '.join(st.session_state.inventory) if st.session_state.inventory else '---'}")

# --- 6. THE GAMEPLAY AREA ---
current = st.session_state.quest
_, play_col, _ = st.columns([1, 2, 1])

with play_col:
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.markdown(f"<h2 style='color:#38bdf8;'>{current['q']}</h2>", unsafe_allow_html=True)
    
    if current['mode'] == "identify":
        # Professional Visual Counting (No math symbols for Age 4)
        orb_html = "".join(['<div class="space-orb"></div>' for _ in range(current['val'])])
        st.markdown(f'<div class="orb-container">{orb_html}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f"<h1 style='font-size: 120px; margin: 40px 0;'>{current['q']}</h1>", unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

    # Input Form for Professional "Enter" key support
    with st.form(key=f"quest_form_{st.session_state.lvl}_{st.session_state.xp}", clear_on_submit=True):
        ans = st.number_input("Your Answer", step=1, value=None, label_visibility="collapsed")
        submit = st.form_submit_button("VALIDATE CODE")
        
        if submit:
            if ans == current['val']:
                st.session_state.xp += 25
                if st.session_state.xp >= 100:
                    st.session_state.lvl += 1
                    st.session_state.xp = 0
                    st.session_state.inventory.append(random.choice(["💎", "🛰️", "🛸"]))
                
                st.session_state.quest = get_new_quest(st.session_state.age, st.session_state.lvl)
                st.balloons()
                st.rerun()
            else:
                st.error("Access Denied! Recalibrate and try again.")
