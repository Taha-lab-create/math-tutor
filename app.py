import streamlit as st
import random

# --- 1. TOUCH-FRIENDLY STYLING ---
st.set_page_config(page_title="Math Quest", page_icon="🎮", layout="centered")

# This CSS makes fonts huge for kids and centers everything for touchscreens
st.markdown("""
    <style>
    /* Make the question and text huge */
    .big-font { font-size:40px !important; font-weight: bold; color: #2E4053; text-align: center; }
    .stNumberInput div div input { font-size: 30px !important; height: 60px !important; text-align: center; }
    .stButton>button { height: 80px; font-size: 25px !important; border-radius: 20px; background-color: #4CAF50; color: white; }
    
    /* Fix the sidebar contrast */
    [data-testid="stSidebar"] { background-color: #FADBD8; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. PERMANENT MEMORY (Session State) ---
# This ensures progress doesn't reset when the screen refreshes
if 'level' not in st.session_state:
    st.session_state.level = 1
    st.session_state.xp = 0
    st.session_state.inventory = []
    st.session_state.history = []
    st.session_state.current_num1 = random.randint(1, 5)
    st.session_state.current_num2 = random.randint(1, 5)

def get_reward(level):
    rewards = {2: "🛡️ Wood Shield", 5: "🗡️ Stone Sword", 8: "🧥 Leather Armor", 10: "🦄 Magic Pony"}
    return rewards.get(level, None)

def generate_new_question():
    # Difficulty scales as level increases
    max_val = st.session_state.level + 4
    st.session_state.current_num1 = random.randint(1, max_val)
    st.session_state.current_num2 = random.randint(1, max_val)

# --- 3. THE SIDEBAR (Progress & Rewards) ---
with st.sidebar:
    st.title(f"Level {st.session_state.level}")
    st.write("XP Progress")
    st.progress(st.session_state.xp / 100)
    
    st.subheader("🎒 Your Inventory")
    if st.session_state.inventory:
        for item in st.session_state.inventory:
            st.write(f"✅ {item}")
    else:
        st.write("Win quests to find loot!")

# --- 4. MAIN GAMEPLAY ---
st.markdown(f'<p class="big-font">Quest {st.session_state.level}</p>', unsafe_allow_html=True)

# The Question Area
q_text = f"What is {st.session_state.current_num1} + {st.session_state.current_num2}?"
st.markdown(f'<p class="big-font" style="color:#1D8348;">{q_text}</p>', unsafe_allow_html=True)

# The Answer Box - we use 'key' to keep it stable
ans = st.number_input("Tap here to type:", step=1, value=None, key="ans_input")

# Use columns to center the button
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    submit = st.button("Check My Answer! 🚀")

# --- 5. THE BRAIN (Logic) ---
if submit:
    correct_ans = st.session_state.current_num1 + st.session_state.current_num2
    
    if ans == correct_ans:
        st.balloons()
        st.success(f"🌟 GREAT JOB! {ans} is correct!")
        st.session_state.xp += 25
        st.session_state.history.append(f"Level {st.session_state.level}: Correct")
        
        # Level Up Logic
        if st.session_state.xp >= 100:
            st.session_state.level += 1
            st.session_state.xp = 0
            gift = get_reward(st.session_state.level)
            if gift:
                st.session_state.inventory.append(gift)
                st.toast(f"New Item: {gift}!", icon='🎁')
            st.info(f"🎉 LEVEL UP! You are now Level {st.session_state.level}!")
        
        # Immediately change the numbers for the next round
        generate_new_question()
        st.rerun() # Refresh to show new numbers and update bars
    else:
        st.error("Oops! Not quite. Try again! 💡")
        st.info("Tip: Try using your fingers to count!")

# --- 6. PARENT DASHBOARD ---
with st.expander("📊 Parent Report (See Results)"):
    st.write(f"**Total Correct Answers:** {len(st.session_state.history)}")
    if st.button("Generate Downloadable Report"):
        report = f"Math Quest Results\nLevel reached: {st.session_state.level}\nItems: {st.session_state.inventory}"
        st.download_button("Download Report.txt", report)
