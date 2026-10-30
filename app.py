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
    .ghost {
        font-size: 40px;
        animation: float 3s ease-in-out infinite;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

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

# --- HEADER ---
st.markdown("<div class='ghost'>👻</div>", unsafe_allow_html=True)
st.title("🎃 The Haunted Streamlit Mansion 💀")
st.write("Welcome, brave traveler... Enter at your own risk. Turn up your imagination and choose your fate below.")

st.divider()

# --- SIDEBAR / NAVIGATION ---
page = st.sidebar.selectbox("Choose Your Activity:", ["🚪 Front Porch", "📖 Spooky Story Generator", "🍬 Trick or Treat Roulette", "🔮 Monster Mash Soundboard"])

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
        st.success("🌟 EASTER EGG UNLOCKED: The walls glow bright in green (#05f7bf)!")
        st.snow()
    
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
    
    # Custom interaction counters for an ongoing tracking egg
    if "draw_count" not in st.session_state:
        st.session_state.draw_count = 0

    if st.button("🎃 Draw from the Bowl 🍬"):
        st.session_state.draw_count += 1
        
        # Easter Egg #3: Trigger exactly on the 5th draw
        if st.session_state.draw_count == 5:
            st.warning("👀 EASTER EGG UNLOCKED: You found the hidden golden skull token down at the bottom of the bowl! 💀")
            
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

# --- PAGE 4: MONSTER MASH SOUNDBOARD ---
elif page == "🔮 Monster Mash Soundboard":
    st.header("🎵 The Monster Mash Board")
    st.write("Turn up your speakers to 100% volume and click a button to hear the pure cinematic vocal creature effects!")
    
    c1, c2, c3 = st.columns(3)
    
    with c1:
        if st.button("🐺 Werewolf"):
            st.write("🐺 *AWOOOOOOOOO!*")
            # Uses vowel manipulation for real vocalizations instead of talking words
            speak_like_a_monster("Ah-wwooooo! Ow-ow-ow-wwoooo! Grrrr.", 0.2, 0.7)
    with c2:
        if st.button("🧛 Vampire"):
            st.write("🧛 *Mwahahahahaha!*")
            speak_like_a_monster("Mwahahahahaha! Ahahahaha!", 0.5, 0.85)
    with c3:
        if st.button("🧟 Zombie"):
            st.write("🧟 *Braaaaains...*")
            speak_like_a_monster("Uuuuuurrrrgh. Grrrrroaaaannn. Hhhhungggerrr.", 0.1, 0.4)

# --- FOOTER ---
st.markdown("<br><hr><center>Made with 🧡 and 🔮 by a Spooky Developer</center>", unsafe_allow_html=True)
