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

# Unblockable Web Audio API Sound Trigger
def trigger_browser_synth(sound_type):
    if sound_type == "wolf":
        freq_script = "osc.frequency.setValueAtTime(150, ctx.currentTime); osc.frequency.exponentialRampToValueAtTime(300, ctx.currentTime + 0.4); osc.frequency.exponentialRampToValueAtTime(120, ctx.currentTime + 1.2);"
        type_script = "sawtooth"
    elif sound_type == "laugh":
        freq_script = "osc.frequency.setValueAtTime(80, ctx.currentTime); osc.frequency.setValueAtTime(110, ctx.currentTime + 0.15); osc.frequency.setValueAtTime(70, ctx.currentTime + 0.3); osc.frequency.setValueAtTime(100, ctx.currentTime + 0.45); osc.frequency.setValueAtTime(60, ctx.currentTime + 0.6);"
        type_script = "square"
    else: # ghost
        freq_script = "osc.frequency.setValueAtTime(320, ctx.currentTime); osc.frequency.linearRampToValueAtTime(360, ctx.currentTime + 0.3); osc.frequency.linearRampToValueAtTime(280, ctx.currentTime + 0.7); osc.frequency.linearRampToValueAtTime(340, ctx.currentTime + 1.2);"
        type_script = "sine"

    js_html = f"""
    <script>
    (function() {{
        var ctx = new (window.AudioContext || window.webkitAudioContext)();
        var osc = ctx.createOscillator();
        var gain = ctx.createGain();
        
        osc.type = '{type_script}';
        {freq_script}
        
        gain.gain.setValueAtTime(0.15, ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 1.2);
        
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.start();
        osc.stop(ctx.currentTime + 1.2);
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
    st.write("Tap a button below to hear browser-synthesized retro effects instantly!")
    
    c1, c2, c3 = st.columns(3)
    
    with c1:
        if st.button("🐺 Werewolf Howl"):
            st.markdown("### *AWOOOOOOOOO!* 🌕")
            trigger_browser_synth("wolf")
    with c2:
        if st.button("😈 Evil Laugh"):
            st.markdown("### *MWAHAHAHAHA!* 🧛")
            trigger_browser_synth("laugh")
    with c3:
        if st.button("👻 Ghost Theremin"):
            st.markdown("### *BOOOOOOOO!* 🧠")
            trigger_browser_synth("ghost")

# --- FOOTER ---
st.markdown("<br><hr><center>Made with 🧡 and 🔮 by a Spooky Developer</center>", unsafe_allow_html=True)
