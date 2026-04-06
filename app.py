import streamlit as st
import random
import time

# --- 1. THE DESIGN SYSTEM (CSS) ---
st.set_page_config(page_title="Galaxy Academy Pro", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;700;900&display=swap');
    
    html, body, [class*="st-"] { font-family: 'Outfit', sans-serif; background-color: #020617; }
    
    /* Fixed Contrast & Background */
    .stApp {
        background: radial-gradient(circle at 50% 50%, #0f172a 0%, #020617 100%);
        color: #f8fafc;
    }

    /* Phase Containers */
    .glass-panel {
        background: rgba(15, 23, 42, 0.8);
        border: 2px solid #38bdf8;
        border-radius: 30px;
        padding: 40px;
        text-align: center;
        box-shadow: 0 0 30px rgba(56, 189, 248, 0.2);
    }

    /* Success/Failure Animations */
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        25% { transform: translateX(-10px); }
        75% { transform: translateX(10px); }
    }
    .error-shake { animation: shake 0.4s ease-in-out; border: 2px solid #ef4444 !important; }
    
    /* Orb Design for Age 5 */
    .orb-grid { display: flex; flex-wrap: wrap; justify-content: center; gap: 15px; margin: 30px 0; }
    .orb { 
        width: 50px; height: 50px; border-radius: 50%;
        background: radial-gradient(circle at 30% 30%, #38bdf8, #1e40af);
        box-shadow: 0 0 20px #38bdf8;
    }

    /* Professional Buttons */
    .stButton>button {
        background: #38bdf8 !important; color: #020617 !important;
        font-weight: 900 !important; border-radius: 15px !important;
        height: 60px !important; width: 100% !important; border: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. ENGINE LOGIC ---
def generate_quest(age, lvl):
    if age <= 5:
        target = random.randint(1, 5 + lvl)
        return {"type": "count", "val": target, "q": f"How many Star-Orbs can you find?"}
    else:
        n1, n2 = random.randint(1, 10 + lvl), random.randint(1, 10)
        return {"type": "math", "val": n1 + n2, "q": f"{n1} + {n2}"}

# --- 3. THE STATE MACHINE ---
if 'phase' not in st.session_state:
    st.session_state.update({
        'phase': 'ONBOARDING',
        'name': '', 'age': 5, 'lvl': 1, 'xp': 0,
        'quest': None, 'feedback': ''
    })

# --- STAGE 1: ONBOARDING ---
if st.session_state.phase == 'ONBOARDING':
    _, col, _ = st.columns([1, 1.5, 1])
    with col:
        st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
        st.title("🚀 Galaxy Academy")
        name = st.text_input("Enter Hero Name:", placeholder="Commander...")
        age = st.select_slider("Select Age:", options=list(range(3, 13)), value=5)
        
        if st.button("START MISSION"):
            if name:
                st.session_state.update({
                    'name': name, 'age': age, 'phase': 'EXERCISE',
                    'quest': generate_quest(age, 1)
                })
                st.rerun()
            else:
                st.warning("Please enter your name, Hero!")
        st.markdown("</div>", unsafe_allow_html=True)

# --- STAGE 2 & 3: EXERCISE & FEEDBACK ---
elif st.session_state.phase == 'EXERCISE':
    # HUD
    c1, c2, c3 = st.columns([1, 2, 1])
    c1.metric("HERO", st.session_state.name)
    c2.progress(st.session_state.xp / 100, text=f"Level {st.session_state.lvl} Progress")
    c3.metric("RANK", f"LVL {st.session_state.lvl}")

    _, mid, _ = st.columns([1, 2, 1])
    with mid:
        q = st.session_state.quest
        st.markdown(f"<div class='glass-panel'><h3>{q['q']}</h3>", unsafe_allow_html=True)
        
        if q['type'] == "count":
            st.markdown('<div class="orb-grid">' + ('<div class="orb"></div>' * q['val']) + '</div>', unsafe_allow_html=True)
        else:
            st.markdown(f"<h1 style='font-size:80px;'>{q['q']}</h1>", unsafe_allow_html=True)

        with st.form(key=f"q_{st.session_state.xp}", clear_on_submit=True):
            ans = st.number_input("Your Answer", step=1, value=None, label_visibility="collapsed")
            if st.form_submit_button("VALIDATE 🚀"):
                if ans == q['val']:
                    st.session_state.feedback = "CORRECT"
                    st.session_state.phase = 'PROGRESS'
                    st.rerun()
                else:
                    st.error(f"Not quite, {st.session_state.name}! Try counting again. 🛰️")
        st.markdown("</div>", unsafe_allow_html=True)

# --- STAGE 4: PROGRESS & ENCOURAGEMENT ---
elif st.session_state.phase == 'PROGRESS':
    _, mid, _ = st.columns([1, 1.5, 1])
    with mid:
        st.balloons()
        st.markdown(f"""
            <div class='glass-panel'>
                <h1 style='color:#38bdf8;'>GREAT JOB, {st.session_state.name.upper()}!</h1>
                <p>You gained +25 XP!</p>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("NEXT GALAXY ➡️"):
            st.session_state.xp += 25
            if st.session_state.xp >= 100:
                st.session_state.lvl += 1
                st.session_state.xp = 0
            
            st.session_state.quest = generate_quest(st.session_state.age, st.session_state.lvl)
            st.session_state.phase = 'EXERCISE'
            st.rerun()
