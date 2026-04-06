import streamlit as st
import random

# --- 1. ULTRA-POLISH INTERFACE ---
st.set_page_config(page_title="Math Galaxy Pro", page_icon="🚀", layout="wide")

st.markdown("""
    <style>
    /* Main Background with subtle stars */
    .stApp {
        background: #0b0d17;
        background-image: radial-gradient(white, rgba(255,255,255,.2) 2px, transparent 40px);
        background-size: 550px 550px;
        color: white;
    }
    
    /* Neon Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: rgba(15, 23, 42, 0.9);
        border-right: 1px solid #38bdf8;
    }
    
    .journey-step {
        padding: 12px;
        border-radius: 12px;
        margin-bottom: 8px;
        border: 1px solid rgba(56, 189, 248, 0.3);
        text-align: center;
        color: #94a3b8;
        font-family: 'Segoe UI', sans-serif;
    }
    .active-step {
        background: linear-gradient(90deg, #0ea5e9 0%, #2563eb 100%) !important;
        color: white !important;
        box-shadow: 0px 0px 20px rgba(14, 165, 233, 0.5);
        border: none;
    }

    /* The Math Card - Vertical Scaffolding */
    .math-container {
        display: flex;
        justify-content: center;
        margin-top: 20px;
    }
    .math-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        padding: 50px;
        border-radius: 30px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        text-align: right;
        min-width: 300px;
    }
    .math-num {
        font-size: 100px;
        font-weight: 800;
        font-family: 'Monaco', monospace;
        text-shadow: 0 0 15px rgba(255,255,255,0.2);
    }
    .operator { 
        font-size: 60px; 
        color: #f43f5e; 
        float: left; 
        margin-top: 20px;
    }
    .divider { 
        border-bottom: 8px solid #f8fafc; 
        width: 100%; 
        margin: 10px 0; 
        border-radius: 4px;
    }
    
    /* BUTTON FIX: High Visibility Text */
    .stButton>button {
        width: 100%;
        height: 80px;
        background: #0ea5e9 !important;
        color: #ffffff !important;
        font-size: 28px !important;
        font-weight: bold !important;
        border-radius: 20px;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background: #38bdf8 !important;
        transform: scale(1.02);
        box-shadow: 0 0 30px rgba(14, 165, 233, 0.6);
    }

    /* Dialogue bubble */
    .bubble {
        background: #1e293b;
        padding: 20px;
        border-radius: 20px;
        border-left: 6px solid #0ea5e9;
        font-size: 22px;
        margin-bottom: 30px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. LOGIC ---
if 'level' not in st.session_state:
    st.session_state.update({
        'level': 1, 'xp': 0, 'inventory': [],
        'num1': random.randint(1, 5), 'num2': random.randint(1, 5),
        'input_key': 0, 'child_name': "Hero"
    })

# --- 3. SIDEBAR MAP ---
with st.sidebar:
    st.markdown("### 🗺️ Your Mission")
    worlds = [("🌲 Forest", 1), ("🌊 Ocean", 11), ("🌋 Volcano", 21), ("🚀 Space", 31)]
    for name, start in worlds:
        is_active = "active-step" if st.session_state.level >= start and st.session_state.level < start+10 else ""
        st.markdown(f'<div class="journey-step {is_active}">{name}</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.write(f"⭐ **XP:** {st.session_state.xp}")
    st.write("🎒 **Loot:** " + (" ".join(st.session_state.inventory) if st.session_state.inventory else "Empty"))

# --- 4. MAIN GAME ---
st.markdown(f'<div class="bubble">"Hey {st.session_state.child_name}! Solve this to blast off to the next planet!"</div>', unsafe_allow_html=True)

col_left, col_mid, col_right = st.columns([1, 1.5, 1])

with col_mid:
    # Vertical Math Card
    st.markdown(f"""
        <div class="math-container">
            <div class="math-card">
                <div class="math-num" style="color: #fb7185;">{st.session_state.num1}</div>
                <div class="operator">+</div>
                <div class="math-num" style="color: #38bdf8;">{st.session_state.num2}</div>
                <div class="divider"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Input Area
    ans = st.number_input("Result", step=1, value=None, key=f"ans_{st.session_state.input_key}", label_visibility="collapsed")
    
    if st.button("CHECK ANSWER 🚀"):
        if ans == st.session_state.num1 + st.session_state.num2:
            st.balloons()
            st.markdown('<audio autoplay><source src="https://assets.mixkit.co/active_storage/sfx/2013/2013-preview.mp3"></audio>', unsafe_allow_html=True)
            
            st.session_state.xp += 20
            if st.session_state.xp % 100 == 0:
                st.session_state.level += 1
                items = {2: "🔭", 5: "🛰️", 10: "🪐"}
                if st.session_state.level in items:
                    st.session_state.inventory.append(items[st.session_state.level])
            
            # Reset for next question
            st.session_state.num1 = random.randint(1, st.session_state.level + 4)
            st.session_state.num2 = random.randint(1, st.session_state.level + 2)
            st.session_state.input_key += 1
            st.rerun()
        elif ans is not None:
            st.markdown('<audio autoplay><source src="https://assets.mixkit.co/active_storage/sfx/2571/2571-preview.mp3"></audio>', unsafe_allow_html=True)
            st.error("Try again! You've got this! 💪")

# --- 5. HIDDEN PARENT TRACKER ---
with st.expander("⚙️ Parent Control"):
    st.session_state.child_name = st.text_input("Child's Name", st.session_state.child_name)
    if st.button("Clear Progress"):
        st.session_state.clear()
        st.rerun()
