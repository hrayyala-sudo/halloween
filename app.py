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

# Initialize Session State tracking for Easter Eggs
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

# Unblockable Native Browser Speech Generator with Monster Voice Modifiers
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

# If all eggs are found, render a clickable ghost action layout link
if all_eggs_found:
    if st.button("✨ The Floating Ghost is glowing! CLICK ME! ✨", use_container_width=True):
        st.session_state.ghost_dimension_unlocked = True
        st.toast("The air grows cold... A secret room has opened in the sidebar!", icon="🔮")

st.title("🎃 The Haunted Streamlit Mansion 💀")
st.write("Welcome, brave traveler... Enter at your own risk. Turn up your imagination and choose your fate below.")

# Easter Egg Progress HUD Tracker (Hidden once everything is done)
if not all_eggs_found:
    st.caption(f"🤫 Secrets Discovered: {sum([st.session_state.egg_porch, st.session_state.egg_story, st.session_state.egg_candy])} / 3")
else:
    if not st.session_state.ghost_dimension_unlocked:
        st.info("💡 Complete! All hidden Easter Eggs have been discovered. Quick, click the glowing Ghost button above!")

st.divider()

# --- SIDEBAR / NAVIGATION ---
menu_options = ["🚪 Front Porch", "📖 Spooky Story Generator", "🍬 Trick or Treat Roulette", "🔮 Monster Mash Soundboard"]
if st.session_state.ghost_dimension_unlocked:
    menu_options.append("🌌 The Ghost Dimension")

page = st.sidebar.selectbox("Choose Your Activity:", menu_options)

# --- PAGE 1: FRONT PORCH ---
if page == "🚪 Front Porch":
    st.header("Welcome to the Mansion")
    st.image("https://unsplash.com", 
             caption="The fog rolls in...", use_container_width=True)
    
    st.write("""
    You stand before a creaking, old Victorian mansion. The wind howls, and the moon is full.
    What secrets lie within these digital walls? Use the sidebar menu to explore the haunted rooms!
    """)
    
    # Easter Egg #1 input field box
    secret_knock = st.text_input("Psst... do you know the secret pass-phrase?", placeholder="Type here...")
    if secret_knock.lower() == "neon mint":
        if not st.session_state.egg_porch:
            st.session_state.egg_porch = True
            st.rerun()
    
    if st.session_state.egg_porch:
        st.success("🌟 EASTER EGG UNLOCKED: The walls glow bright in green (#05f7bf)!")
    
    if st.button("Knock on the Door 🚪"):
        with st.spinner("Creaaaaak..."):
            time.sleep(1)
        st.error("A disembodied voice whispers: *'Who dares disturb the mansion?!'*")
        st.balloons()

# --- PAGE 2: SPOOKY STORY GENERATOR ---
elif page == "📖 Spooky Story Generator":
    st.header("📜 Create Your Own Spooky Tale")
    st.write("Fill out the blanks to conjure a custom terrifying Halloween story.")
    
    col1, col2 = st.columns(2)
    with col1:
        protagonist = st.text_input("Main Character's Name", value="Brave Traveler")
        adjective = st.text_input("Spooky Adjective", value="slimy")
        creature = st.text_input("Monster/Creature", value="Shadow Beast")
    with col2:
        place = st.text_input("Creepy Place", value="The Graveyard")
        object_held = st.text_input("An Object", value="Flashlight")
        exclamation = st.text_input("Scared Exclamation", value="Help me!")

    # Easter Egg #2 trigger within inputs
    if protagonist.lower() == "goofy gang":
        if not st.session_state.egg_story:
            st.session_state.egg_story = True
            st.rerun()

    if st.session_state.egg_story:
        st.warning("👾 EASTER EGG UNLOCKED: Welcome to the official Goofy Gang sanctuary portal! 🚀")

    if st.button("🔮 Conjure Story"):
        story = f"""
        It was a dark and stormy night at **{place}**. **{protagonist}** was minding their own business 
        when suddenly, a **{adjective}** **{creature}** burst through the shadows! 
        
        **{protagonist}** gasped, dropping their **{object_held}** and screaming, "**{exclamation}**!" 
        They turned and ran as fast as they could back to safety. The End.
        """
        st.info(story)

# --- PAGE 3: TRICK OR TREAT ROULETTE ---
elif page == "🍬 Trick or Treat Roulette":
    st.header("🍬 Trick or Treat Roulette")
    st.write("Reach into the digital candy bowl. Will you get a delicious treat or a devious trick?")
    
    if st.button("🎃 Draw from the Bowl 🍬"):
        st.session_state.draw_count += 1
        
        # Easter Egg #3: Trigger exactly on or after the 5th draw
        if st.session_state.draw_count >= 5:
            if not st.session_state.egg_candy:
                st.session_state.egg_candy = True
                st.rerun()
            
        outcomes = [
            {"type": "Treat", "text": "You got a King-Sized Peanut Butter Cup! 🍫 (+100 Spooky Points)", "icon": "🎉"},
            {"type": "Treat", "text": "Sour Patch Kids that actually taste like green apples! 🍏", "icon": "🍭"},
            {"type": "Trick", "text": "A spider crawls out of the bowl! 🕷️ Run!", "icon": "😱"},
            {"type": "Trick", "text": "You got dental floss and a bruised apple. 🍏 BOOO!", "icon": "😒"},
            {"type": "Trick", "text": "Your path has been cursed! Everything is upside down (metaphorically). 🪄", "icon": "🔮"},
        ]
        
        result = random.choice(outcomes)
        if result["type"] == "Treat":
            st.success(f"{result['icon']} {result['text']}")
            st.snow()
        else:
            st.error(f"{result['icon']} {result['text']}")

    if st.session_state.egg_candy:
        st.warning("💀 EASTER EGG UNLOCKED: You found the hidden golden skull token down at the bottom of the bowl!")

# --- PAGE 4: MONSTER MASH SOUNDBOARD ---
elif page == "🔮 Monster Mash Soundboard":
    st.header("🎵 The Monster Mash Board")
    st.write("Turn up your speakers and click a button to hear pure creature effects!")
    
    c1, c2, c3 = st.columns(3)
    
    with c1:
        if st.button("🐺 Werewolf"):
            st.write("🐺 *AWOOOOOOOOO!*")
            speak_like_a_monster("Ah-wwooooo! Ow-ow-ow-wwoooo! Grrrr.", 0.2, 0.7)
    with c2:
        if st.button("🧛 Vampire"):
            st.write("🧛 *Mwahahahahaha!*")
            speak_like_a_monster("Mwahahahahaha! Ahahahaha!", 0.5, 0.85)
    with c3:
        if st.button("🧟 Zombie"):
            st.write("🧟 *Braaaaains...*")
            speak_like_a_monster("Uuuuuurrrrgh. Grrrrroaaaannn. Hhhhungggerrr.", 0.1, 0.4)

# --- SECRET PAGE 5: THE GHOST DIMENSION ---
elif page == "🌌 The Ghost Dimension" and st.session_state.ghost_dimension_unlocked:
    st.header("🌌 Room Unlocked: The Ghost Dimension")
    st.balloons()
    st.write("""
    **Congratulations, Ultimate Mansion Explorer!** You have broken through the code layout logic. 
    The floating ghost welcomes you to the infinite digital ether.
    """)
    st.image("https://unsplash.com", 
             caption="Deep space within the server racks...", use_container_width=True)
    
    if st.button("🔮 Summon The Grand Phantom Presence"):
