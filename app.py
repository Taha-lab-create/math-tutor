import streamlit as st
import random
import time

# --- 1. THE COSMIC UI (STAYS PRO-LEVEL) ---
st.set_page_config(page_title="Math Galaxy: Zero-Cost Pro", layout="wide")

st.markdown("""
    <style>
    .stApp { background: #020617; color: #f8fafc; }
    .math-card {
        background: rgba(30, 41, 59, 0.8);
        border: 3px solid #38bdf8;
        border-radius: 40px;
        padding: 60px;
        text-align: center;
        box-shadow: 0 0 50px rgba(56, 189, 248, 0.3);
    }
    .stButton>button {
        background: linear-gradient(180deg, #f43f5e 0%, #be123c 100%) !important;
        height: 100px !important; font-size: 32px !important; border-radius: 30px !important;
        color: white !important; font-weight: 900 !important; border: 4px solid #fff !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. THE LOCAL SYLLABUS ENGINE ---
def generate_syllabus_problem(age, level, streak):
    """Mimics an LLM by choosing logic based on age and progress."""
    # Difficulty scales based on Age + (Level/2) + (Streak/5)
    difficulty_anchor = age + (level // 2) + (streak // 5)
    
    if age <= 5: # Visual/Early Learner
        n1 = random.randint(1, difficulty_anchor)
        n2 = random.randint(1, 5)
        return {"q": f"{n1} + {n2}", "a": n1 + n2, "mode": "visual"}
    
    elif age <= 8: # Primary Learner (Add/Sub)
        ops = ['+', '-']
        op = random.choice(ops)
        n1 = random.randint(10, 10 + difficulty_anchor * 2)
        n2 = random.randint(1, 10)
        if op == '-': n1, n2 = max(n1, n2), min(n1, n2) # Avoid negatives
        return {"q": f"{n1} {op} {n2}", "a": eval(f"{n1}{op}{n2}"), "mode": "text"}
    
    else: # Advanced Learner (Multi/Mix)
        ops = ['+', '-', '*']
        op = random.choice(ops)
        n1 = random.randint(5, 5 + difficulty_anchor)
        n2 = random.randint(2, 10)
        return {"q": f"{n1} {'×' if op=='*' else op} {n2}", "a": eval(f"{n1}{op}{n2}"), "mode": "text"}

# --- 3. STATE MANAGEMENT ---
if 'game_active' not in st.session_state:
    st.session_state.update({
        'game_active': False, 'age': 6, 'level': 1, 'xp': 0,
        'streak': 0, 'current_q': None, 'inventory': [],
        'start_time': time.time(), 'last_feedback': None
    })

# --- 4. THE WELCOME GATE ---
if not st.session_state.game_active:
    _, col, _ = st.columns([1, 2, 1])
    with col:
        st.title("👨‍🚀 Command Center")
        age = st.slider("Select Hero Age:", 3, 12, 6)
        if st.button("LAUNCH MISSION 🚀"):
            st.session_state.age = age
            st.session_state.current_q = generate_syllabus_problem(age, 1, 0)
            st.session_state.game_active = True
            st.rerun()
    st.stop()

# --- 5. MAIN HUD & GAMEPLAY ---
with st.sidebar:
    st.title("🛰️ HUD")
    st.metric("LEVEL", st.session_state.level)
    st.write(f"**🔥 Streak:** {st.session_state.streak}")
    st.progress(min(st.session_state.xp / 100, 1.0))
    st.write(f"**Inventory:** {' '.join(st.session_state.inventory)}")

# Timer logic
elapsed = time.time() - st.session_state.start_time
remaining = max(0, 20 - int(elapsed))

_, mid, _ = st.columns([1, 1.5, 1])
with mid:
    st.markdown(f"<h2 style='text-align:center;'>MISSION {st.session_state.level}.{st.session_state.streak}</h2>", unsafe_allow_html=True)
    
    # The Problem Card
    st.markdown(f"""
        <div class="math-card">
            <h1 style="font-size: 110px; margin:0;">{st.session_state.current_q['q']}</h1>
            <p style="color:#fb7185;">⏱️ Bonus Time: {remaining}s</p>
        </div>
    """, unsafe_allow_html=True)

    # Input Form
    with st.form(key=f"val_{st.session_state.level}_{st.session_state.streak}", clear_on_submit=True):
        ans = st.number_input("Enter Code:", step=1, value=None, label_visibility="collapsed")
        if st.form_submit_button("VALIDATE 🚀"):
            if ans == st.session_state.current_q['a']:
                # Success Logic
                points = 25 if remaining > 10 else 15
                st.session_state.xp += points
                st.session_state.streak += 1
                
                if st.session_state.xp >= 100:
                    st.session_state.level += 1
                    st.session_state.xp = 0
                    st.session_state.inventory.append("🛸")
                
                st.session_state.current_q = generate_syllabus_problem(
                    st.session_state.age, st.session_state.level, st.session_state.streak
                )
                st.session_state.start_time = time.time()
                st.balloons()
                st.rerun()
            else:
                st.error("Incorrect! Try again, Hero!")
                st.session_state.streak = 0
