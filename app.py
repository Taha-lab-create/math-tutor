import streamlit as st
import random
import time

# --- 1. GLOBAL DESIGN SYSTEM (High-Contrast & Modern) ---
st.set_page_config(page_title="Math Galaxy Quest", layout="wide", initial_sidebar_state="collapsed")

def inject_styles():
    st.markdown("""
        <style>
        /* High-Contrast Color Palette */
        :root {
            --bg-deep: #020617;
            --panel-bg: #0f172a;
            --neon-blue: #38bdf8;
            --neon-green: #10b981;
            --error-red: #f43f5e;
            --text-main: #f8fafc;
        }

        .stApp { background-color: var(--bg-deep); color: var(--text-main); }
        
        /* Mission Card styling from your reference guide */
        .mission-container {
            background: var(--panel-bg);
            border: 2px solid var(--neon-blue);
            border-radius: 24px;
            padding: 40px;
            text-align: center;
            box-shadow: 0 0 40px rgba(56, 189, 248, 0.15);
            margin-top: 20px;
        }

        /* Input Field Fix: High contrast white text on dark navy background */
        .stTextInput input, .stNumberInput input {
            background-color: #1e293b !important;
            color: #ffffff !important;
            border: 2px solid var(--neon-blue) !important;
            font-size: 24px !important;
            height: 60px !important;
        }

        /* Big Green 'Check Answer' Button */
        .stButton>button {
            background-color: var(--neon-green) !important;
            color: white !important;
            font-weight: 800 !important;
            font-size: 22px !important;
            height: 70px !important;
            width: 100% !important;
            border-radius: 16px !important;
            border: none !important;
            box-shadow: 0 6px 0 #047857 !important;
            transition: 0.1s;
        }
        .stButton>button:active { transform: translateY(4px); box-shadow: 0 2px 0 #047857 !important; }

        /* HUD Styling */
        .hud-label { color: var(--neon-blue); font-weight: 700; font-size: 14px; text-transform: uppercase; }
        .hud-value { color: #ffffff; font-size: 28px; font-weight: 900; }

        /* Orb Grid for Ages 3-5 */
        .orb { 
            width: 60px; height: 60px; border-radius: 50%;
            background: radial-gradient(circle at 30% 30%, #38bdf8, #1e40af);
            display: inline-block; margin: 10px;
            box-shadow: 0 0 20px rgba(56, 189, 248, 0.5);
        }
        </style>
    """, unsafe_allow_html=True)

# --- 2. ENGINE & STATE MANAGEMENT ---
if 'initialized' not in st.session_state:
    st.session_state.update({
        'initialized': True,
        'phase': 'START', # START, PLAY, REWARD
        'hero_name': '',
        'hero_age': 4,
        'level': 1,
        'xp': 0,
        'current_q': None,
        'current_a': 0,
        'attempts': 0
    })

def get_new_question():
    age = st.session_state.hero_age
    lvl = st.session_state.level
    if age <= 5:
        target = random.randint(1, 5 + lvl)
        st.session_state.current_q = "count"
        st.session_state.current_a = target
    else:
        num1 = random.randint(1, 5 * lvl)
        num2 = random.randint(1, 5)
        st.session_state.current_q = f"{num1} + {num2}"
        st.session_state.current_a = num1 + num2

# --- 3. UI RENDERING PHASES ---
inject_styles()

# HUD (Only visible after onboarding)
if st.session_state.phase != 'START':
    c1, c2, c3 = st.columns([1, 2, 1])
    with c1: st.markdown(f"<p class='hud-label'>Hero</p><p class='hud-value'>{st.session_state.hero_name}</p>", unsafe_allow_html=True)
    with c2: st.progress(st.session_state.xp / 100, text=f"Rank: Level {st.session_state.level}")
    with c3: st.markdown(f"<p class='hud-label'>XP Points</p><p class='hud-value'>{st.session_state.xp}</p>", unsafe_allow_html=True)

# PHASE: ONBOARDING
if st.session_state.phase == 'START':
    _, mid, _ = st.columns([1, 1.5, 1])
    with mid:
        st.markdown("<div class='mission-container'>", unsafe_allow_html=True)
        st.title("🚀 GALAXY ACADEMY")
        name = st.text_input("Enter Hero Name:", key="onboard_name")
        age = st.select_slider("Hero Age:", options=list(range(3, 13)), value=5)
        if st.button("INITIALIZE SYSTEMS 🛰️"):
            if name:
                st.session_state.hero_name = name
                st.session_state.hero_age = age
                get_new_question()
                st.session_state.phase = 'PLAY'
                st.rerun()
            else:
                st.error("Commander, we need your name to begin!")
        st.markdown("</div>", unsafe_allow_html=True)

# PHASE: THE EXERCISE (Main Loop)
elif st.session_state.phase == 'PLAY':
    _, mid, _ = st.columns([1, 2, 1])
    with mid:
        st.markdown("<div class='mission-container'>", unsafe_allow_html=True)
        
        # Display Question
        if st.session_state.current_q == "count":
            st.subheader("How many Star-Orbs can you find?")
            st.markdown("".join(['<div class="orb"></div>' for _ in range(st.session_state.current_a)]), unsafe_allow_html=True)
        else:
            st.markdown(f"<h1 style='font-size: 80px;'>{st.session_state.current_q}</h1>", unsafe_allow_html=True)

        # Interaction Form
        with st.form(key=f"math_form_{st.session_state.xp}"):
            ans = st.number_input("Your Answer", step=1, value=None, label_visibility="collapsed")
            submit = st.form_submit_button("CHECK ANSWER 🚀")
            
            if submit:
                if ans == st.session_state.current_a:
                    st.session_state.phase = 'REWARD'
                    st.rerun()
                else:
                    st.error("Almost! Recalibrate and try again, Hero!")
        st.markdown("</div>", unsafe_allow_html=True)

# PHASE: REWARD / FEEDBACK LOOP
elif st.session_state.phase == 'REWARD':
    _, mid, _ = st.columns([1, 1.5, 1])
    with mid:
        st.balloons()
        st.markdown(f"""
            <div class='mission-container' style='border-color: #10b981;'>
                <h1 style='color: #10b981;'>EXCELLENT WORK, {st.session_state.hero_name.upper()}!</h1>
                <p style='font-size: 20px;'>The mission was a success. +20 XP awarded.</p>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("NEXT MISSION ➡️"):
            st.session_state.xp += 20
            if st.session_state.xp >= 100:
                st.session_state.level += 1
                st.session_state.xp = 0
            get_new_question()
            st.session_state.phase = 'PLAY'
            st.rerun()
