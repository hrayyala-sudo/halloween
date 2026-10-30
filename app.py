
import streamlit as st
import random
import json
import time

# ============================================================
# PHANTOM QUEST QUESTIONS
# ============================================================

PHANTOM_QUEST_QUESTIONS = [
    {
        "question": "Bats are blind.",
        "answer": False,
        "hint": "Bats can see, and many also use echolocation."
    },
    {
        "question": "A pumpkin is a fruit.",
        "answer": True,
        "hint": "It grows from a flower and has seeds."
    },
    {
        "question": "The Sun is a star.",
        "answer": True,
        "hint": "It is at the center of our solar system."
    },
    {
        "question": "Spiders have six legs.",
        "answer": False,
        "hint": "Spiders have more legs than insects."
    },
    {
        "question": "Water freezes at 0 degrees Celsius.",
        "answer": True,
        "hint": "Think about the temperature when ice forms."
    },
    {
        "question": "Penguins are mammals.",
        "answer": False,
        "hint": "Penguins have feathers and lay eggs."
    },
    {
        "question": "The Moon makes its own light.",
        "answer": False,
        "hint": "The Moon reflects light from the Sun."
    },
    {
        "question": "An octopus has three hearts.",
        "answer": True,
        "hint": "This sea creature has more than one heart."
    },
    {
        "question": "A year on Earth is about 365 days.",
        "answer": True,
        "hint": "It is how long Earth takes to orbit the Sun."
    },
    {
        "question": "Sound can travel through empty space.",
        "answer": False,
        "hint": "Sound needs something to travel through."
    }
]


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="The Haunted Mansion",
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
    "quest_questions": random.sample(PHANTOM_QUEST_QUESTIONS, 5),
    "quest_message": "",
    "quest_message_type": "",
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
    st.session_state.quest_questions = random.sample(
        PHANTOM_QUEST_QUESTIONS, 5
    )
    st.session_state.quest_message = ""
    st.session_state.quest_message_type = ""
    st.session_state.phantom_quest_completed = False


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

st.title("🎃 The Haunted Mansion 💀")

