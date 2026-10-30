
import streamlit as st
import random
import json
import time

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="The Haunted Streamlit Mansion",
    page_icon="🎃",
    layout="centered",
    initial_sidebar_state="expanded"
)

# ============================================================
# SESSION STATE
# ============================================================

defaults = {
    "egg_porch": False,
    "egg_story": False,
    "egg_candy": False,
    "draw_count": 0,
    "ghost_dimension_unlocked": False,
    "phantom_summoned": False,
    "quest_round": 1,
    "quest_score": 0,
    "quest_safe_door": random.randint(1, 3),
    "quest_failed": False,
    "phantom_quest_completed": False,
    "graveyard_round": 1,
    "graveyard_score": 0,
    "graveyard_completed": False,
    "last_candy_result": None,
    "story_generated": False,
    "story_text": ""
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ============================================================
# CUSTOM HALLOWEEN THEME
# ============================================================

st.markdown("""
<style>
.stApp {
    background-color: #0F0C20;
    background-image: radial-gradient(
        circle,
        #241442 0%,
        #0F0C20 100%
    );
    color: #E0E0E0;
}

h1, h2, h3 {
    color: #FF5E00 !important;
    font-family: 'Courier New', Courier, monospace;
    text-shadow: 2px 2px 4px #000000,
                 0 0 10px #9D00FF;
}

.stButton > button {
    background-color: #9D00FF !important;
    color: white !important;
    border: 2px solid #FF5E00 !important;
    border-radius: 10px;
    font-weight: bold;
    box-shadow: 0 0 8px #9D00FF;
    transition: all 0.3s ease;
}

.stButton > button:hover {
    background-color: #FF5E00 !important;
    border: 2px solid #9D00FF !important;
    box-shadow: 0 0 15px #FF5E00;
    transform: scale(1.05);
}

@keyframes float {
    0% { transform: translate(0, 0px); }
    50% { transform: translate(0, -15px); }
    100% { transform: translate(0, 0px); }
}

.ghost-style {
    font-size: 55px;
    animation: float 3s ease-in-out infinite;
    text-align: center;
}

.spooky-box {
    background-color: #241442;
    border: 2px solid #9D00FF;
    border-radius: 12px;
    padding: 18px;
    margin: 12px 0;
    text-align: center;
}

</style>
""", unsafe_allow_html=True)

# ============================================================
# HELPER FUNCTIONS
# ============================================================

def speak_like_a_monster(text, pitch=0.7, rate=0.8):
    """Use the browser's built-in speech generator."""
    safe_text = json.dumps(text)

    html = f"""
    <script>
    (function() {{
        if ('speechSynthesis' in window) {{
            window.speechSynthesis.cancel();

            var msg = new SpeechSynthesisUtterance({safe_text});
            msg.pitch = {pitch};
            msg.rate = {rate};

            window.speechSynthesis.speak(msg);
        }}
    }})();
    </script>
    """

    st.components.v1.html(html, height=0)


def reset_phantom_quest():
    st.session_state.quest_round = 1
    st.session_state.quest_score = 0
    st.session_state.quest_safe_door = random.randint(1, 3)
    st.session_state.quest_failed = False


def reset_graveyard_game():
    st.session_state.graveyard_round = 1
    st.session_state.graveyard_score = 0
    st.session_state.graveyard_completed = False


# ============================================================
# EASTER EGG STATUS
# ============================================================

all_eggs_found = (
    st.session_state.egg_porch
    and st.session_state.egg_story
    and st.session_state.egg_candy
)

# ============================================================
# HEADER
# ============================================================

st.markdown(
    "<div class='ghost-style'>👻</div>",
    unsafe_allow_html=True
)

st.title("🎃 The Haunted Streamlit Mansion 💀")

st.write(
    "Welcome, brave traveler... Enter at your own risk. "
    "Turn up your imagination and choose your fate below."
)

# ============================================================
# FLOATING GHOST / SECRET ROOM UNLOCK
# ============================================================

if all_eggs_found and not st.session_state.ghost_dimension_unlocked:

    st.success(
        "All 3 Easter eggs have been discovered! "
        "The floating ghost is glowing!"
    )

    if st.button(
        "✨ The Floating Ghost is glowing! CLICK ME! ✨",
        use_container_width=True
    ):
        st.session_state.ghost_dimension_unlocked = True
        st.toast(
            "The air grows cold... A secret room has opened!",
            icon="🔮"
        )
        st.rerun()

if not all_eggs_found:
    discovered = sum([
        st.session_state.egg_porch,
        st.session_state.egg_story,
        st.session_state.egg_candy
    ])

    st.caption(f"🤫 Secrets Discovered: {discovered} / 3")

st.divider()

# ============================================================
# SIDEBAR NAVIGATION
# ============================================================

menu_options = [
    "🚪 Front Porch",
    "📖 Spooky Story Generator",
    "🍬 Trick or Treat Roulette",
    "🔮 Monster Mash Soundboard"
]

if st.session_state.ghost_dimension_unlocked:
    menu_options.append("🌌 The Ghost Dimension")

if st.session_state.phantom_summoned:
    menu_options.append("👻 Phantom Quest")

if st.session_state.phantom_quest_completed:
    menu_options.append("🎃 The Haunted Graveyard")

page = st.sidebar.selectbox(
    "Choose Your Activity:",
    menu_options
)

# ============================================================
# PAGE 1: FRONT PORCH
# ============================================================

if page == "🚪 Front Porch":

    st.header("🚪 Welcome to the Mansion")

    st.markdown(
        "<div class='spooky-box'>"
        "<h2>🏚️ The Haunted Mansion</h2>"
        "<p>The fog rolls in... The door slowly opens...</p>"
        "</div>",
        unsafe_allow_html=True
    )

    st.write("""
    You stand before a creaking, old Victorian mansion.

    The wind howls, and the moon is full.

    What secrets lie within these digital walls?
    Use the sidebar menu to explore the haunted rooms!
    """)

    if st.button("Knock on the Door 🚪"):

        with st.spinner("Creaaaaak..."):
            time.sleep(1)

        st.error(
            "A disembodied voice whispers: "
            "'Who dares disturb the Streamlit code?!'"
        )

        st.balloons()

    st.divider()

    st.subheader("🤫 A Secret Message")

    st.write(
        "The mansion door has a strange inscription. "
        "Perhaps the right words will reveal something..."
    )

    passphrase = st.text_input(
        "Enter the secret passphrase:",
        type="password"
    )

    if st.button("Unlock the Secret"):

        if passphrase.strip().lower() == "neon mint":

            st.session_state.egg_porch = True

            st.success(
                "🎉 Easter Egg #1 discovered! "
                "You found the hidden neon mint secret!"
            )

            st.balloons()

        else:
            st.warning("That is not the secret phrase. Try again!")

    if st.session_state.egg_porch:
        st.success("✅ Easter Egg #1: Discovered!")

# ============================================================
# PAGE 2: SPOOKY STORY GENERATOR
# ============================================================

elif page == "📖 Spooky Story Generator":

    st.header("📜 Create Your Own Spooky Tale")

    st.write(
        "Fill out the blanks to conjure a custom "
        "terrifying or hilarious Halloween story."
    )

    col1, col2 = st.columns(2)

    with col1:
        protagonist = st.text_input(
            "Main Character's Name",
            value="Professor Code"
        )

        adjective = st.text_input(
            "Spooky Adjective",
            value="slimy"
        )

        creature = st.text_input(
            "Monster/Creature",
            value="Python Bug"
        )

    with col2:
        place = st.text_input(
            "Creepy Place",
            value="The Server Room"
        )

        object_held = st.text_input(
            "An Object",
            value="Keyboard"
        )

        exclamation = st.text_input(
            "Scared Exclamation",
            value="Syntax Error!"
        )

    if st.button("🔮 Conjure Story"):

        story = f"""
        It was a dark and stormy night at {place}.

        {protagonist} was minding their own business
        when suddenly, a {adjective} {creature}
        burst through the wall!

        {protagonist} gasped, dropping their
        {object_held} and screaming, "{exclamation}!"

        But it was too late. The {creature} didn't
        want to eat them. It just wanted to review
        their code.

        They lived happily and bug-free ever after.

        THE END.
        """

        st.session_state.story_text = story
        st.session_state.story_generated = True

        # Easter Egg #2
        if protagonist.strip().lower() == "goofy gang":
            st.session_state.egg_story = True

    if st.session_state.story_generated:

        st.info(st.session_state.story_text)

    if protagonist.strip().lower() == "goofy gang":

        st.success(
            "🎉 Easter Egg #2 discovered! "
            "The legendary Goofy Gang has entered the mansion!"
        )

        st.session_state.egg_story = True

    if st.session_state.egg_story:
        st.success("✅ Easter Egg #2: Discovered!")

# ============================================================
# PAGE 3: TRICK OR TREAT ROULETTE
# ============================================================

elif page == "🍬 Trick or Treat Roulette":

    st.header("🍬 Trick or Treat Roulette")

    st.write(
        "Reach into the digital candy bowl. "
        "Will you get a delicious treat or a devious trick?"
    )

    st.markdown(
        "<div class='spooky-box'>"
        "<h2>🍬 The Magical Candy Bowl</h2>"
        "<p>Choose wisely... You never know what is inside!</p>"
        "</div>",
        unsafe_allow_html=True
    )

    st.write(
        f"🎯 Candy draws: {st.session_state.draw_count}"
    )

    if st.button("🎃 Draw from the Bowl 🍬"):

        st.session_state.draw_count += 1

        outcomes = [
            {
                "type": "Treat",
                "text": "You got a King-Sized Peanut Butter Cup! 🍫",
                "icon": "🎉"
            },
            {
                "type": "Treat",
                "text": "Sour Patch Kids that taste like green apples!",
                "icon": "🍭"
            },
            {
                "type": "Trick",
                "text": "A spider crawls out of the bowl! 🕷️ Run!",
                "icon": "😱"
            },
            {
                "type": "Trick",
                "text": "You got dental floss and a bruised apple.",
                "icon": "😒"
            },
            {
                "type": "Trick",
                "text": "Your path has been cursed! 🔮",
                "icon": "💀"
            }
        ]

        result = random.choice(outcomes)

        st.session_state.last_candy_result = result

        # Easter Egg #3
        if st.session_state.draw_count >= 5:
            st.session_state.egg_candy = True

    if st.session_state.last_candy_result:

        result = st.session_state.last_candy_result

        if result["type"] == "Treat":
            st.success(
                f"{result['icon']} {result['text']}"
            )
            st.snow()

        else:
            st.error(
                f"{result['icon']} {result['text']}"
            )

    if st.session_state.egg_candy:

        st.success(
            "💀 EASTER EGG #3 UNLOCKED! "
            "You discovered the hidden golden skull token!"
        )

    st.caption(
        f"Draws remaining to discover the secret: "
        f"{max(0, 5 - st.session_state.draw_count)}"
    )

# ============================================================
# PAGE 4: MONSTER MASH SOUNDBOARD
# ============================================================

elif page == "🔮 Monster Mash Soundboard":

    st.header("🎵 The Monster Mash Board")

    st.write(
        "Turn up your speakers and click a button "
        "to hear pure creature effects!"
    )

    c1, c2, c3 = st.columns(3)

    with c1:

        if st.button("🐺 Werewolf"):

            st.write("🐺 AWOOOOOOOOO!")

            speak_like_a_monster(
                "Ah-wwooooo! Ow-ow-ow-wwoooo! Grrrr.",
                0.2,
                0.7
            )

    with c2:

        if st.button("🧛 Vampire"):

            st.write("🧛 Mwahahahahaha!")

            speak_like_a_monster(
                "Mwahahahahaha! Ahahahaha!",
                0.5,
                0.85
            )

    with c3:

        if st.button("🧟 Zombie"):

            st.write("🧟 Braaaaains...")

            speak_like_a_monster(
                "Uuuuuurrrrgh. Grrrrroaaaannn. Hhhhungggerrr.",
                0.1,
                0.4
            )

# ============================================================
# SECRET PAGE 5: THE GHOST DIMENSION
# ============================================================

elif page == "🌌 The Ghost Dimension":

    if st.session_state.ghost_dimension_unlocked:

        st.header("🌌 Room Unlocked: The Ghost Dimension")

        st.balloons()

        st.write("""
        **Congratulations, Ultimate Mansion Explorer!**

        You have broken through the code layout logic.

        The floating ghost welcomes you to the infinite digital ether.
        """)

        st.markdown(
            "<div class='spooky-box'>"
            "<h2>🔮 The Grand Phantom Awaits</h2>"
            "<p>Only the bravest explorers may summon the Grand Phantom.</p>"
            "</div>",
            unsafe_allow_html=True
        )

        if not st.session_state.phantom_summoned:

            if st.button(
                "🔮 Summon The Grand Phantom Presence",
                use_container_width=True
            ):

                st.session_state.phantom_summoned = True

                speak_like_a_monster(
                    "WwooooooOooooo! "
                    "You have summoned the Grand Phantom!",
                    1.2,
                    0.7
                )

                st.success(
                    "The Grand Phantom has recognized your achievement! 🏆"
                )

                st.balloons()
                st.rerun()

        else:

            st.success(
                "🏆 The Grand Phantom has been summoned!"
            )

            st.info(
                "A new challenge has appeared in your sidebar: "
                "👻 Phantom Quest!"
            )

    else:

        st.error("This dimension is still locked!")

# ============================================================
# SECRET GAME 6: PHANTOM QUEST
# ============================================================

elif page == "👻 Phantom Quest":

    if st.session_state.phantom_summoned:

        st.header("👻 Phantom Quest: Escape the Mansion")

        st.write("""
        The Grand Phantom has challenged you!

        You must escape through three haunted doors.

        One door is safe. The other two contain terrifying surprises.

        Choose carefully!
        """)

        st.markdown(
            f"<div class='spooky-box'>"
            f"<h2>Round {st.session_state.quest_round} of 3</h2>"
            f"<h3>🏆 Score: {st.session_state.quest_score}/3</h3>"
            f"</div>",
            unsafe_allow_html=True
        )

        if st.session_state.quest_failed:

            st.error(
                "💀 You entered the wrong door! "
                "The ghosts have captured you!"
            )

            if st.button("🔄 Try Phantom Quest Again"):

                reset_phantom_quest()
                st.rerun()

        elif st.session_state.phantom_quest_completed:

            st.success(
                "🎉 You escaped the mansion! "
                "You have completed Phantom Quest!"
            )

            st.balloons()

            st.info(
                "🎃 A new adventure has unlocked: "
                "The Haunted Graveyard!"
            )

        else:

            st.subheader("🚪 Choose Your Door")

            col1, col2, col3 = st.columns(3)

            doors = [
                (col1, 1, "🚪 Door 1"),
                (col2, 2, "🚪 Door 2"),
                (col3, 3, "🚪 Door 3")
            ]

            for col, door_number, label in doors:

                with col:

                    if st.button(
                        label,
                        key=f"quest_door_{st.session_state.quest_round}_{door_number}",
                        use_container_width=True
                    ):

                        if door_number == st.session_state.quest_safe_door:

                            st.session_state.quest_score += 1

                            if st.session_state.quest_round >= 3:

                                st.session_state.phantom_quest_completed = True

                            else:

                                st.session_state.quest_round += 1

                                st.session_state.quest_safe_door = (
                                    random.randint(1, 3)
                                )

                            st.success(
                                "✨ You found the safe door! "
                                "The ghosts let you pass."
                            )

                        else:

                            st.session_state.quest_failed = True

                        st.rerun()

            st.caption(
                "One door is safe. Two doors are haunted. "
                "Choose wisely!"
            )

# ============================================================
# SECRET GAME 7: THE HAUNTED GRAVEYARD
# ============================================================

elif page == "🎃 The Haunted Graveyard":

    if st.session_state.phantom_quest_completed:

        st.header("🎃 The Haunted Graveyard")

        st.write("""
        You escaped the mansion, but your adventure is not over.

        The Grand Phantom has transported you to an ancient graveyard.

        Three mysterious riddles guard the hidden treasure.

        Solve them all to become the Master of the Haunted Graveyard!
        """)

        riddles = [
            {
                "question": "I have a face and two hands, but no arms or legs. What am I?",
                "answers": ["clock"],
                "hint": "You can find me on a wall."
            },
            {
                "question": "The more you take, the more you leave behind. What are they?",
                "answers": ["footsteps", "footstep"],
                "hint": "You make them when you walk."
            },
            {
                "question": "I am full of keys but cannot open a single door. What am I?",
                "answers": ["piano"],
                "hint": "I make music."
            }
        ]

        if st.session_state.graveyard_completed:

            st.success(
                "🏆 YOU ARE THE MASTER OF THE HAUNTED GRAVEYARD!"
            )

            st.balloons()

            st.markdown(
                "<div class='spooky-box'>"
                "<h2>👑 Halloween Champion</h2>"
                "<p>You conquered the mansion, "
                "escaped the Phantom, and solved the graveyard mysteries!</p>"
                "</div>",
                unsafe_allow_html=True
            )

            st.write(
                f"Your final score: "
                f"{st.session_state.graveyard_score}/3"
            )

            if st.button("🔄 Play Haunted Graveyard Again"):

                reset_graveyard_game()
                st.rerun()

        else:

            current_round = st.session_state.graveyard_round
            riddle = riddles[current_round - 1]

            st.markdown(
                f"<div class='spooky-box'>"
                f"<h2>⚰️ Riddle {current_round} of 3</h2>"
                f"<h3>🏆 Score: "
                f"{st.session_state.graveyard_score}/3</h3>"
                f"</div>",
                unsafe_allow_html=True
            )

            st.subheader("🧩 Solve the Mystery")

            st.write(riddle["question"])

            with st.form(
                key=f"graveyard_riddle_{current_round}"
            ):

                answer = st.text_input(
                    "Your answer:"
                )

                submitted = st.form_submit_button(
                    "🔮 Submit Answer"
                )

            if submitted:

                if answer.strip().lower() in riddle["answers"]:

                    st.session_state.graveyard_score += 1

                    st.success(
                        "🎉 Correct! The graveyard spirits are impressed!"
                    )

                    if current_round == 3:

                        st.session_state.graveyard_completed = True

                    else:

                        st.session_state.graveyard_round += 1

                    st.rerun()

                else:

                    st.error(
                        "💀 Not quite! The spirits are not convinced."
                    )

                    st.info(
                        f"💡 Hint: {riddle['hint']}"
                    )

    else:

        st.error(
            "This adventure is locked! "
            "Complete Phantom Quest first."
        )

# ============================================================
# FOOTER
# ============================================================

st.divider()

st.markdown(
    """
    <center>
    <p>🎃 Made with 🧡 and 🔮 by a Spooky Developer</p>
    <p>👻 Beware... The Mansion is always watching!</p>
    </center>
    """,
    unsafe_allow_html=True
)
