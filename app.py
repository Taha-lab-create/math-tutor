import streamlit as st
import random
import time

# --- 1. THE DESIGN SYSTEM (HIGH CONTRAST) ---
st.set_page_config(page_title="Galaxy Academy Pro", layout="wide", initial_sidebar_state="collapsed")

def apply_pro_styles():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;700;900&display=swap');
        
        /* Base Setup */
        html, body, [class*="st-"] { font-family: 'Outfit', sans-serif; background-color: #020617; }
        .stApp { background: radial-gradient(circle at 50% 50%, #0f172a 0%, #020617 100%); color: #FFFFFF; }

        /* High-Contrast Input Fields */
        input[type="text"], input[type="number"] {
            background-color: #1e293b !important;
            color: #FFFFFF !important;
            border: 2px solid #38bdf8 !important;
            border-radius: 12px !important;
            padding: 10px !important;
            font-size: 20px !important;
        }

        /* The Main Mission Card */
        .mission-card {
            background: rgba(15, 23, 42, 0.95);
            border: 3px solid #38bdf8;
            border-radius: 40px;
            padding: 50px;
            text-align: center;
            box-shadow: 0 0 50px rgba(56, 189, 248, 0.2);
            margin: 20px auto;
        }

        /* Success/Progress Banner */
        .success-banner {
            background: linear-gradient(90deg, #065f46, #059669);
            color: white;
            padding: 20px;
            border-radius: 20px;
            border: 2px solid #10b981;
            margin-bottom: 20px;
            animation: pulse 2s infinite;
        }

        /* Orb Grid for Visual Counting (Age 4-5) */
        .orb-grid { display: flex; flex-wrap: wrap; justify-content: center; gap: 20px; margin: 40px 0; }
        .orb { 
            width: 70px; height: 70px; border-radius: 50%;
            background: radial-gradient(circle at 30% 30%, #38bdf8, #1e40af);
            box-shadow: 0 0 30px rgba(56, 189, 248, 0.6);
            border: 3px solid #FFFFFF;
        }

        /* Navigation Buttons */
        .stButton>button {
            background: #10b981 !important; /* High Visibility Green */
            color: white !important;
            font-size: 24px !important;
            font-weight: 900 !important;
            height: 70px !important;
            border-radius: 20px !important;
            box-shadow: 0 8px 0 #047857;
            transition: all 0.1s;
        }
        .stButton>button:active { transform: translateY(4px); box-shadow: 0 2px 0 #047857; }

        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.02); }
            100% { transform: scale(1); }
        }
        </style>
    """, unsafe_allow_html=True)

# --- 2. GAME ENGINE MODULES ---
def generate_level_data(age, level):
    """Syllabus Logic: Defines the problem based on developmental stage."""
    if age <= 5:
        # One-to-one correspondence mode (Counting)
        target = random.randint(2, 6 + level)
        return {"mode": "count", "val": target, "text": "Count the Space Orbs!"}
    else:
        # Arithmetic mode
        ops = ['+'] if level < 3 else ['+', '-']
        op = random.choice(ops)
        n1 = random.randint(level, level + 10)
        n2 = random.randint(1, 10)
        if op == '-': n1, n2 = max(n1, n2), min(n1, n2)
        return {"mode": "math", "val": eval(f"{n1}{op}{n2}"), "text": f"{n1} {op} {n2}"}

def initialize_session():
    if 'app_state' not in st.session_state:
        st.session_state.update({
            'phase': 'ONBOARDING',
            'user_name': '',
            'user_age': 4,
            'current_level': 1,
            'xp': 0,
            'quest': None,
            'feedback_msg': '',
            'history': []
        })

# --- 3. THE PHASE RENDERER ---
def render_onboarding():
    _, col, _ = st.columns([1, 1.8, 1])
    with col:
        st.markdown("<div class='mission-card'>", unsafe_allow_html=True)
        st.title("👨‍🚀 GALAXY ACADEMY")
        name = st.text_input("HERO NAME", placeholder="Type your name here...")
        age = st.select_slider("YOUR AGE", options=list(range(3, 13)), value=4)
        
        if st.button("LAUNCH MISSION 🚀"):
            if name.strip():
                st.session_state.user_name = name
                st.session_state.user_age = age
                st.session_state.quest = generate_level_data(age, 1)
                st.session_state.phase = 'EXERCISE'
                st.rerun()
            else:
                st.error("Wait! We need your name to start the rocket!")
        st.markdown("</div>", unsafe_allow_html=True)

def render_exercise():
    # HUD Bar
    h1, h2, h3 = st.columns([1, 2, 1])
    h1.metric("HERO", st.session_state.user_name)
    h2.progress(st.session_state.xp / 100, text=f"Level {st.session_state.current_level} Progress")
    h3.metric("XP", st.session_state.xp)

    _, mid, _ = st.columns([1, 2, 1])
    with mid:
        q = st.session_state.quest
        st.markdown(f"<div class='mission-card'><h2>{q['text']}</h2>", unsafe_allow_html=True)
        
        if q['mode'] == "count":
            st.markdown('<div class="orb-grid">' + ('<div class="orb"></div>' * q['val']) + '</div>', unsafe_allow_html=True)
        else:
            st.markdown(f"<h1 style='font-size:100px; color:#38bdf8;'>{q['text']}</h1>", unsafe_allow_html=True)

        with st.form(key=f"input_form_{st.session_state.xp}", clear_on_submit=True):
            ans = st.number_input("ANSWER", step=1, value=None, label_visibility="collapsed")
            if st.form_submit_button("CHECK MY ANSWER! ✅"):
                if ans == q['val']:
                    st.session_state.phase = 'FEEDBACK'
                    st.rerun()
                else:
                    st.error(f"Oops! Let's try that again, {st.session_state.user_name}!")
        st.markdown("</div>", unsafe_allow_html=True)

def render_feedback():
    _, col, _ = st.columns([1, 1.5, 1])
    with col:
        st.balloons()
        st.markdown(f"""
            <div class='success-banner'>
                <h1 style='text-align:center;'>OUTSTANDING, {st.session_state.user_name.upper()}!</h1>
            </div>
            <div class='mission-card'>
                <p style='font-size:24px;'>You've mastered this quest!</p>
                <h3>+25 XP Gained</h3>
        """, unsafe_allow_html=True)
        
        if st.button("NEXT MISSION ➡️"):
            st.session_state.xp += 25
            if st.session_state.xp >= 100:
                st.session_state.current_level += 1
                st.session_state.xp = 0
            
            st.session_state.quest = generate_level_data(st.session_state.user_age, st.session_state.current_level)
            st.session_state.phase = 'EXERCISE'
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# --- 4. EXECUTION ---
initialize_session()
apply_pro_styles()

if st.session_state.phase == 'ONBOARDING':
    render_onboarding()
elif st.session_state.phase == 'EXERCISE':
    render_exercise()
elif st.session_state.phase == 'FEEDBACK':
    render_feedback()
