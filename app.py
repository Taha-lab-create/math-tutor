import streamlit as st
import random
import time

# --- 1. SUPER PRO INTERFACE STYLING ---
st.set_page_config(page_title="Math Galaxy: God Mode", page_icon="🌌", layout="wide")

st.markdown("""
    <style>
    /* Ultra-Dark Cyberpunk Theme */
    .stApp {
        background: radial-gradient(circle at center, #1e293b 0%, #020617 100%);
        color: #f8fafc;
    }
    
    /* Neon Sidebar */
    [data-testid="stSidebar"] {
        background-color: rgba(15, 23, 42, 0.95);
        border-right: 2px solid #38bdf8;
    }

    /* The 'Math Tablet' Card */
    .math-tablet {
        background: rgba(30, 41, 59, 0.7);
        backdrop-filter: blur(20px);
        border: 4px solid #38bdf8;
        border-radius: 60px;
        padding: 60px;
        width: 450px;
        margin: 0 auto;
        text-align: right;
        box-shadow: 0 0 50px rgba(56, 189, 248, 0.3);
    }
    .big-num { 
        font-size: 140px; 
        font-weight: 900; 
        font-family: 'Monaco', monospace; 
        line-height: 1;
        text-shadow: 0 0 20px rgba(56, 189, 248, 0.5);
    }
    .big-op { font-size: 90px; color: #fb7185; float: left; margin-top: 30px; }
    .neon-line { border-bottom: 12px solid #f8fafc; box-shadow: 0 5px 15px #fff; margin: 20px 0; border-radius: 10px; }

    /* The MEGA BUTTON - Maximum Contrast */
    .stButton>button {
        width: 100% !important;
        height: 120px !important;
        background: linear-gradient(180deg, #f43f5e 0%, #be123c 100%) !important;
        color: #ffffff !important;
        font-size: 40px !important;
        font-weight: 900 !important;
        border-radius: 40px !important;
        border: 6px solid #ffffff !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        box-shadow: 0 15px 0px #881337, 0 20px 30px rgba(0,0,0,0.5);
        transition: all 0.1s;
    }
    .stButton>button:active { transform: translateY(10px); box-shadow: 0 5px 0px #881337; }

    /* HUD Progress Bar */
    .stProgress > div > div > div > div { background-image: linear-gradient(to right, #38bdf8 , #818cf8); }
    </style>
    """, unsafe_allow_html=True)

# --- 2. THE LOCK-AND-KEY LOGIC ---
# We use st.session_state to "lock" the numbers until the child is ready
if 'n1' not in st.session_state:
    st.session_state.update({
        'level': 1, 'xp': 0, 'inventory': [],
        'n1': random.randint(1, 5), 'n2': random.randint(1, 5),
        'attempts': 0, 'show_win': False, 'show_loss': False
    })

def generate_new_numbers():
    # Difficulty scales slightly with level
    limit = st.session_state.level + 4
    st.session_state.n1 = random.randint(1, limit)
    st.session_state.n2 = random.randint(1, limit)

# --- 3. THE HUD (LEFT NAV) ---
with st.sidebar:
    st.markdown("<h1 style='color: #38bdf8; text-align:center;'>🚀 HUD 1.0</h1>", unsafe_allow_html=True)
    st.write(f"### 🛡️ RANK: Level {st.session_state.level}")
    st.progress(st.session_state.xp / 100)
    st.write(f"**XP:** {st.session_state.xp} / 100")
    
    st.markdown("---")
    st.write("### 🎒 SPACE LOOT")
    if st.session_state.inventory:
        for item in st.session_state.inventory:
            st.write(f"✨ {item}")
    else:
        st.caption("Complete quests to find artifacts!")

# --- 4. THE MAIN BATTLEGROUND ---
st.markdown("<h1 style='text-align: center; font-size: 55px; letter-spacing: 5px;'>MATH GALAXY QUEST</h1>", unsafe_allow_html=True)

_, mid, _ = st.columns([1, 1.5, 1])

with mid:
    # THE TABLET
    st.markdown(f"""
        <div class="math-tablet">
            <div class="big-num" style="color: #38bdf8;">{st.session_state.n1}</div>
            <div class="big-op">+</div>
            <div class="big-num" style="color: #818cf8;">{st.session_state.n2}</div>
            <div class="neon-line"></div>
        </div>
        """, unsafe_allow_html=True)

    # THE INPUT ZONE
    # We use a form to ensure "Enter" works and inputs don't lag
    with st.form(key=f"quest_form_{st.session_state.level}_{st.session_state.xp}"):
        ans = st.number_input("ENTER CODE", step=1, value=None, label_visibility="collapsed")
        submitted = st.form_submit_button("VALIDATE 🚀")
        
        if submitted:
            correct = st.session_state.n1 + st.session_state.n2
            if ans == correct:
                st.session_state.show_win = True
                st.session_state.show_loss = False
                st.session_state.xp += 25
                
                # Level Up Logic
                if st.session_state.xp >= 100:
                    st.session_state.level += 1
                    st.session_state.xp = 0
                    prizes = ["🔭 Ion Lens", "🛰️ Sat-Link", "💎 Star Jewel", "🛸 Scout Ship"]
                    st.session_state.inventory.append(random.choice(prizes))
                
                # IMPORTANT: ONLY REGENERATE AFTER SUCCESS
                generate_new_numbers()
                st.rerun()
            else:
                st.session_state.show_win = False
                st.session_state.show_loss = True

    # CELEBRATION / ERROR BANNERS
    if st.session_state.show_win:
        st.balloons()
        st.markdown("""
            <div style="background: #10b981; border: 5px solid white; border-radius: 30px; padding: 25px; text-align: center;">
                <h1 style="color: white; margin:0;">MISSION SUCCESS! 🌟</h1>
                <p style="color: white; font-size: 20px;">+25 XP Awarded to Hero</p>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('<audio autoplay><source src="https://assets.mixkit.co/active_storage/sfx/2013/2013-preview.mp3"></audio>', unsafe_allow_html=True)
        # We don't need a rerun here because the next quest generates after the next 'Win'
    
    if st.session_state.show_loss:
        st.markdown("""
            <div style="background: #f43f5e; border: 5px solid white; border-radius: 30px; padding: 25px; text-align: center;">
                <h1 style="color: white; margin:0;">SYSTEM ERROR! ❌</h1>
                <p style="color: white; font-size: 20px;">Try again, Commander!</p>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('<audio autoplay><source src="https://assets.mixkit.co/active_storage/sfx/2571/2571-preview.mp3"></audio>', unsafe_allow_html=True)

# --- 5. DATA CENTER ---
with st.expander("🛠️ COMMAND CENTER (Parent View)"):
    st.write("### Hero Performance Data")
    col_a, col_b = st.columns(2)
    col_a.metric("Quests Passed", (st.session_state.level - 1) * 4 + (st.session_state.xp // 25))
    col_b.metric("Loot Found", len(st.session_state.inventory))
    
    if st.button("Emergency System Reset"):
        for key in st.session_state.keys():
            del st.session_state[key]
        st.rerun()
