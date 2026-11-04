import streamlit as st
import random
import time

# --- PAGE CONFIG & THEME ---
st.set_page_config(
    page_title="The Haunted Streamlit Mansion",
    page_icon="🎃",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Initialize Session State tracking for Easter Eggs and States
if "egg_porch" not in st.session_state:
    st.session_state.egg_porch = False
if "egg_story" not in st.session_state:
    st.session_state.egg_story = False
if "egg_candy" not in st.session_state:
    st.session_state.egg_candy = False
if "draw_count" not in st.session_state:
    st.session_state.draw_count = 0
if "ghost_dimension_unlocked" not in st.session_state:
    st.session_state.ghost_dimension_unlocked = False
if "graveyard_finished" not in st.session_state:
    st.session_state.graveyard_finished = False
if "arcade_unlocked" not in st.session_state:
    st.session_state.arcade_unlocked = False

# --- "PAC MAN 67" SIMULATION ENGINE STATE ---
if "pm_x" not in st.session_state:
    st.session_state.pm_x = 2
if "pm_y" not in st.session_state:
    st.session_state.pm_y = 2
if "ghost_x" not in st.session_state:
    st.session_state.ghost_x = random.randint(0, 4)
if "ghost_y" not in st.session_state:
    st.session_state.ghost_y = random.randint(0, 4)
if "is_super_mode" not in st.session_state:
    st.session_state.is_super_mode = False
if "super_mode_timer" not in st.session_state:
    st.session_state.super_mode_timer = 0
if "pm_score" not in st.session_state:
    st.session_state.pm_score = 0
if "orbs_active" not in st.session_state:
    st.session_state.orbs_active = {"Orb1": True, "Orb2": True, "Orb3": True, "Orb4": True}
if "pm_game_over" not in st.session_state:
    st.session_state.pm_game_over = False

# --- GOOFY GANG TETRIS ENGINE STATE ---
if "tetris_board" not in st.session_state:
    st.session_state.tetris_board = [["⬛" for _ in range(6)] for _ in range(10)]
if "piece_x" not in st.session_state:
    st.session_state.piece_x = 2
if "piece_y" not in st.session_state:
    st.session_state.piece_y = 0
if "tetris_score" not in st.session_state:
    st.session_state.tetris_score = 0
if "active_shape" not in st.session_state:
    st.session_state.active_shape = random.choice(["🟧", "🟪", "🟦", "🟩"])

# Custom CSS for Halloween Vibe & Animations
st.markdown("""
    <style>
    /* Dark, spooky background and neon accents */
    .stApp {
        background-color: #0F0C20;
        background-image: radial-gradient(circle, #241442 0%, #0F0C20 100%);
        color: #E0E0E0;
    }
    
    /* Custom Headers */
    h1, h2, h3 {
        color: #FF5E00 !important; /* Halloween Orange */
        font-family: 'Courier New', Courier, monospace;
        text-shadow: 2px 2px 4px #000000, 0 0 10px #9D00FF;
    }
    
    /* Spooky glowing buttons */
    .stButton>button {
        background-color: #9D00FF !important;
        color: white !important;
        border: 2px solid #FF5E00 !important;
        border-radius: 10px;
        font-weight: bold;
        box-shadow: 0 0 8px #9D00FF;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #FF5E00 !important;
        border: 2px solid #9D00FF !important;
        box-shadow: 0 0 15px #FF5E00;
        transform: scale(1.05);
    }
    
    /* Floating Ghost Animation */
    @keyframes float {
        0% { transform: translate(0, 0px); }
        50% { transform: translate(0, -15px); }
        100% { transform: translate(0, 0px); }
    }
    .ghost-style {
        font-size: 50px;
        animation: float 3s ease-in-out infinite;
        text-align: center;
        margin-bottom: -10px;
    }
    </style>
""", unsafe_allow_html=True)

# Check if all Easter Eggs are found
all_eggs_found = st.session_state.egg_porch and st.session_state.egg_story and st.session_state.egg_candy

# Unblockable Native Browser Speech Generator with Voice Modifiers
def speak_like_a_monster(text, pitch, rate):
    js_html = f"""
    <script>
    (function() {{
        if ('speechSynthesis' in window) {{
            window.speechSynthesis.cancel(); 
            var msg = new SpeechSynthesisUtterance("{text}");
            msg.pitch = {pitch}; 
            msg.rate = {rate};   
            window.speechSynthesis.speak(msg);
        }}
    }})();
    </script>
    """
    st.components.v1.html(js_html, height=0)

# --- HEADER & FLOATING GHOST EASTER EGG TRACKING ---
st.markdown("<div class='ghost-style'>👻</div>", unsafe_allow_html=True)

if all_eggs_found and not st.session_state.ghost_dimension_unlocked:
    if st.button("✨ The Floating Ghost is glowing! CLICK ME! ✨", use_container_width=True):
        st.session_state.ghost_dimension_unlocked = True
        st.toast("The air grows cold... The Haunted Graveyard has opened in the sidebar!", icon="🔮")
        st.rerun()

st.title("🎃 The Haunted Streamlit Mansion 💀")

# Menu routing logic setup
menu_options = ["🚪 Front Porch", "📖 Spooky Story Generator", "🍬 Trick or Treat Roulette", "🔮 Monster Mash Soundboard"]
if st.session_state.ghost_dimension_unlocked:
    menu_options.append("🌌 Haunted Graveyard")
if st.session_state.arcade_unlocked:
    menu_options.append("🕹️ Pac-Man 67 Station")
    menu_options.append("🧩 Goofy Gang Tetris")

page = st.sidebar.selectbox("Choose Your Activity:", menu_options)

# --- PAGE 1: FRONT PORCH ---
if page == "🚪 Front Porch":
    st.header("Welcome to the Mansion")
    st.image("https://unsplash.com", 
             caption="The fog rolls in...", use_container_width=True)
    
    # Hide inputs once respect is fully earned
    if not st.session_state.arcade_unlocked:
        secret_knock = st.text_input("Psst... do you know the secret pass-phrase?", placeholder="Type here...")
        if secret_knock.lower() == "neon mint":
            if not st.session_state.egg_porch:
                st.session_state.egg_porch = True
                st.rerun()
        
        if st.session_state.egg_porch:
            st.success("🌟 EASTER EGG UNLOCKED: The walls glow bright in green (#05f7bf)!")
    
    if st.button("Knock on the Door 🚪"):
        with st.spinner("Knocking..."):
            time.sleep(1)
        
        if st.session_state.graveyard_finished:
            st.session_state.arcade_unlocked = True
            st.rerun()
        else:
            st.error("A disembodied voice whispers: *'Who dares disturb the mansion?!'*")
            speak_like_a_monster("Who dares disturb the mansion?!", 0.2, 0.8)

    # Celebratory HUD view instantly triggered right after nice greeting
    if st.session_state.arcade_unlocked:
        st.success("👑 The monster bows deeply and whispers: 'Welcome back, Master Explorer. I respect your legendary bravery. Your Arcade prizes are unlocked inside the sidebar!'")
        st.snow()

# --- PAGE 2: SPOOKY STORY GENERATOR ---
elif page == "📖 Spooky Story Generator":
    st.header("📜 Create Your Own Spooky Tale")
    col1, col2 = st.columns(2)
    with col1:
        protagonist = st.text_input("Main Character's Name", value="Brave Traveler")
        adjective = st.text_input("Spooky Adjective", value="slimy")
        creature = st.text_input("Monster/Creature", value="Shadow Beast")
    with col2:
        place = st.text_input("Creepy Place", value="The Graveyard")
        object_held = st.text_input("An Object", value="Flashlight")
        exclamation = st.text_input("Scared Exclamation", value="Help me!")

    if protagonist.lower() == "goofy gang":
        if not st.session_state.egg_story:
            st.session_state.egg_story = True
            st.rerun()

    if st.session_state.egg_story:
        st.warning("👾 EASTER EGG UNLOCKED: Welcome to the official Goofy Gang sanctuary portal! 🚀")

    if st.button("🔮 Conjure Story"):
        story = f"It was a dark and stormy night at **{place}**. **{protagonist}** was minding their own business when a **{adjective}** **{creature}** burst out!"
        st.info(story)

# --- PAGE 3: TRICK OR TREAT ROULETTE ---
elif page == "🍬 Trick or Treat Roulette":
    st.header("🍬 Trick or Treat Roulette")
    if st.button("🎃 Draw from the Bowl 🍬"):
        st.session_state.draw_count += 1
        if st.session_state.draw_count >= 5:
            if not st.session_state.egg_candy:
                st.session_state.egg_candy = True
                st.rerun()
            
        outcomes = [{"type": "Treat", "text": "You got a King-Sized Peanut Butter Cup! 🍫", "icon": "🎉"}]
        result = random.choice(outcomes)
        st.success(result["text"])

    if st.session_state.egg_candy:
        st.warning("💀 EASTER EGG UNLOCKED: You found the hidden golden skull token down at the bottom of the bowl!")

# --- PAGE 4: MONSTER MASH SOUNDBOARD ---
elif page == "🔮 Monster Mash Soundboard":
    st.header("🎵 The Monster Mash Board")
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("🐺 Werewolf"):
            speak_like_a_monster("Ah-wwooooo! Ow-ow-ow-wwoooo! Grrrr.", 0.2, 0.7)
    with c2:
        if st.button("🧛 Vampire"):
            speak_like_a_monster("Mwahahahahaha! Ahahahaha!", 0.5, 0.85)
    with c3:
        if st.button("🧟 Zombie"):
            speak_like_a_monster("Uuuuuurrrrgh. Grrrrroaaaannn. Hhhhungggerrr.", 0.1, 0.4)

# --- SECRET PAGE 5: HAUNTED GRAVEYARD ---
elif page == "🌌 Haunted Graveyard" and st.session_state.ghost_dimension_unlocked:
    st.header("🌌 Secret Zone: The Haunted Graveyard")
    st.write("The spirits rise from the catacombs. Finish the final trial to confront the master!")
    
    if st.button("🔮 Summon The Grand Phantom Presence"):
        speak_like_a_monster("WwooooooOooooo. You have finished the graveyard challenge. Return to the porch to face the master.", 1.2, 0.7)
        st.session_state.graveyard_finished = True
        st.success("The Grand Phantom whispers: 'The challenge is complete! Go back to the front porch and knock on the door.' 👑")


--- UNLOCKED BONUS PAGE 6: PAC-MAN 67 ARCADE ---

elif page == "🕹️ Pac-Man 67 Station" and st.session_state.arcade_unlocked:
st.header("🕹️ Classic Pac Man 67 Hardware Simulation")
if st.session_state.pm_game_over:
st.error("💀 GAME OVER! The Ghost caught you in normal mode.")
if st.button("🎮 Insert Coin to Retry"):
st.session_state.pm_x, st.session_state.pm_y = 2, 2
st.session_state.ghost_x, st.session_state.ghost_y = random.randint(0, 4), random.randint(0, 4)
st.session_state.is_super_mode = False
st.session_state.orbs_active = {"Orb1": True, "Orb2": True, "Orb3": True, "Orb4": True}
st.session_state.pm_score = 0
st.session_state.pm_game_over = False
st.rerun()
else:
if st.session_state.is_super_mode:
st.session_state.super_mode_timer -= 1
if st.session_state.super_mode_timer <= 0:
st.session_state.is_super_mode = False
st.toast("⚡ Super Mode Expired!", icon="⏳")
st.subheader(f"Score: {st.session_state.pm_score} 🌟")
if st.session_state.is_super_mode:
st.warning(f"⚡ SUPER MODE ACTIVE! ({st.session_state.super_mode_timer} steps left) — Ghost is vulnerable!")
grid = [["▪️" for _ in range(5)] for _ in range(5)]
# Draw active Power Orbs at corners
if st.session_state.orbs_active["Orb1"]: grid[0][0] = "🔮"
if st.session_state.orbs_active["Orb2"]: grid[0][4] = "🔮"
if st.session_state.orbs_active["Orb3"]: grid[4][0] = "🔮"
if st.session_state.orbs_active["Orb4"]: grid[4][4] = "🔮"
ghost_icon = "🟢" if not st.session_state.is_super_mode else "💙"
grid[st.session_state.ghost_y][st.session_state.ghost_x] = ghost_icon
grid[st.session_state.pm_y][st.session_state.pm_x] = "🟡" if not st.session_state.is_super_mode else "⚡"
for row in grid:
st.subheader(" ".join(row))
st.write("---")
ctrl_col1, ctrl_col2, ctrl_col3, ctrl_col4 = st.columns(4)
moved = False
with ctrl_col1:
if st.button("◀️ Button A (Left)") and st.session_state.pm_x > 0:
st.session_state.pm_x -= 1
moved = True
with ctrl_col2:
if st.button("▶️ Button B (Right)") and st.session_state.pm_x < 4:
st.session_state.pm_x += 1
moved = True
with ctrl_col3:
if st.button("🔽 Button A+B (Down)") and st.session_state.pm_y < 4:
st.session_state.pm_y += 1
moved = True
with ctrl_col4:
if st.button("🔼 Logo Touch (Up)") and st.session_state.pm_y > 0:
st.session_state.pm_y -= 1
moved = True
if moved:
gg = random.randint(1, 4)
if gg == 1 and st.session_state.ghost_x < 4: st.session_state.ghost_x += 1
elif gg == 2 and st.session_state.ghost_x > 0: st.session_state.ghost_x -= 1
elif gg == 3 and st.session_state.ghost_y < 4: st.session_state.ghost_y += 1
elif gg == 4 and st.session_state.ghost_y > 0: st.session_state.ghost_y -= 1
# Orb Collision Checks
if st.session_state.pm_x == 0 and st.session_state.pm_y == 0 and st.session_state.orbs_active["Orb1"]:
st.session_state.orbs_active["Orb1"] = False
st.session_state.is_super_mode = True
st.session_state.super_mode_timer = 10
elif st.session_state.pm_x == 4 and st.session_state.pm_y == 0 and st.session_state.orbs_active["Orb2"]:
st.session_state.orbs_active["Orb2"] = False
st.session_state.is_super_mode = True
st.session_state.super_mode_timer = 10
elif st.session_state.pm_x == 0 and st.session_state.pm_y == 4 and st.session_state.orbs_active["Orb3"]:
st.session_state.orbs_active["Orb3"] = False
st.session_state.is_super_mode = True
st.session_state.super_mode_timer = 10
elif st.session_state.pm_x == 4 and st.session_state.pm_y == 4 and st.session_state.orbs_active["Orb4"]:
st.session_state.orbs_active["Orb4"] = False
st.session_state.is_super_mode = True
st.session_state.super_mode_timer = 10
if st.session_state.pm_x == st.session_state.ghost_x and st.session_state.pm_y == st.session_state.ghost_y:
if st.session_state.is_super_mode:
st.session_state.pm_score += 10
st.toast("Ghost Eaten! +10 Points 👻")
st.session_state.ghost_x = random.randint(0, 4)
st.session_state.ghost_y = random.randint(0, 4)
else:
st.session_state.pm_game_over = True
st.rerun()

--- UNLOCKED BONUS PAGE 7: GOOFY GANG RECONSTRUCTED TETRIS ---

elif page == "🧩 Goofy Gang Tetris" and st.session_state.arcade_unlocked:
st.header("🧩 Goofy Gang Reconstructed Tetris Room")
st.write(f"Score: {st.session_state.tetris_score} 🔥 | Steer the falling neon blocks down to clear full rows!")
display_board = [row[:] for row in st.session_state.tetris_board]
if st.session_state.piece_y < 10:
display_board[st.session_state.piece_y][st.session_state.piece_x] = st.session_state.active_shape
for row in display_board:
st.subheader(" ".join(row))
st.write("---")
left_btn, right_btn, drop_btn = st.columns(3)
action_taken = False
with left_btn:
if st.button("◀️ Move Left") and st.session_state.piece_x > 0:
st.session_state.piece_x -= 1
action_taken = True
with right_btn:
if st.button("▶️ Move Right") and st.session_state.piece_x < 5:
st.session_state.piece_x += 1
action_taken = True
with drop_btn:
if st.button("🔽 Step Down"):
action_taken = True
if action_taken or st.button("⏳ Tick Gravity"):
st.session_state.piece_y += 1
if st.session_state.piece_y >= 10:
st.session_state.tetris_board[st.session_state.piece_y - 1][st.session_state.piece_x] = st.session_state.active_shape
for idx, r in enumerate(st.session_state.tetris_board):
if "⬛" not in r:
st.session_state.tetris_board.pop(idx)
st.session_state.tetris_board.insert(0, ["⬛" for _ in range(6)])
st.session_state.tetris_score += 100
st.toast("Row Cleared! +100 Points 🚀", icon="🔥")
st.session_state.piece_x = 2
st.session_state.piece_y = 0
st.session_state.active_shape = random.choice(["🟧", "🟪", "🟦", "🟩"])
st.rerun()
if st.button("🔄 Reset Arcade Board"):
st.session_state.tetris_board = [["⬛" for _ in range(6)] for _ in range(10)]
st.session_state.piece_x = 2
st.session_state.piece_y = 0
st.session_state.tetris_score = 0
st.rerun()

--- FOOTER ---

st.markdown("Made with 🧡 and 🔮 by a Spooky Developer", unsafe_allow_html=True)