st.write(
    "Welcome, brave traveler... Enter at your own risk. "
    "The ghosts, witches, and monsters are waiting for you!"
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
    You stand before a mysterious Victorian mansion.

    The wind howls, the trees are swaying, and the moon
    shines brightly over the dark entrance.

    Strange shadows move behind the windows.

    What secrets are hidden inside?
    Use the sidebar to explore the haunted rooms!
    """)

    if st.button("Knock on the Door 🚪"):

        with st.spinner("The door is slowly opening..."):
            time.sleep(1)

        st.error(
            "A mysterious voice whispers: "
            "'Who dares enter my haunted mansion?!'"
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
        "Fill in the blanks to create your own "
        "spooky, funny, or terrifying Halloween story!"
    )

    col1, col2 = st.columns(2)

    with col1:

        protagonist = st.text_input(
            "Main Character's Name",
            value="Count Dracula"
        )

        adjective = st.text_input(
            "Spooky Adjective",
            value="creepy"
        )

        creature = st.text_input(
            "Monster or Creature",
            value="Vampire"
        )

    with col2:

        place = st.text_input(
            "Creepy Place",
            value="The Haunted Castle"
        )

        object_held = st.text_input(
            "An Object",
            value="Magic Wand"
        )

        exclamation = st.text_input(
            "Scared Exclamation",
            value="Help! A Ghost!"
        )

    if st.button("🔮 Conjure Story"):

        story = f"""
        It was a dark and stormy night at {place}.

        {protagonist} was walking through the dark hallway
        when suddenly, a {adjective} {creature}
        appeared from behind a mysterious curtain!

        {protagonist} screamed, dropped their
        {object_held}, and shouted "{exclamation}!"

        The monster began to laugh and chased
        {protagonist} through the haunted castle.

        Just when everything seemed hopeless,
        a friendly witch appeared and cast a spell.

        The monster disappeared in a cloud of purple smoke.

        {protagonist} was safe... for now.

        THE END.
        """

        st.session_state.story_text = story
        st.session_state.story_generated = True

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
        "Reach into the magical candy bowl. "
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
                "text": "A witch has placed a mysterious curse on you! 🪄",
                "icon": "💀"
            }
        ]

        result = random.choice(outcomes)

        st.session_state.last_candy_result = result

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
        "to hear spooky creature sounds!"
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
# PAGE 5: THE GHOST DIMENSION
# ============================================================

elif page == "🌌 The Ghost Dimension":

    if st.session_state.ghost_dimension_unlocked:

        st.header("🌌 Welcome to the Ghost Dimension")

        st.balloons()

        st.write("""
        **Congratulations, Ultimate Mansion Explorer!**

        You have discovered a secret passage leading
        to a mysterious world filled with ghosts.

        The floating spirits welcome you to their dimension.
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
                    "The Grand Phantom has recognized your bravery! 🏆"
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
# GAME 6: PHANTOM QUEST
# ============================================================

elif page == "👻 Phantom Quest":

    if st.session_state.phantom_summoned:

        st.header("👻 Phantom Quest: The Two Haunted Doors")

        st.write("""
        The Grand Phantom has trapped you inside the mansion!

        You will face five true-or-false questions.

        Each question has two doors:

        🚪 TRUE door
        🚪 FALSE door

        Choose the correct door five times in a row to escape!

        Be careful! One wrong answer resets your streak back to zero!
        """)

        st.markdown(
            f"<div class='spooky-box'>"
            f"<h2>Question {st.session_state.quest_round} of 5</h2>"
            f"<h3>🔥 Correct Answers in a Row: "
            f"{st.session_state.quest_score}/5</h3>"
            f"</div>",
            unsafe_allow_html=True
        )

        # Display feedback from the previous answer
        if st.session_state.quest_message:

            if st.session_state.quest_message_type == "success":
                st.success(st.session_state.quest_message)

            elif st.session_state.quest_message_type == "error":
                st.error(st.session_state.quest_message)

        # Victory screen
        if st.session_state.phantom_quest_completed:

            st.success(
                "🎉 YOU ESCAPED! "
                "You answered five questions correctly in a row!"
            )

            st.balloons()

            st.markdown(
                "<div class='spooky-box'>"
                "<h2>🏆 Phantom Quest Champion!</h2>"
                "<p>You outsmarted the Grand Phantom!</p>"
                "</div>",
                unsafe_allow_html=True
            )

            st.info(
                "🎃 Congratulations! "
                "The Haunted Graveyard is now unlocked!"
            )

            if st.button("🔄 Play Phantom Quest Again"):

                reset_phantom_quest()
                st.rerun()

        else:

            # Get the current question
            current_question = st.session_state.quest_questions[
                st.session_state.quest_round - 1
            ]

            st.subheader("👻 The Phantom's Challenge")

            st.markdown(
                f"<div class='spooky-box'>"
                f"<h2>{current_question['question']}</h2>"
                f"</div>",
                unsafe_allow_html=True
            )

            # Display hint
            st.info(
                f"💡 Hint: {current_question['hint']}"
            )

            st.write("Choose the correct door!")

            # Two doors
            col1, col2 = st.columns(2)

            with col1:

                if st.button(
                    "🚪 TRUE",
                    key=f"true_door_{st.session_state.quest_round}",
                    use_container_width=True
                ):

                    if current_question["answer"] is True:

                        st.session_state.quest_score += 1

                        st.session_state.quest_message = (
                            "✨ Correct! The TRUE door opens!"
                        )

                        st.session_state.quest_message_type = "success"

                        if st.session_state.quest_score == 5:

                            st.session_state.phantom_quest_completed = True

                        else:

                            st.session_state.quest_round += 1

                    else:

                        # Wrong answer resets the streak
                        st.session_state.quest_score = 0
                        st.session_state.quest_round = 1

                        # Start with five new random questions
                        st.session_state.quest_questions = random.sample(
                            PHANTOM_QUEST_QUESTIONS, 5
                        )

                        st.session_state.quest_message = (
                            "💀 WRONG DOOR! Your streak is back to zero. "
                            "Try again!"
                        )

                        st.session_state.quest_message_type = "error"

                    st.rerun()

            with col2:

                if st.button(
                    "🚪 FALSE",
                    key=f"false_door_{st.session_state.quest_round}",
                    use_container_width=True
                ):

                    if current_question["answer"] is False:

                        st.session_state.quest_score += 1

                        st.session_state.quest_message = (
                            "✨ Correct! The FALSE door opens!"
                        )

                        st.session_state.quest_message_type = "success"

                        if st.session_state.quest_score == 5:

                            st.session_state.phantom_quest_completed = True

                        else:

                            st.session_state.quest_round += 1

                    else:

                        # Wrong answer resets the streak
                        st.session_state.quest_score = 0
                        st.session_state.quest_round = 1

                        # Start with five new random questions
                        st.session_state.quest_questions = random.sample(
                            PHANTOM_QUEST_QUESTIONS, 5
                        )

                        st.session_state.quest_message = (
                            "💀 WRONG DOOR! Your streak is back to zero. "
                            "Try again!"
                        )

                        st.session_state.quest_message_type = "error"

                    st.rerun()

            st.caption(
                "🚪 TRUE or FALSE? Choose wisely! "
                "You need five correct answers in a row to escape!"
            )

    else:

        st.error("This dimension is still locked!")


# ============================================================
# GAME 7: THE HAUNTED GRAVEYARD
# ============================================================

elif page == "🎃 The Haunted Graveyard":

    if st.session_state.phantom_quest_completed:

        st.header("🎃 The Haunted Graveyard")

        st.write("""
        You escaped the mansion, but your adventure is not over!

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
                "<p>You conquered the mansion, escaped the Phantom, "
                "and solved the graveyard mysteries!</p>"
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

                answer = st.text_input("Your answer:")

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
