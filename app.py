import streamlit as st
import random
import json
import time
import math
import streamlit.components.v1 as components

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
# PHANTOM QUEST QUESTIONS
# ============================================================

PHANTOM_QUEST_QUESTIONS = [
    {"question": "A pumpkin is a fruit.", "answer": True},
    {"question": "Bats are completely blind.", "answer": False},
    {"question": "The Sun is a star.", "answer": True},
    {"question": "Spiders have six legs.", "answer": False},
    {"question": "Water freezes at 0 degrees Celsius.", "answer": True},
    {"question": "Penguins are mammals.", "answer": False},
    {"question": "The Moon makes its own light.", "answer": False},
    {"question": "An octopus has three hearts.", "answer": True},
    {"question": "A year on Earth is about 365 days.", "answer": True},
    {"question": "Sound can travel through empty space.", "answer": False},
]

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
    "quest_questions": None,
    "quest_failed": False,
    "phantom_quest_completed": False,
    "graveyard_round": 1,
    "graveyard_score": 0,
    "graveyard_completed": False,
    "last_candy_result": None,
    "story_generated": False,
    "story_text": "",
    "arcade_unlocked": False,
    "pm_x": 2,
    "pm_y": 2,
    "ghost_x": 4,
    "ghost_y": 4,
    "is_super_mode": False,
    "super_mode_timer": 0,
    "pm_score": 0,
    "orbs_active": {"Orb1": True, "Orb2": True, "Orb3": True, "Orb4": True},
    "pm_game_over": False,
    # Normal Goofy Gang Pac-Man: 5x5 candy grid and four ghosts.
    "pac_x": 2,
    "pac_y": 4,
    "pac_score": 0,
    "pac_game_grid": [["🍬" for _ in range(5)] for _ in range(5)],
    "pac_ghosts": [
        {"x": 0, "y": 0, "color": "🔴"},
        {"x": 4, "y": 0, "color": "💖"},
        {"x": 0, "y": 2, "color": "🔵"},
        {"x": 4, "y": 2, "color": "🧡"}
    ],
    "pac_game_won": False,
    "pac_last_event": "",
    "tetris_board": [["⬛" for _ in range(6)] for _ in range(10)],
    "piece_x": 2,
    "piece_y": 0,
    "tetris_score": 0,
    "active_shape": "🟦",
    "tetris_piece": None,
    "tetris_game_over": False,
    "tetris_lines": 0,
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ============================================================
# TETRIS SHAPES
# ============================================================

TETROMINOES = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[0, 1, 0], [1, 1, 1]],
    [[0, 1, 1], [1, 1, 0]],
    [[1, 1, 0], [0, 1, 1]],
    [[1, 0, 0], [1, 1, 1]],
    [[0, 0, 1], [1, 1, 1]],
]

if st.session_state.tetris_piece is None:
    st.session_state.tetris_piece = random.choice(TETROMINOES)

# ============================================================
# CUSTOM HALLOWEEN THEME
# ============================================================

