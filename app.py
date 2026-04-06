import streamlit as st
import random

# --- 1. PRO-GRADE INTERFACE STYLING ---
st.set_page_config(page_title="Math Galaxy", page_icon="🚀", layout="wide")

# Custom CSS to mimic the high-end space theme
st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background: radial-gradient(circle, #1b2735 0%, #090a0f 100%);
        color: white;
    }
    
    /* Left Nav Journey Styling */
    .journey-step {
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 10px;
        border: 1px solid #3498db;
        text-align: center;
        background: rgba(52, 152, 219, 0.1);
    }
    .active-step {
        background: #3498db !important;
        box-shadow: 0px 0px 15px #3498db;
        font-weight: bold;
    }

    /* Math Problem Card (The Scaffolding) */
    .math-box {
        font-family: 'Courier New', Courier, monospace;
        font-size: 80px;
        line-height: 1.2;
        text-align: right;
        padding: 40px;
        border-radius: 20px;
        background: rgba(255, 255, 255, 0.05);
        border: 2px solid rgba(255, 255, 255, 0.1);
        display: inline-block;
        margin-top: 20px;
    }
    .operator { color: #e74c3c; float: left; margin-right: 20px; }
    .line { border-bottom: 5px solid white; width: 100%; margin-top: 10px; }
    
    /* Guide Text */
    .guide-text {
        font-size: 24px;
        font-style: italic;
        color: #ecf0f1;
        background: rgba(0,0,0,0.4);
        padding: 20px;
        border-radius: 15px;
        border-left: 5px solid #f1c40f;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. GAME STATE ---
if 'level' not in st.session_state:
    st.session_state.update({
        'level': 1, 'xp': 0, 'inventory': [],
        'num1': random.randint(1, 5), 'num2': random.randint(1, 5),
        'input_key': 0, 'child_name': "Hero"
    })

# --- 3. LAYOUT: LEFT NAV & MAIN CONTENT ---
left_nav, main_game = st.columns([1, 4])

with left_nav:
    st.markdown("### 🗺️ The Journey")
    stages = [
        (1, "🌲 Forest"), (11, "🌊 Ocean"), 
        (21, "🌋 Volcano"), (31, "🚀 Space")
    ]
    for start_lvl, label in stages:
        active_class = "active-step" if st.session_state.level >= start_lvl and st.session_state.level < start_lvl+10 else ""
        st.markdown(f'<div class="journey-step {active_class}">{label}</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.metric("Total XP", st.session_state.xp)
    if st.session_state.inventory:
        st.write("🎒 **Prizes:** " + " ".join(st.session_state.inventory))

with main_game:
    # Character Dialogue
    st.markdown(f'<div class="guide-text">"Okay {st.session_state.child_name}, let\'s solve this equation to fuel our rocket!"</div>', unsafe_allow_html=True)
    
    # Visual Scaffolding (Stacked Math)
    col_a, col_b, col_c = st.columns([1, 1, 1])
    with col_b:
        st.markdown(f"""
            <div class="math-box">
                <span style="color: #ff4b4b;">{st.session_state.num1}</span><br>
                <span class="operator">+</span><span style="color: #4bafff;">{st.session_state.num2}</span>
                <div class="line"></div>
            </div>
            """, unsafe_allow_html=True)
        
        # Giant Input
        ans = st.number_input("Type result here:", step=1, value=None, key=f"ans_{st.session_state.input_key}", label_visibility="collapsed")
        
        if st.button("LAUNCH 🚀", use_container_width=True):
            if ans == st.session_state.num1 + st.session_state.num2:
                st.balloons()
                # Correct Sound
                st.markdown('<audio autoplay><source src="https://assets.mixkit.co/active_storage/sfx/2013/2013-preview.mp3"></audio>', unsafe_allow_html=True)
                
                st.session_state.xp += 20
                if st.session_state.xp % 100 == 0:
                    st.session_state.level += 1
                    rewards = {2: "🔭", 5: "🛰️", 10: "🪐"}
                    if st.session_state.level in rewards:
                        st.session_state.inventory.append(rewards[st.session_state.level])
                
                # New Numbers
                st.session_state.num1 = random.randint(1, st.session_state.level + 4)
                st.session_state.num2 = random.randint(1, st.session_state.level + 2)
                st.session_state.input_key += 1
                st.rerun()
            else:
                st.error("Engine failure! Try that number again. 💡")
                st.markdown('<audio autoplay><source src="https://assets.mixkit.co/active_storage/sfx/2571/2571-preview.mp3"></audio>', unsafe_allow_html=True)

# --- 4. HIDDEN PARENT TRACKER ---
with st.expander("⚙️ Parent Control"):
    st.session_state.child_name = st.text_input("Child's Name", st.session_state.child_name)
    if st.button("Reset All Progress"):
        st.session_state.clear()
        st.rerun()
