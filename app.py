import streamlit as st
import random
import time
import base64
import math
import struct

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

# 100% Reliable Offline Sound Generator (Generates clean synth audio mathematically)
def generate_halloween_synth(sound_type):
    sample_rate = 8000
    duration_ms = 1200
    num_samples = int(sample_rate * (duration_ms / 1000.0))
    audio_data = bytearray()
    
    for i in range(num_samples):
        t = float(i) / sample_rate
        
        if sound_type == "wolf":
            # Rising and falling low-pitch howl
            frequency = 150 + 80 * math.sin(math.pi * t / 1.2)
            val = int(25000.0 * math.sin(2.0 * math.pi * frequency * t))
        elif sound_type == "laugh":
            # Bouncing spooky chopped evil laugh pulses
            frequency = 90
            pulse = math.sin(2.0 * math.pi * 7 * t) # Chop up the sound
            if pulse > 0:
                val = int(20000.0 * math.sin(2.0 * math.pi * frequency * t))
            else:
                val = 0
        else:
            # Ghostly wavering Theremin tone
            frequency = 300 + 40 * math.sin(2.0 * math.pi * 6 * t)
            val = int(18000.0 * math.sin(2.0 * math.pi * frequency * t))
            
        audio_data.extend(struct.pack('<h', val))
        
    # Build standard system-ready RIFF/WAVE header wrapper
    header = bytearray()
    header.extend(b'RIFF')
    header.extend(struct.pack('<I', 36 + len(audio_data)))
    header.extend(b'WAVEfmt ')
    header.extend(struct.pack('<I', 16))
    header.extend(struct.pack('<H', 1))  # PCM Format
    header.extend(struct.pack('<H', 1))  # Mono
    header.extend(struct.pack('<I', sample_rate))
    header.extend(struct.pack('<I', sample_rate * 2))
    header.extend(struct.pack('<H', 2))
    header.extend(struct.pack('<H', 16)) # 16-bit precision
    header.extend(b'data')
    header.extend(struct.pack('<I', len(audio_data)))
    
    return base64.b64encode(header + audio_data).decode('utf-8')

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
    
    if st.button("Knock on the Door 🚪"):
        with st.spinner("Creaaaaak..."):
            time.sleep(1)
        st.error("A disembodied voice whispers: *'Who dares disturb the Streamlit code?!'*")
        st.balloons()

# --- PAGE 2: SPOOKY STORY GENERATOR ---
elif page == "📖 Spooky Story Generator":
    st.header("📜 Create Your Own Spooky Tale")
    st.write("Fill out the blanks to conjure a custom terrifying (or hilarious) Halloween story.")
    
    col1, col2 = st.columns(2)
    with col1:
        protagonist = st.text_input("Main Character's Name", value="Professor Code")
        adjective = st.text_input("Spooky Adjective", value="slimy")
        creature = st.text_input("Monster/Creature", value="Python Bug")
    with col2:
        place = st.text_input("Creepy Place", value="The Server Room")
        object_held = st.text_input("An Object", value="Keyboard")
        exclamation = st.text_input("Scared Exclamation", value="Syntax Error!")

    if st.button("🔮 Conjure Story"):
        story = f"""
        It was a dark and stormy night at **{place}**. **{protagonist}** was minding their own business 
        when suddenly, a **{adjective}** **{creature}** burst through the wall! 
        
        **{protagonist}** gasped, dropping their **{object_held}** and screaming, "**{exclamation}**!" 
        But it was too late. The **{creature}** didn't want to eat them—it just wanted to review their code. 
        They lived happily (and bug-free) ever after. The End.
        """
        st.info(story)

# --- PAGE 3: TRICK OR TREAT ROULETTE ---
elif page == "🍬 Trick or Treat Roulette":
    st.header("🍬 Trick or Treat Roulette")
    st.write("Reach into the digital candy bowl. Will you get a delicious treat or a devious trick?")
    
    if st.button("🎃 Draw from the Bowl 🍬"):
        outcomes = [
            {"type": "Treat", "text": "You got a King-Sized Peanut Butter Cup! 🍫 (+100 Spooky Points)", "icon": "🎉"},
            {"type": "Treat", "text": "Sour Patch Kids that actually taste like green apples! 🍏", "icon": "🍭"},
            {"type": "Trick", "text": "A spider crawls out of the bowl! 🕷️ Run!", "icon": "😱"},
            {"type": "Trick", "text": "You got a dental floss and a bruised apple. 🍏 BOOO!", "icon": "😒"},
            {"type": "Trick", "text": "Your CSS has been cursed! Everything is upside down (metaphorically). 🪄", "icon": "🔮"},
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
    st.write("No internet needed. These sounds are generated dynamically by your Python code server!")
    
    # Generate local data structures instantly
    wolf_wav = generate_halloween_synth("wolf")
    laugh_wav = generate_halloween_synth("laugh")
    ghost_wav = generate_halloween_synth("ghost")

    st.markdown("### 🐺 Creepy Wolf Howl Synth")
    st.audio(f"data:audio/wav;base64,{wolf_wav}", format="audio/wav")
    
    st.markdown("### 😈 Monster Laugh Synth")
    st.audio(f"data:audio/wav;base64,{laugh_wav}", format="audio/wav")
    
    st.markdown("### 👻 Ghost Theremin Sound")
    st.audio(f"data:audio/wav;base64,{ghost_wav}", format="audio/wav")

# --- FOOTER ---
st.markdown("<br><hr><center>Made with 🧡 and 🔮 by a Spooky Developer</center>", unsafe_allow_html=True)