st.markdown("""
<style>
.stApp {
    background-color: #0F0C20;
    background-image: radial-gradient(circle, #241442 0%, #0F0C20 100%);
    color: #E0E0E0;
}
h1, h2, h3 {
    color: #FF5E00 !important;
    font-family: 'Courier New', Courier, monospace;
    text-shadow: 2px 2px 4px #000000, 0 0 10px #9D00FF;
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
    components.html(html, height=0)


def reset_phantom_quest():
    st.session_state.quest_round = 1
    st.session_state.quest_score = 0
    st.session_state.quest_questions = random.sample(
        PHANTOM_QUEST_QUESTIONS, 5
    )
    st.session_state.quest_failed = False
    st.session_state.phantom_quest_completed = False


def reset_graveyard_game():
    st.session_state.graveyard_round = 1
    st.session_state.graveyard_score = 0
    st.session_state.graveyard_completed = False


# ============================================================
# TETRIS GAME FUNCTIONS
# ============================================================

def tetris_fits(shape, x, y):
    board = st.session_state.tetris_board

    for row_index, row in enumerate(shape):
        for col_index, cell in enumerate(row):
            if not cell:
                continue

            board_x = x + col_index
            board_y = y + row_index

            if board_x < 0 or board_x >= 6 or board_y >= 10:
                return False

            if board_y >= 0 and board[board_y][board_x] != "⬛":
                return False

    return True


def tetris_spawn_piece():
    st.session_state.tetris_piece = random.choice(TETROMINOES)
    st.session_state.active_shape = random.choice(
        ["🟧", "🟪", "🟦", "🟩"]
    )
    st.session_state.piece_x = 2
    st.session_state.piece_y = 0

    if not tetris_fits(
        st.session_state.tetris_piece,
        st.session_state.piece_x,
        st.session_state.piece_y
    ):
        st.session_state.tetris_game_over = True


def tetris_lock_piece():
    board = st.session_state.tetris_board
    shape = st.session_state.tetris_piece

    for row_index, row in enumerate(shape):
        for col_index, cell in enumerate(row):
            if cell:
                board_y = st.session_state.piece_y + row_index
                board_x = st.session_state.piece_x + col_index

                if board_y < 0:
                    st.session_state.tetris_game_over = True
                    return

                board[board_y][board_x] = st.session_state.active_shape

    remaining_rows = [
        row for row in board
        if any(cell == "⬛" for cell in row)
    ]

    cleared = 10 - len(remaining_rows)

    if cleared:
        st.session_state.tetris_board = (
            [["⬛" for _ in range(6)] for _ in range(cleared)]
            + remaining_rows
        )

        points = [0, 100, 300, 500, 800][min(cleared, 4)]
        st.session_state.tetris_score += points
        st.session_state.tetris_lines += cleared

        st.toast(
            f"{cleared} row(s) cleared! +{points} points",
            icon="🔥"
        )

    tetris_spawn_piece()


def tetris_gravity_step():
    if st.session_state.tetris_game_over:
        return

    next_y = st.session_state.piece_y + 1

    if tetris_fits(
        st.session_state.tetris_piece,
        st.session_state.piece_x,
        next_y
    ):
        st.session_state.piece_y = next_y
    else:
        tetris_lock_piece()


def tetris_rotate_piece():
    shape = st.session_state.tetris_piece

    rotated = [
        list(row) for row in zip(*shape[::-1])
    ]

    for offset in (0, -1, 1, -2, 2):
        if tetris_fits(
            rotated,
            st.session_state.piece_x + offset,
            st.session_state.piece_y
        ):
            st.session_state.tetris_piece = rotated
            st.session_state.piece_x += offset
            return


def reset_tetris_game():
    st.session_state.tetris_board = [
        ["⬛" for _ in range(6)] for _ in range(10)
    ]
    st.session_state.piece_x = 2
    st.session_state.piece_y = 0
    st.session_state.tetris_piece = random.choice(TETROMINOES)
    st.session_state.active_shape = random.choice(
        ["🟧", "🟪", "🟦", "🟩"]
    )
    st.session_state.tetris_score = 0
    st.session_state.tetris_lines = 0
    st.session_state.tetris_game_over = False


# ============================================================
# UNLOCK STATUS
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
    "<div style='font-size:55px;text-align:center;'>👻</div>",
    unsafe_allow_html=True
)

st.title("🎃 The Haunted Mansion 💀")

st.write(
    "Welcome, brave traveler... Enter at your own risk. "
    "The ghosts, witches, and monsters are waiting for you!"
)

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

if st.session_state.arcade_unlocked:
    menu_options.append("🟡 Pac-Man Arcade")
    menu_options.append("🕹️ Pac-Man 67 Station")
    menu_options.append("🧩 Goofy Gang Tetris")

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

        if st.session_state.graveyard_completed:
            st.session_state.arcade_unlocked = True
            st.success(
                "👑 The monster bows and welcomes you back! "
                "Both arcade stations are now unlocked in the sidebar."
            )
            st.balloons()
            st.rerun()
        else:
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

    st.write(f"🎯 Candy draws: {st.session_state.draw_count}")

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
            st.success(f"{result['icon']} {result['text']}")
            st.snow()
        else:
            st.error(f"{result['icon']} {result['text']}")

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
            st.success("🏆 The Grand Phantom has been summoned!")
            st.info(
                "A new challenge has appeared in your sidebar: "
                "👻 Phantom Quest!"
            )
    else:
        st.error("This dimension is still locked!")


# ============================================================
# GAME 6: PHANTOM QUEST — NO HINTS
# ============================================================

elif page == "👻 Phantom Quest":
    if st.session_state.phantom_summoned:
        st.header("👻 Phantom Quest: True or False")

        st.write("""
        The Grand Phantom has challenged you!

        Answer five true-or-false questions correctly in a row
        to escape the mansion. Choose one of the two doors:
        TRUE or FALSE.
        """)

        st.markdown(
            f"<div class='spooky-box'>"
            f"<h2>Question {st.session_state.quest_round} of 5</h2>"
            f"<h3>🏆 Correct Answers in a Row: "
            f"{st.session_state.quest_score}/5</h3>"
            f"</div>",
            unsafe_allow_html=True
        )

        if st.session_state.quest_failed:
            st.error(
                "💀 Incorrect answer! Your streak has ended. "
                "The ghosts have sent you back to the beginning!"
            )

            if st.button("🔄 Try Phantom Quest Again"):
                reset_phantom_quest()
                st.rerun()

        elif st.session_state.phantom_quest_completed:
            st.success(
                "🎉 You escaped the mansion! "
                "You answered five questions correctly in a row!"
            )
            st.balloons()

            st.info(
                "🎃 A new adventure has unlocked: "
                "The Haunted Graveyard!"
            )

            if st.button("🔄 Play Phantom Quest Again"):
                reset_phantom_quest()
                st.rerun()

        else:
            current_question = st.session_state.quest_questions[
                st.session_state.quest_round - 1
            ]

            st.subheader("❓ True or False?")

            st.markdown(
                f"<div class='spooky-box'>"
                f"<h3>{current_question['question']}</h3>"
                f"</div>",
                unsafe_allow_html=True
            )

            col1, col2 = st.columns(2)

            with col1:
                if st.button(
                    "🚪 TRUE",
                    key=f"quest_true_{st.session_state.quest_round}",
                    use_container_width=True
                ):
                    if current_question["answer"] is True:
                        st.session_state.quest_score += 1

                        if st.session_state.quest_score == 5:
                            st.session_state.phantom_quest_completed = True
                        else:
                            st.session_state.quest_round += 1
                    else:
                        st.session_state.quest_failed = True

                    st.rerun()

            with col2:
                if st.button(
                    "🚪 FALSE",
                    key=f"quest_false_{st.session_state.quest_round}",
                    use_container_width=True
                ):
                    if current_question["answer"] is False:
                        st.session_state.quest_score += 1

                        if st.session_state.quest_score == 5:
                            st.session_state.phantom_quest_completed = True
                        else:
                            st.session_state.quest_round += 1
                    else:
                        st.session_state.quest_failed = True

                    st.rerun()
    else:
        st.error("This dimension is still locked!")


# ============================================================
# GAME 7: THE HAUNTED GRAVEYARD — NO HINTS
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
            },
            {
                "question": "The more you take, the more you leave behind. What are they?",
                "answers": ["footsteps", "footstep"],
            },
            {
                "question": "I am full of keys but cannot open a single door. What am I?",
                "answers": ["piano"],
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

            with st.form(key=f"graveyard_riddle_{current_round}"):
                answer = st.text_input("Your answer:")
                submitted = st.form_submit_button("🔮 Submit Answer")

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
    else:
        st.error(
            "This adventure is locked! "
            "Complete Phantom Quest first."
        )


# ============================================================
# PAC-MAN ARCADE — SMOOTH CLASSIC PAC-MAN
# ============================================================

elif page == "🟡 Pac-Man Arcade":
    if not st.session_state.arcade_unlocked:
        st.error("Complete the Haunted Graveyard to unlock the arcade.")
    else:
        st.header("🟡 Classic Pac-Man Arcade")

        st.write(
            "Eat the dots, collect power pellets, avoid the ghosts, "
            "and clear the maze!"
        )

        # The game runs in the browser for smooth animation.
        pacman_html = r"""
        <div id="pacman-app">
          <div class="hud">
            <div>SCORE <span id="score">0</span></div>
            <div>HIGH SCORE <span id="highscore">0</span></div>
            <div>LIVES <span id="lives">3</span></div>
          </div>
          <canvas id="game" width="560" height="620"></canvas>
          <div class="controls">
            <button data-dir="up">▲</button>
            <div>
              <button data-dir="left">◀</button>
              <button data-dir="down">▼</button>
              <button data-dir="right">▶</button>
            </div>
          </div>
          <div class="game-actions">
            <button id="start">NEW GAME</button>
            <span id="message">Use arrow keys or WASD to move</span>
          </div>
        </div>
        <style>
          #pacman-app {
            background:#050510;
            color:#fff;
            padding:12px;
            border:3px solid #172cff;
            border-radius:14px;
            text-align:center;
            font-family:Arial,sans-serif;
            max-width:600px;
            margin:auto;
          }
          #pacman-app .hud {
            display:flex;
            justify-content:space-around;
            gap:8px;
            color:#ffe600;
            font-weight:bold;
            font-size:13px;
            padding:8px 0;
          }
          #pacman-app canvas {
            width:100%;
            height:auto;
            max-width:560px;
            display:block;
            margin:auto;
            background:#000;
            border-radius:6px;
          }
          #pacman-app button {
            background:#172cff;
            color:white;
            border:2px solid #4d8dff;
            border-radius:9px;
            padding:10px 15px;
            margin:3px;
            font-weight:bold;
            cursor:pointer;
            touch-action:manipulation;
          }
          #pacman-app button:active {
            background:#ffb900;
            color:#000;
          }
          #pacman-app .controls {
            padding:8px;
          }
          #pacman-app .controls button {
            min-width:55px;
            min-height:42px;
          }
          #pacman-app .game-actions {
            display:flex;
            justify-content:center;
            align-items:center;
            flex-wrap:wrap;
            gap:8px;
            padding:8px;
            font-size:12px;
          }
          #pacman-app #message {
            color:#ffe600;
          }
        </style>
        <script>
        (() => {
          const canvas = document.getElementById("game");
          const ctx = canvas.getContext("2d");
          const scoreEl = document.getElementById("score");
          const highEl = document.getElementById("highscore");
          const livesEl = document.getElementById("lives");
          const messageEl = document.getElementById("message");

          const TILE = 28;
          const COLS = 20;
          const ROWS = 22;
          const W = COLS * TILE;
          const H = ROWS * TILE;

          const raw = [
            "####################",
            "#........##........#",
            "#.##.###.##.###.##.#",
            "#o##.###.##.###.##o#",
            "#..................#",
            "#.##.##.######.##..#",
            "#....##...##...##..#",
            "####.###.##.###.####",
            "####.##......##.####",
            "####.##.####.##.####",
            "......#..GG..#......",
            "####.##.####.##.####",
            "####.##......##.####",
            "####.###.##.###.####",
            "#........##........#",
            "#.##.###.##.###.##.#",
            "#o.#...........#.o.#",
            "##.#.##.######.#.###",
            "#....##...##...##..#",
            "#.######.##.######.#",
            "#..................#",
            "####################"
          ];

          const maze = raw.map(row => row.split(""));
          const original = raw.map(row => row.split(""));

          const colors = ["#ff3030","#ff91d2","#26d9ff","#ff9b28"];
          const ghostStarts = [
            {x:9.5,y:10.5},
            {x:10.5,y:10.5},
            {x:9.5,y:11.5},
            {x:10.5,y:11.5}
          ];

          let player, ghosts, score, lives, power, powerTimer;
          let direction, nextDirection, running, gameOver, won;
          let lastTime = 0;
          let high = 0;

          try {
            high = Number(localStorage.getItem("hauntedPacHigh") || 0);
          } catch(e) {}
          highEl.textContent = high;

          function resetPositions() {
            player = {
              x: 9.5 * TILE,
              y: 16.5 * TILE,
              dir: {x:0,y:0},
              speed: 115,
              radius: 10
            };
            direction = {x:0,y:0};
            nextDirection = {x:0,y:0};

            ghosts = ghostStarts.map((p,i) => ({
              x:p.x*TILE,
              y:p.y*TILE,
              color:colors[i],
              dir:{x:0,y:0},
              speed: i===0 ? 83 : 75,
              frightened:false,
              homeX:p.x*TILE,
              homeY:p.y*TILE
            }));

            power = false;
            powerTimer = 0;
          }

          function resetGame() {
            for(let y=0;y<ROWS;y++) {
              for(let x=0;x<COLS;x++) {
                maze[y][x] = original[y][x];
              }
            }
            score = 0;
            lives = 3;
            gameOver = false;
            won = false;
            running = true;
            resetPositions();
            updateHud();
            messageEl.textContent = "Eat all the dots!";
          }

          function updateHud() {
            scoreEl.textContent = score;
            livesEl.textContent = lives;
            if(score > high) {
              high = score;
              highEl.textContent = high;
              try {
                localStorage.setItem("hauntedPacHigh", String(high));
              } catch(e) {}
            }
          }

          function wallAtPixel(px,py) {
            const c = Math.floor(px/TILE);
            const r = Math.floor(py/TILE);
            if(r<0 || r>=ROWS || c<0 || c>=COLS) return true;
            return maze[r][c] === "#";
          }

          function canMove(entity,dir) {
            if(dir.x===0 && dir.y===0) return true;
            const margin = entity.radius ? entity.radius-2 : 7;
            const nx = entity.x + dir.x * 4;
            const ny = entity.y + dir.y * 4;
            const points = [
              [nx-margin,ny-margin],
              [nx+margin,ny-margin],
              [nx-margin,ny+margin],
              [nx+margin,ny+margin]
            ];
            return points.every(p => !wallAtPixel(p[0],p[1]));
          }

          function aligned(entity) {
            return (
              Math.abs((entity.x % TILE) - TILE/2) < 3 &&
              Math.abs((entity.y % TILE) - TILE/2) < 3
            );
          }

          function eatTile() {
            const c = Math.floor(player.x/TILE);
            const r = Math.floor(player.y/TILE);
            if(r<0 || r>=ROWS || c<0 || c>=COLS) return;

            if(maze[r][c] === ".") {
              maze[r][c] = " ";
              score += 10;
              updateHud();
            } else if(maze[r][c] === "o") {
              maze[r][c] = " ";
              score += 50;
              power = true;
              powerTimer = 8;
              ghosts.forEach(g => g.frightened = true);
              updateHud();
              messageEl.textContent = "POWER PELLET! Eat the ghosts!";
            }

            let dots = 0;
            for(let y=0;y<ROWS;y++) {
              for(let x=0;x<COLS;x++) {
                if(maze[y][x]==="." || maze[y][x]==="o") dots++;
              }
            }
            if(dots===0) {
              won = true;
              running = false;
              messageEl.textContent = "YOU CLEARED THE MAZE!";
            }
          }

          function movePlayer(dt) {
            if(aligned(player) && canMove(player,nextDirection)) {
              direction = {...nextDirection};
            }

            if(!canMove(player,direction)) {
              if(aligned(player)) {
                direction = {x:0,y:0};
              }
            }

            if(direction.x!==0 || direction.y!==0) {
              player.x += direction.x * player.speed * dt;
              player.y += direction.y * player.speed * dt;
            }

            player.x = Math.max(TILE/2,Math.min(W-TILE/2,player.x));
            player.y = Math.max(TILE/2,Math.min(H-TILE/2,player.y));
            eatTile();
          }

          function ghostChoices(g) {
            const dirs = [
              {x:1,y:0},{x:-1,y:0},
              {x:0,y:1},{x:0,y:-1}
            ];
            return dirs.filter(d => {
              if(d.x===-g.dir.x && d.y===-g.dir.y) return false;
              return canMove(g,d);
            });
          }

          function moveGhost(g,dt,index) {
            if(aligned(g)) {
              let choices = ghostChoices(g);
              if(choices.length===0) {
                g.dir = {x:0,y:0};
              } else {
                let target;
                if(g.frightened) {
                  target = {x:player.x,y:player.y};
                  choices.sort(() => Math.random()-0.5);
                  g.dir = choices[0];
                } else {
                  target = {
                    x:player.x + (index%2===0 ? 30 : -30),
                    y:player.y
                  };
                  choices.sort((a,b) => {
                    const da = Math.hypot(
                      g.x+a.x*TILE-target.x,
                      g.y+a.y*TILE-target.y
                    );
                    const db = Math.hypot(
                      g.x+b.x*TILE-target.x,
                      g.y+b.y*TILE-target.y
                    );
                    return da-db;
                  });
                  g.dir = choices[0];
                }
              }
            }

            if(canMove(g,g.dir)) {
              g.x += g.dir.x*g.speed*dt;
              g.y += g.dir.y*g.speed*dt;
            } else {
              g.dir = {x:0,y:0};
            }
          }

          function collisionCheck() {
            for(let i=0;i<ghosts.length;i++) {
              const g = ghosts[i];
              const d = Math.hypot(player.x-g.x,player.y-g.y);
              if(d < 17) {
                if(power || g.frightened) {
                  score += 200;
                  updateHud();
                  g.x = g.homeX;
                  g.y = g.homeY;
                  g.dir = {x:0,y:0};
                  g.frightened = false;
                } else {
                  lives--;
                  updateHud();
                  if(lives<=0) {
                    gameOver = true;
                    running = false;
                    messageEl.textContent = "GAME OVER — Press NEW GAME";
                  } else {
                    resetPositions();
                    messageEl.textContent = "Ouch! Watch out for the ghosts!";
                  }
                  break;
                }
              }
            }
          }

          function drawMaze() {
            ctx.fillStyle = "#000";
            ctx.fillRect(0,0,W,H);

            for(let y=0;y<ROWS;y++) {
              for(let x=0;x<COLS;x++) {
                const cell = maze[y][x];
                const px=x*TILE, py=y*TILE;

                if(cell==="#") {
                  ctx.fillStyle="#0614a8";
                  ctx.fillRect(px+1,py+1,TILE-2,TILE-2);
                  ctx.strokeStyle="#247bff";
                  ctx.lineWidth=1.5;
                  ctx.strokeRect(px+2,py+2,TILE-4,TILE-4);
                } else if(cell===".") {
                  ctx.fillStyle="#ffe6a3";
                  ctx.beginPath();
                  ctx.arc(px+TILE/2,py+TILE/2,2.5,0,Math.PI*2);
                  ctx.fill();
                } else if(cell==="o") {
                  ctx.fillStyle="#fff";
                  ctx.beginPath();
                  ctx.arc(px+TILE/2,py+TILE/2,6,0,Math.PI*2);
                  ctx.fill();
                }
              }
            }
          }

          function drawPlayer() {
            ctx.fillStyle="#ffe500";
            ctx.beginPath();
            let angle = Math.atan2(direction.y,direction.x);
            if(direction.x===0 && direction.y===0) angle=0;
            const mouth = 0.25 + Math.abs(Math.sin(Date.now()/90))*0.22;
            ctx.moveTo(player.x,player.y);
            ctx.arc(
              player.x,player.y,player.radius,
              angle+mouth,angle+Math.PI*2-mouth
            );
            ctx.closePath();
            ctx.fill();
          }

          function drawGhost(g) {
            const x=g.x, y=g.y, r=10;
            ctx.fillStyle=(power || g.frightened) ? "#285bff" : g.color;
            ctx.beginPath();
            ctx.arc(x,y-2,r,Math.PI,0);
            ctx.lineTo(x+r,y+9);
            ctx.lineTo(x+r/2,y+6);
            ctx.lineTo(x,y+10);
            ctx.lineTo(x-r/2,y+6);
            ctx.lineTo(x-r,y+10);
            ctx.closePath();
            ctx.fill();

            ctx.fillStyle="#fff";
            ctx.beginPath();
            ctx.arc(x-4,y-2,3.2,0,Math.PI*2);
            ctx.arc(x+4,y-2,3.2,0,Math.PI*2);
            ctx.fill();

            ctx.fillStyle="#111";
            ctx.beginPath();
            ctx.arc(x-4,y-2,1.5,0,Math.PI*2);
            ctx.arc(x+4,y-2,1.5,0,Math.PI*2);
            ctx.fill();
          }

          function draw() {
            drawMaze();
            ghosts.forEach(drawGhost);
            drawPlayer();
          }

          function loop(timestamp) {
            const dt=Math.min((timestamp-lastTime)/1000 || 0,0.035);
            lastTime=timestamp;

            if(running && !gameOver && !won) {
              movePlayer(dt);
              ghosts.forEach((g,i)=>moveGhost(g,dt,i));
              collisionCheck();

              if(power) {
                powerTimer-=dt;
                if(powerTimer<=0) {
                  power=false;
                  ghosts.forEach(g=>g.frightened=false);
                  messageEl.textContent="Keep collecting dots!";
                }
              }
            }

            draw();
            requestAnimationFrame(loop);
          }

          function setDirection(name) {
            const map={
              up:{x:0,y:-1},
              down:{x:0,y:1},
              left:{x:-1,y:0},
              right:{x:1,y:0}
            };
            nextDirection=map[name];
          }

          window.addEventListener("keydown",e=>{
            const keys={
              ArrowUp:"up",w:"up",W:"up",
              ArrowDown:"down",s:"down",S:"down",
              ArrowLeft:"left",a:"left",A:"left",
              ArrowRight:"right",d:"right",D:"right"
            };
            if(keys[e.key]) {
              e.preventDefault();
              setDirection(keys[e.key]);
            }
          });

          document.querySelectorAll("#pacman-app [data-dir]").forEach(btn=>{
            btn.addEventListener("pointerdown",e=>{
              e.preventDefault();
              setDirection(btn.dataset.dir);
            });
          });

          document.getElementById("start").addEventListener("click",resetGame);

          resetGame();
          requestAnimationFrame(loop);
        })();
        </script>
        """

        components.html(pacman_html, height=850, scrolling=False)


# ============================================================
# PAC-MAN 67 STATION
# ============================================================

elif page == "🕹️ Pac-Man 67 Station":
    if not st.session_state.arcade_unlocked:
        st.error("Complete the Haunted Graveyard to unlock the arcade.")
    else:
        st.header("🕹️ Pac-Man 67 Hardware Simulation")

        st.write(
            "Collect the four corner power orbs, avoid the ghost, "
            "and catch it while Super Mode is active."
        )

        if st.session_state.pm_game_over:
            st.error("💀 GAME OVER! The ghost caught you in normal mode.")

            if st.button("🎮 Insert Coin to Retry"):
                st.session_state.pm_x = 2
                st.session_state.pm_y = 2
                st.session_state.ghost_x = 4
                st.session_state.ghost_y = 4
                st.session_state.is_super_mode = False
                st.session_state.super_mode_timer = 0
                st.session_state.orbs_active = {
                    "Orb1": True,
                    "Orb2": True,
                    "Orb3": True,
                    "Orb4": True
                }
                st.session_state.pm_score = 0
                st.session_state.pm_game_over = False
                st.rerun()

        else:
            st.subheader(f"Score: {st.session_state.pm_score} 🌟")

            if st.session_state.is_super_mode:
                st.warning(
                    f"⚡ SUPER MODE ACTIVE — "
                    f"{st.session_state.super_mode_timer} moves remaining"
                )

            grid = [["▪️" for _ in range(5)] for _ in range(5)]

            orb_positions = {
                "Orb1": (0, 0),
                "Orb2": (0, 4),
                "Orb3": (4, 0),
                "Orb4": (4, 4)
            }

            for orb, (y, x) in orb_positions.items():
                if st.session_state.orbs_active[orb]:
                    grid[y][x] = "🔮"

            ghost_icon = (
                "💙" if st.session_state.is_super_mode else "🟢"
            )
            player_icon = (
                "⚡" if st.session_state.is_super_mode else "🟡"
            )

            grid[
                st.session_state.ghost_y
            ][
                st.session_state.ghost_x
            ] = ghost_icon

            grid[
                st.session_state.pm_y
            ][
                st.session_state.pm_x
            ] = player_icon

            for row in grid:
                st.markdown(
                    "<div style='font-size:30px; letter-spacing:8px;'>"
                    + " ".join(row)
                    + "</div>",
                    unsafe_allow_html=True
                )

            st.caption(
                "Use the controls to move. "
                "The ghost moves after each player move."
            )

            c1, c2, c3, c4 = st.columns(4)
            moved = False

            with c1:
                if (
                    st.button("◀️ Left", key="pm_left")
                    and st.session_state.pm_x > 0
                ):
                    st.session_state.pm_x -= 1
                    moved = True

            with c2:
                if (
                    st.button("▶️ Right", key="pm_right")
                    and st.session_state.pm_x < 4
                ):
                    st.session_state.pm_x += 1
                    moved = True

            with c3:
                if (
                    st.button("🔼 Up", key="pm_up")
                    and st.session_state.pm_y > 0
                ):
                    st.session_state.pm_y -= 1
                    moved = True

            with c4:
                if (
                    st.button("🔽 Down", key="pm_down")
                    and st.session_state.pm_y < 4
                ):
                    st.session_state.pm_y += 1
                    moved = True

            if moved:
                for orb, (y, x) in orb_positions.items():
                    if (
                        st.session_state.pm_y == y
                        and st.session_state.pm_x == x
                        and st.session_state.orbs_active[orb]
                    ):
                        st.session_state.orbs_active[orb] = False
                        st.session_state.is_super_mode = True
                        st.session_state.super_mode_timer = 10

                        st.toast(
                            "Power Orb collected! Super Mode activated!",
                            icon="⚡"
                        )

                if st.session_state.ghost_x < st.session_state.pm_x:
                    st.session_state.ghost_x += 1
                elif st.session_state.ghost_x > st.session_state.pm_x:
                    st.session_state.ghost_x -= 1
                elif st.session_state.ghost_y < st.session_state.pm_y:
                    st.session_state.ghost_y += 1
                elif st.session_state.ghost_y > st.session_state.pm_y:
                    st.session_state.ghost_y -= 1

                if (
                    st.session_state.pm_x == st.session_state.ghost_x
                    and st.session_state.pm_y == st.session_state.ghost_y
                ):
                    if st.session_state.is_super_mode:
                        st.session_state.pm_score += 10
                        st.toast("Ghost caught! +10 points", icon="👻")

                        (
                            st.session_state.ghost_x,
                            st.session_state.ghost_y
                        ) = random.choice([
                            (0, 2), (2, 0), (4, 2), (2, 4)
                        ])
                    else:
                        st.session_state.pm_game_over = True

                if st.session_state.is_super_mode:
                    st.session_state.super_mode_timer -= 1

                    if st.session_state.super_mode_timer <= 0:
                        st.session_state.is_super_mode = False
                        st.toast("Super Mode has expired!", icon="⏳")

                st.rerun()


# ============================================================
# GOOFY GANG TETRIS
# ============================================================

elif page == "🧩 Goofy Gang Tetris":
    if not st.session_state.arcade_unlocked:
        st.error("Complete the Haunted Graveyard to unlock the arcade.")
    else:
        st.header("🧩 Goofy Gang Tetris")

        st.write(
            "Classic Tetris-style gameplay: blocks fall automatically. "
            "Move them left or right and rotate them to fit the gaps."
        )

        @st.fragment(run_every=0.8)
        def render_tetris_game():
            if not st.session_state.tetris_game_over:
                tetris_gravity_step()

            score_col, lines_col = st.columns(2)

            score_col.metric("Score", st.session_state.tetris_score)
            lines_col.metric("Lines cleared", st.session_state.tetris_lines)

            if st.session_state.tetris_game_over:
                st.error("💀 GAME OVER! Your blocks reached the top.")

                if st.button("🔄 Play Again", key="tetris_play_again"):
                    reset_tetris_game()
                    st.rerun()

                return

            display_board = [
                row[:] for row in st.session_state.tetris_board
            ]

            for row_index, row in enumerate(st.session_state.tetris_piece):
                for col_index, cell in enumerate(row):
                    if cell:
                        board_y = st.session_state.piece_y + row_index
                        board_x = st.session_state.piece_x + col_index

                        if (
                            0 <= board_y < 10
                            and 0 <= board_x < 6
                        ):
                            display_board[board_y][board_x] = (
                                st.session_state.active_shape
                            )

            st.markdown(
                "<div style='font-family:monospace; font-size:25px; "
                "line-height:1.35; letter-spacing:5px; "
                "background:#100b20; padding:12px; border-radius:10px;'>"
                + "<br>".join(
                    "".join(row) for row in display_board
                )
                + "</div>",
                unsafe_allow_html=True
            )

            left_btn, rotate_btn, right_btn, down_btn = st.columns(4)

            with left_btn:
                if st.button(
                    "◀️ Left",
                    key="tetris_left",
                    use_container_width=True
                ):
                    if tetris_fits(
                        st.session_state.tetris_piece,
                        st.session_state.piece_x - 1,
                        st.session_state.piece_y
                    ):
                        st.session_state.piece_x -= 1

            with rotate_btn:
                if st.button(
                    "🔄 Rotate",
                    key="tetris_rotate",
                    use_container_width=True
                ):
                    tetris_rotate_piece()

            with right_btn:
                if st.button(
                    "Right ▶️",
                    key="tetris_right",
                    use_container_width=True
                ):
                    if tetris_fits(
                        st.session_state.tetris_piece,
                        st.session_state.piece_x + 1,
                        st.session_state.piece_y
                    ):
                        st.session_state.piece_x += 1

            with down_btn:
                if st.button(
                    "⬇️ Drop",
                    key="tetris_down",
                    use_container_width=True
                ):
                    tetris_gravity_step()

            if st.button(
                "⏬ Hard Drop",
                key="tetris_hard_drop",
                use_container_width=True
            ):
                while tetris_fits(
                    st.session_state.tetris_piece,
                    st.session_state.piece_x,
                    st.session_state.piece_y + 1
                ):
                    st.session_state.piece_y += 1

                tetris_lock_piece()

            st.caption(
                "Controls: Left / Right to move · Rotate to turn the piece "
                "· Drop to move down faster · Hard Drop to place it "
                "immediately. Gravity runs automatically."
            )

            if st.button("🧹 Reset Tetris", key="tetris_reset"):
                reset_tetris_game()
                st.rerun()

        render_tetris_game()


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
