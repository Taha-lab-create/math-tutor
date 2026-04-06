import streamlit as st
import random

# --- 1. HUD & CYBER-SPACE STYLING ---
st.set_page_config(page_title="Math Galaxy: Ultra Pro", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    /* Dark Space Theme with Neon Grid */
    .stApp {
        background-color: #050505;
        background-image: linear-gradient(0deg, transparent 24%, rgba(56, 189, 248, .05) 25%, rgba(56, 189, 248, .05) 26%, transparent 27%, transparent 74%, rgba(56, 189, 248, .05) 75%, rgba(56, 189, 248, .05) 76%, transparent 77%, transparent), linear-gradient(90deg, transparent 24%, rgba(56, 189, 248, .05) 25%, rgba(56, 189, 248, .05) 26%, transparent 27%, transparent 74%, rgba(56, 189, 248, .05) 75%, rgba(56, 189, 248, .05) 76%, transparent 77%, transparent);
        background-size: 50px 50px;
    }

    /* Ultra-High Contrast Math Card */
    .math-card-pro {
        background: rgba(15, 23, 42, 0.9);
        border: 6px solid #0ea5e9;
        border-radius: 50px;
        padding: 50px;
        width: 400px;
        text-align: right;
        box-shadow: 0 0 40px rgba(14, 165, 233, 0.4);
        margin: 0 auto;
    }
    .num-large { font-size: 130px; font-weight: 900; font-family: 'Courier New', monospace; text-shadow: 0 0 20px rgba(255,255,255,0.3); }
    .op-large { font-size: 80px; color: #f43f5e; float: left; margin-top: 30px; font-weight: bold; }
    .glow-line { border-bottom: 12px solid #f8fafc; border-radius: 20px; margin: 20px 0; box-shadow: 0 0 15px #fff; }

    /* The Mega Button - Perfect Contrast */
    .stButton>button {
        width: 100% !important;
        height: 100px !important;
        background: #f43f5e !important; /* Hot Pink/Red for visibility */
        color: #ffffff !important;
        font-size: 36px !important;
        font-weight: 900 !important;
        border-radius: 30px !important;
        border: 5px solid #ffffff !important;
        text-transform: uppercase;
        letter-spacing: 2px;
        box-shadow: 0 10px 0px #9f1239;
        transition: all 0.1s;
    }
    .stButton>button:active { transform: translateY(8px); box-shadow: 0 2px 0px #9f1239; }

    /* Success/Error Banners */
    .banner-win { background: #10b981; color: white; padding: 20px; border-radius: 20px; font-size: 40px; text-align: center; font-weight: bold; border: 4px solid #ffffff; }
    .banner-lose { background: #f43f5e; color: white; padding: 20px; border-radius: 20px; font-size: 30px; text-align: center; border: 4px solid #ffffff; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. THE LOGIC CORE ---
if 'level' not in st.session_state:
    st.session_state.update({
        'level': 1, 'xp': 0, 'inventory': [],
        'n1': random.randint(1, 5), 'n2': random.randint(1, 5),
        'input_key': 0, 'feedback': None
    })

def refresh_quest():
    st.session_state.n1 = random.randint(1, st.session_state.level + 4)
    st.session_state.n2 = random.randint(1, st.session_state.level + 2)
    st.session_state.input_key += 1

# --- 3. THE MISSION SIDEBAR ---
with st.sidebar:
    st.markdown("<h1 style='color: #0ea5e9;'>🚀 HUD DISPLAY</h1>", unsafe_allow_html=True)
    st.write(f"### CURRENT LEVEL: {st.session_state.level}")
    st.progress(st.session_state.xp / 100)
    st.write(f"**XP TO NEXT REWARD:** {100 - st.session_state.xp}")
    st.markdown("---")
    st.write("### 🎒 COLLECTED LOOT")
    if st.session_state.inventory:
        for item in st.session_state.inventory:
            st.write(f"💎 {item}")
    else:
        st.write("Searching for treasures...")

# --- 4. THE MAIN GAME ---
st.markdown("<h1 style='text-align: center; color: #f8fafc; font-size: 60px;'>MATH GALAXY QUEST</h1>", unsafe_allow_html=True)

# Center everything
_, center_col, _ = st.columns([1, 1.5, 1])

with center_col:
    # 1. The Math Card
    st.markdown(f"""
        <div class="math-card-pro">
            <div class="num-large" style="color: #38bdf8;">{st.session_state.n1}</div>
            <div class="op-large">+</div>
            <div class="num-large" style="color: #f43f5e;">{st.session_state.n2}</div>
            <div class="glow-line"></div>
        </div>
        """, unsafe_allow_html=True)

    # 2. The Input Form
    with st.form(key=f"ultra_form_{st.session_state.input_key}", clear_on_submit=True):
        ans = st.number_input("ENTER CODE:", step=1, value=None, label_visibility="collapsed")
        # Massive Submit Button
        submit = st.form_submit_button("VALIDATE ANSWER 🛰️")
        
        if submit:
            if ans == (st.session_state.n1 + st.session_state.n2):
                st.session_state.feedback = "WIN"
                st.session_state.xp += 25
                if st.session_state.xp >= 100:
                    st.session_state.level += 1
                    st.session_state.xp = 0
                    prizes = ["⚡ Plasma Core", "🛡️ Aegis Shield", "🧪 Super Fuel", "👑 Galaxy Crown"]
                    st.session_state.inventory.append(prizes[st.session_state.level % 4])
                refresh_quest()
                st.rerun()
            else:
                st.session_state.feedback = "LOSE"

    # 3. Dynamic Feedback
    if st.session_state.feedback == "WIN":
        st.balloons()
        st.markdown('<div class="banner-win">✨ MISSION SUCCESS! +25 XP ✨</div>', unsafe_allow_html=True)
        st.markdown('<audio autoplay><source src="https://assets.mixkit.co/active_storage/sfx/2013/2013-preview.mp3"></audio>', unsafe_allow_html=True)
        st.session_state.feedback = None # Reset for next turn
    elif st.session_state.feedback == "LOSE":
        st.markdown('<div class="banner-lose">❌ CODE ERROR! TRY AGAIN, HERO!</div>', unsafe_allow_html=True)
        st.markdown('<audio autoplay><source src="https://assets.mixkit.co/active_storage/sfx/2571/2571-preview.mp3"></audio>', unsafe_allow_html=True)

# --- 5. PARENT DATA SECTOR ---
with st.expander("📁 ENCRYPTED PROGRESS DATA"):
    st.json({
        "Student": "Hero",
        "Mastery_Level": st.session_state.level,
        "Total_XP": st.session_state.xp,
        "Inventory_Count": len(st.session_state.inventory)
    })
    if st.button("RESET SYSTEM"):
        st.session_state.clear()
        st.rerun()
