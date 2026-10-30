
import json
import random
import time

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="The Haunted Streamlit Mansion",
    page_icon="🎃",
    layout="wide",
)

# -------------------- SESSION STATE --------------------
DEFAULTS = {
    "egg_porch": False,
    "egg_story": False,
    "egg_candy": False,
    "draw_count": 0,
    "ghost_dimension_unlocked": False,
    "quest_round": 1,
    "quest_score": 0,
    "quest_over": False,
    "quest_safe_door": None,
    "quest_message": "",
}

for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value


# -------------------- THEME --------------------
st.markdown(
    """
    <style>
    .stApp {
        background: radial-gradient(circle, #241442 0%, #0F0C20 100%);
        color: #E0E0E0;
    }

    h1, h2, h3 {
        color: #FF7A1A !important;
        font-family: "Courier New", monospace;
        text-shadow: 2px 2px 4px #000, 0 0 10px #9D00FF;
    }

    .stButton > button {
        background: #7900C8;
        color: white;
        border: 2px solid #FF7A1A;
        border-radius: 10px;
        font-weight: 700;
        box-shadow: 0 0 8px #7900C8;
        transition: all .2s ease;
    }

    .stButton > button:hover {
        background: #FF7A1A;
        color: white;
        border-color: #9D00FF;
        transform: scale(1.02);
    }

    .ghost {
        font-size: 54px;
        text-align: center;
        animation: float 3s ease-in-out infinite;
    }

    @keyframes float {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-14px); }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# -------------------- MONSTER VOICE FUNCTION --------------------
def speak_like_a_monster(message: str, pitch: float, rate: float) -> None:
    """Use browser speech synthesis instead of external audio files."""

    safe_message = json.dumps(message)

    html = f"""
    <script>
    (() => {{
        if (!("speechSynthesis" in window)) return;

        window.speechSynthesis.cancel();

        const utterance = new SpeechSynthesisUtterance({safe_message});
        utterance.pitch = {pitch};
        utterance.rate = {rate};

        window.speechSynthesis.speak(utterance);
    }})();
    </script>
    """

    components.html(html, height=0)


# -------------------- HEADER / EASTER EGGS --------------------
all_eggs_found = (
    st.session_state.egg_porch
    and st.session_state.egg_story
    and st.session_state.egg_candy
)

st.markdown('<div class="ghost">👻</div>', unsafe_allow_html=True)

if all_eggs_found and not st.session_state.ghost_dimension_unlocked:
    if st.button(
        "✨ The Floating Ghost is glowing! Click me! ✨",
        use_container_width=True,
    ):
        st.session_state.ghost_dimension_unlocked = True
        st.toast("A secret room has opened in the sidebar!", icon="🔮")
        st.rerun()

st.title("🎃 The Haunted Streamlit Mansion 💀")

st.write(
    "Welcome, brave traveler... Enter at your own risk. "
    "Choose your fate using the menu on the left."
)

if not all_eggs_found:
    discovered = sum([
        st.session_state.egg_porch,
        st.session_state.egg_story,
        st.session_state.egg_candy,
    ])
    st.caption(f"🤫 Secrets discovered: {discovered} / 3")

elif not st.session_state.ghost_dimension_unlocked:
    st.info("You found all three Easter eggs! Click the glowing ghost above.")

st.divider()


# -------------------- NAVIGATION --------------------
menu_options = [
    "🚪 Front Porch",
    "📖 Spooky Story Generator",
    "🍬 Trick or Treat Roulette",
    "🔮 Monster Mash Soundboard",
]

if st.session_state.ghost_dimension_unlocked:
    menu_options.append("🌌 The Ghost Dimension")
    menu_options.append("👑 Phantom Quest: Escape the Mansion")

page = st.sidebar.selectbox(
    "Choose Your Activity:",
    menu_options,
)


# -------------------- PAGE 1: FRONT PORCH --------------------
if page == "🚪 Front Porch":

    st.header("Welcome to the Mansion")

    st.markdown(
        """
        <div style="font-size:100px;text-align:center;">
            🏚️ 🌕 🦇
        </div>
        <div style="text-align:center;font-size:20px;">
            The fog rolls in... and something is moving behind the windows.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write(
        "You stand before a creaking, old Victorian mansion. "
        "The wind howls, and the moon is full. What secrets lie within?"
    )

    secret_knock = st.text_input(
        "Psst... do you know the secret passphrase?",
        placeholder="Type here...",
    )

    if (
        secret_knock.strip().lower() == "neon mint"
        and not st.session_state.egg_porch
    ):
        st.session_state.egg_porch = True
        st.rerun()

    if st.session_state.egg_porch:
        st.success("🌟 Easter egg unlocked: The walls glow bright green!")

    if st.button("Knock on the Door 🚪"):
        with st.spinner("Creaaaaak..."):
            time.sleep(1)

        st.error(
            "A disembodied voice whispers: "
            "'Who dares disturb the mansion?!'"
        )
        st.balloons()


# -------------------- PAGE 2: STORY GENERATOR --------------------
elif page == "📖 Spooky Story Generator":

    st.header("📜 Create Your Own Spooky Tale")
    st.write("Fill in the blanks to conjure a custom Halloween story.")

    col1, col2 = st.columns(2)

    with col1:
        protagonist = st.text_input(
            "Main character's name",
            value="Brave Traveler",
        )
        adjective = st.text_input(
            "Spooky adjective",
            value="slimy",
        )
        creature = st.text_input(
            "Monster or creature",
            value="Shadow Beast",
        )

    with col2:
        place = st.text_input(
            "Creepy place",
            value="The Graveyard",
        )
        object_held = st.text_input(
            "An object",
            value="Flashlight",
        )
        exclamation = st.text_input(
            "Scared exclamation",
            value="Help me!",
        )

    if (
        protagonist.strip().lower() == "goofy gang"
        and not st.session_state.egg_story
    ):
        st.session_state.egg_story = True
        st.rerun()

    if st.session_state.egg_story:
        st.warning(
            "👾 Easter egg unlocked: Welcome to the Goofy Gang sanctuary!"
        )

    if st.button("🔮 Conjure Story"):

        story = (
            f"It was a dark and stormy night at **{place}**. "
            f"**{protagonist}** was minding their own business when suddenly, "
            f"a **{adjective} {creature}** burst through the shadows! "
            f"**{protagonist}** dropped their **{object_held}** and screamed, "
            f"**'{exclamation}'** They ran as fast as they could. The End."
        )

        st.info(story)


# -------------------- PAGE 3: TRICK OR TREAT --------------------
elif page == "🍬 Trick or Treat Roulette":

    st.header("🍬 Trick or Treat Roulette")

    st.write(
        "Reach into the digital candy bowl. "
        "Will you get a treat or a trick?"
    )

    if st.button("🎃 Draw from the Bowl 🍬"):

        st.session_state.draw_count += 1

        if (
            st.session_state.draw_count >= 5
            and not st.session_state.egg_candy
        ):
            st.session_state.egg_candy = True
            st.rerun()

        outcomes = [
            (
                "Treat",
                "King-sized peanut butter cup! 🍫 (+100 Spooky Points)",
                "🎉",
            ),
            (
                "Treat",
                "Sour candy that tastes like green apples! 🍏",
                "🍭",
            ),
            (
                "Trick",
                "A spider crawls out of the bowl! 🕷️ Run!",
                "😱",
            ),
            (
                "Trick",
                "You got dental floss and a bruised apple. BOOO!",
                "😒",
            ),
            (
                "Trick",
                "Your path has been cursed! Everything is upside down. 🪄",
                "🔮",
            ),
        ]

        kind, result, icon = random.choice(outcomes)

        if kind == "Treat":
            st.success(f"{icon} {result}")
            st.snow()
        else:
            st.error(f"{icon} {result}")

    st.caption(f"Draws so far: {st.session_state.draw_count}")

    if st.session_state.egg_candy:
        st.warning(
            "💀 Easter egg unlocked: "
            "You found the hidden golden skull token!"
        )


# -------------------- PAGE 4: MONSTER MASH SOUNDBOARD --------------------
elif page == "🔮 Monster Mash Soundboard":

    st.header("🎵 The Monster Mash Soundboard")

    st.write(
        "Turn up your speakers and click a button to hear creature effects."
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        if st.button("🐺 Werewolf", use_container_width=True):
            st.write("🐺 *AWOOOOOOOOO!*")
            speak_like_a_monster(
                "Ah-wwooooo! Ow-ow-ow-wwoooo! Grrrr.",
                0.2,
                0.7,
            )

    with c2:
        if st.button("🧛 Vampire", use_container_width=True):
            st.write("🧛 *Mwahahahahaha!*")
            speak_like_a_monster(
                "Mwahahahahaha! Ahahahaha!",
                0.5,
                0.85,
            )

    with c3:
        if st.button("🧟 Zombie", use_container_width=True):
            st.write("🧟 *Braaaaains...*")
            speak_like_a_monster(
                "Uuuuuurrrrgh. Grrrrroaaaannn. Hhhhungggerrr.",
                0.1,
                0.4,
            )

    st.caption(
        "Sound playback uses your browser's speech synthesis. "
        "Some browsers require interaction before audio can play."
    )


# -------------------- PAGE 5: SECRET GHOST DIMENSION --------------------
elif page == "🌌 The Ghost Dimension":

    if st.session_state.ghost_dimension_unlocked:

        st.header("🌌 Room Unlocked: The Ghost Dimension")

        st.balloons()

        st.write(
            "**Congratulations, Ultimate Mansion Explorer!** "
            "You have discovered the secret room. "
            "The floating ghost welcomes you to the infinite digital ether."
        )

        st.markdown(
            '<div style="font-size:100px;text-align:center;">'
            '👻 ✨ 🌌'
            '</div>',
            unsafe_allow_html=True,
        )

        if st.button("🔮 Summon The Grand Phantom Presence"):

            speak_like_a_monster(
                "WwooooooOooooo. You have discovered the final room. "
                "Master programmer. Goodbye.",
                1.2,
                0.7,
            )

            st.success(
                "The Grand Phantom recognizes your achievement! 🏆"
            )

    else:
        st.warning(
            "This room is still locked. Find all three Easter eggs first."
        )


# -------------------- PAGE 6: PHANTOM QUEST --------------------
elif page == "👑 Phantom Quest: Escape the Mansion":

    st.header("👑 Phantom Quest: Escape the Mansion")

    st.write(
        "The Grand Phantom has opened one final challenge. "
        "Choose the safe door in each room and escape the mansion!"
    )

    st.markdown(
        '<div style="font-size:75px;text-align:center;">'
        '🚪 🕯️ 👻 🚪'
        '</div>',
        unsafe_allow_html=True,
    )

    if (
        st.session_state.quest_safe_door is None
        and not st.session_state.quest_over
    ):
        st.session_state.quest_safe_door = random.choice(
            ["Left", "Middle", "Right"]
        )

    st.progress(min(st.session_state.quest_round - 1, 3) / 3)

    st.write(
        f"**Room {min(st.session_state.quest_round, 3)} of 3**"
    )

    st.write(
        f"**Phantom points:** {st.session_state.quest_score}"
    )

    if st.session_state.quest_over:

        if st.session_state.quest_score == 3:
            st.success(
                "🏆 Perfect escape! You outsmarted the Grand Phantom!"
            )
            st.balloons()

        else:
            st.success(
                f"You escaped the mansion with "
                f"{st.session_state.quest_score} out of 3 phantom points!"
            )

        if st.button("🔁 Play Phantom Quest Again"):

            st.session_state.quest_round = 1
            st.session_state.quest_score = 0
            st.session_state.quest_over = False

            st.session_state.quest_safe_door = random.choice(
                ["Left", "Middle", "Right"]
            )

            st.session_state.quest_message = ""

            st.rerun()

    else:

        st.info(
            "One door is safe. The other two are haunted. Choose wisely!"
        )

        door_cols = st.columns(3)

        doors = ["Left", "Middle", "Right"]

        door_emojis = [
            "🚪 Left Door",
            "🚪 Middle Door",
            "🚪 Right Door",
        ]

        for col, door, label in zip(
            door_cols,
            doors,
            door_emojis,
        ):

            with col:

                if st.button(
                    label,
                    key=f"quest_{st.session_state.quest_round}_{door}",
                    use_container_width=True,
                ):

                    if door == st.session_state.quest_safe_door:

                        st.session_state.quest_score += 1

                        st.session_state.quest_message = (
                            f"✨ Correct! The {door.lower()} door was safe. "
                            "The ghost lets you pass!"
                        )

                    else:

                        st.session_state.quest_message = (
                            f"👻 Oh no! The {door.lower()} door was haunted. "
                            f"The safe door was "
                            f"{st.session_state.quest_safe_door.lower()}."
                        )

                    st.session_state.quest_round += 1

                    if st.session_state.quest_round > 3:
                        st.session_state.quest_over = True

                    else:
                        st.session_state.quest_safe_door = random.choice(
                            ["Left", "Middle", "Right"]
                        )

                    st.rerun()

        if st.session_state.quest_message:
            st.warning(st.session_state.quest_message)


# -------------------- FOOTER --------------------
st.divider()

st.markdown(
    """
    <div style="text-align:center;">
        Made with 🧡 and 🔮 by a Spooky Developer
    </div>
    """,
    unsafe_allow_html=True,
)
