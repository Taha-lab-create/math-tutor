import streamlit as st
import random
import time

# --- 1. THE "GLASS-UI" DESIGN SYSTEM ---
st.set_page_config(page_title="Math Galaxy Pro", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;700;900&display=swap');
    
    html, body, [class*="st-"] { font-family: 'Outfit', sans-serif; }
    
    .stApp {
        background: radial-gradient(circle at 20% 30%, #0f172a 0%, #020617 100%);
        color: #f8fafc;
    }

    /* The "Hero" Math Card */
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(20px);
        border: 2px solid rgba(56, 189, 248, 0.3);
        border-radius: 40px;
        padding: 60px;
        text-align: center;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
        margin: 20px auto;
        max-width: 600px;
        animation: float 6s ease-in-out infinite;
    }

    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-15px); }
        100% { transform: translateY(0px); }
    }

    /* Orb Styling for Age 4 Identification */
    .orb-grid {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 15px;
        margin-bottom: 30px;
    }
    .orb {
        width: 45px;
        height: 45px;
        background: radial-gradient(circle at 30% 30%, #38bdf8, #1e40af);
        border-radius: 50%;
        box-shadow: 0 0 20px rgba(56, 189, 248, 0.6);
    }

    /* Ultra-Pro Button */
    .stButton>button {
        width: 100% !important;
        height: 85px !important;
        background: linear-gradient(135deg, #0ea5e9 0%, #2563eb 100%) !important;
        color: white !important;
        font-size: 28px !important;
        font-weight: 800 !important;
        border-radius: 25px !important;
        border: none !important;
        box-shadow: 0 10px 25px rgba(37, 99, 235, 0.4);
        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    .stButton>button:hover {
        transform: scale(1.03) translateY(-5px);
        box-shadow: 0 15px 35px rgba(37, 99, 235, 0.6);
    }

    /* HUD Metrics */
    .hud-box {
        background: rgba(15, 23, 42, 0.6);
        border-radius: 20px;
        padding: 15px;
        border: 1px solid rgba(56, 189, 248, 0.2);
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. PEDAGOGICAL ENGINE ---
def generate_problem(age, level):
    # IDENTITY MODE (Ages 3-5)
    if age <= 5:
        target_num = random.randint(1, 5 + level)
        return {
            "mode": "identify",
            "q": "Count the Space Orbs!",
            "val": target_num,
            "hint": "How many blue circles can you see?"
        }
    # ARITHMETIC MODE (Ages 6+)
    else:
        n1 = random.randint(level, level + 10)
        n2 = random.randint(1, 10)
        return {
            "mode": "math",
            "q": f"{n1} + {n2}",
            "val": n1 + n2,
            "hint": "Add them together!"
        }

# --- 3. SESSION STATE ---
if 'state' not in st.session_state:
    st.session_state.update({
        'active': False, 'age': 4, 'lvl': 1, 'xp': 0,
        'current': None, 'inv': [], 'start': time.time()
    })

# --- 4. PROFESSIONAL ONBOARDING ---
if not st.session_state.active:
    _, center, _ = st.columns([1, 1.5, 1])
    with center:
        st.markdown("<h1 style='text-align:center; font-size: 50px;'>Galaxy Academy</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; color:#94a3b8;'>Select the hero's age to begin calibration</p>", unsafe_allow_html=True)
        age_select = st.select_slider("", options=list(range(3, 13)), value=4)
        if st.button("INITIALIZE SYSTEMS"):
            with st.spinner("Calibrating Syllabus..."):
                time.sleep(1)
                st.session_state.age = age_select
                st.session_state.current = generate_problem(age_select, 1)
                st.session_state.active = True
                st.rerun()
    st.stop()

# --- 5. THE HUD (Top Bar) ---
col_hud1, col_hud2, col_hud3 = st.columns(3)
with col_hud1:
    st.markdown(f'<div class="hud-box"><b>RANK</b><br><span style="color:#38bdf8; font-size:20px;">LVL {st.session_state.lvl}</span></div>', unsafe_allow_html=True)
with col_hud2:
    st.markdown(f'<div class="hud-box"><b>PROGRESS</b><br>', unsafe_allow_html=True)
    st.progress(st.session_state.xp / 100)
    st.markdown('</div>', unsafe_allow_html=True)
with col_hud3:
    st.markdown(f'<div class="hud-box"><b>LOOT</b><br>{" ".join(st.session_state.inv) if st.session_state.inv else "Searching..."}</div>', unsafe_allow_html=True)

# --- 6. GAMEPLAY ---
curr = st.session_state.current
elapsed = time.time() - st.session_state.start
remaining = max(0, 15 - int(elapsed))

_, play_area, _ = st.columns([1, 2, 1])

with play_area:
    st.markdown(f'<p style="text-align:center; color:#fb7185; margin-bottom:0;">⏱️ TIME BONUS: {remaining}s</p>', unsafe_allow_html=True)
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    
    if curr['mode'] == "identify":
        st.markdown(f"<h2>{curr['q']}</h2>", unsafe_allow_html=True)
        # Visual Orbs for Age 4
        st.markdown('<div class="orb-grid">' + ('<div class="orb"></div>' * curr['val']) + '</div>', unsafe_allow_html=True)
    else:
        st.markdown(f"<h1 style='font-size:100px; margin:0;'>{curr['q']}</h1>", unsafe_allow_html=True)
    
    st.markdown(f"<p style='color:#94a3b8;'>{curr['hint']}</p>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    with st.form(key=f"input_{st.session_state.lvl}_{st.session_state.xp}", clear_on_submit=True):
        ans = st.number_input("Enter Answer", step=1, value=None, label_visibility="collapsed")
        submit = st.form_submit_button("VALIDATE 🚀")
        
        if submit:
            if ans == curr['val']:
                # Scoring
                bonus = 25 if remaining > 5 else 15
                st.session_state.xp += bonus
                
                if st.session_state.xp >= 100:
                    st.session_state.lvl += 1
                    st.session_state.xp = 0
                    prizes = ["🛸", "🛰️", "☄️", "🛡️"]
                    st.session_state.inv.append(random.choice(prizes))
                
                # New Problem
                st.session_state.current = generate_problem(st.session_state.age, st.session_state.lvl)
                st.session_state.start = time.time()
                st.balloons()
                st.rerun()
            else:
                st.error("Systems Check Failed. Try again!")
