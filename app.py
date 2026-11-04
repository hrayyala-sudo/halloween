import streamlit as st
import random
import json
import time

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
    "orbs_active": {
        "Orb1": True,
        "Orb2": True,
        "Orb3": True,
        "Orb4": True
    },
    "pm_game_over": False,

    # Normal Goofy Gang Pac-Man
    "pac_x": 2,
    "pac_y": 4,
    "pac_score": 0,
    "pac_game_grid": [
        ["🍬" for _ in range(5)] for _ in range(5)
    ],
    "pac_ghosts": [
        {"x": 0, "y": 0, "color": "🔴"},
        {"x": 4, "y": 0, "color": "💖"},
        {"x": 0, "y": 2, "color": "🔵"},
        {"x": 4, "y": 2, "color": "🧡"}
    ],
    "pac_game_won": False,
    "pac_last_event": "",

    # Tetris
    "tetris_board": [
        ["⬛" for _ in range(6)] for _ in range(10)
    ],
    "piece_x": 2,
    "piece_y": 0,
    "tetris_score": 0,
    "active_shape": "🟦",
    "tetris_piece": None,
    "tetris_game_over": False,
    "tetris_lines": 0
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ============================================================
# TETRIS SHAPES
# ============================================================

TETROMINOES = [
    [[1, 1, 1, 1]],                 # I
    [[1, 1], [1, 1]],               # O
    [[0, 1, 0], [1, 1, 1]],         # T
    [[0, 1, 1], [1, 1, 0]],         # S
    [[1, 1, 0], [0, 1, 1]],         # Z
    [[1, 0, 0], [1, 1, 1]],         # J
    [[0, 0, 1], [1, 1, 1]],         # L
]

if st.session_state.tetris_piece is None:
    st.session_state.tetris_piece = random.choice(TETROMINOES)

# Keep Pac-Man's starting square clear.
st.session_state.pac_game_grid[4][2] = "▪️"

if st.session_state.quest_questions is None:
    st.session_state.quest_questions = random.sample(
        PHANTOM_QUEST_QUESTIONS, 5
    )

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
    st.session_state.quest_failed = False
    st.session_state.phantom_quest_completed = False


def reset_graveyard_game():

    st.session_state.graveyard_round = 1
    st.session_state.graveyard_score = 0
    st.session_state.graveyard_completed = False


# ============================================================
# TETRIS GAME HELPERS
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

    st.session_state.active_shape = random.choice([
        "🟧", "🟪", "🟦", "🟩"
    ])

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

                board[board_y][board_x] = (
                    st.session_state.active_shape
                )

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

    # Wall kicks allow rotation near the board edges.
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

    st.session_state.active_shape = random.choice([
        "🟧", "🟪", "🟦", "🟩"
    ])

    st.session_state.tetris_score = 0
    st.session_state.tetris_lines = 0
    st.session_state.tetris_game_over = False


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

            st.warning(
                "That is not the secret phrase. Try again!"
            )

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

    else:

        st.error(
            "This adventure is locked! "
            "Complete Phantom Quest first."
        )
# ============================================================
# BONUS PAGE 8: NORMAL GOOFY GANG PAC-MAN
# ============================================================

elif page == "🟡 Pac-Man Arcade":

    if not st.session_state.arcade_unlocked:

        st.error(
            "This arcade station is locked. Complete the Haunted "
            "Graveyard and knock on the Front Porch door!"
        )

    else:

        st.header("🟡 Retro Pac-Man Arcade")

        st.write(
            "Clear the candy from the 5×5 maze while avoiding "
            "the four ghosts. Each candy is worth 10 points."
        )

        st.markdown(
            "<div class='spooky-box'>"
            "<h3>🍬 Collect every candy and escape the ghosts!</h3>"
            "<p>Use the directional buttons to move one square at a time.</p>"
            "</div>",
            unsafe_allow_html=True
        )

        remaining_candy = sum(
            cell == "🍬"
            for row in st.session_state.pac_game_grid
            for cell in row
        )

        st.subheader(
            f"Score: {st.session_state.pac_score} 🌟  |  "
            f"Candies left: {remaining_candy} 🍬"
        )

        if st.session_state.pac_game_won:

            st.success(
                "🏆 You cleared the maze! "
                "You are the Pac-Man champion!"
            )

            st.balloons()

        else:

            display_grid = [
                row[:] for row in st.session_state.pac_game_grid
            ]

            for ghost in st.session_state.pac_ghosts:

                display_grid[ghost["y"]][ghost["x"]] = ghost["color"]

            display_grid[
                st.session_state.pac_y
            ][
                st.session_state.pac_x
            ] = "🟡"

            st.markdown(
                "<div style='background:#090909; border:3px solid #2875ff; "
                "border-radius:12px; padding:14px; width:fit-content; "
                "margin:0 auto; box-shadow:0 0 14px #2875ff;'>",
                unsafe_allow_html=True
            )

            for row in display_grid:

                st.markdown(
                    "<div style='font-size:34px; line-height:1.55; "
                    "letter-spacing:10px; text-align:center;'>"
                    + " ".join(row)
                    + "</div>",
                    unsafe_allow_html=True
                )

            st.markdown("</div>", unsafe_allow_html=True)

            st.caption(
                "🟡 Pac-Man  |  🍬 Candy  |  🔴 💖 🔵 🧡 Ghosts"
            )

            st.write("### Move Pac-Man")

            top_pad, top_center, top_pad_right = st.columns(3)

            with top_center:
                up_pressed = st.button(
                    "🔼 Up",
                    key="normal_pac_up",
                    use_container_width=True
                )

            left_col, middle_pad, right_col = st.columns(3)

            with left_col:
                left_pressed = st.button(
                    "◀️ Left",
                    key="normal_pac_left",
                    use_container_width=True
                )

            with right_col:
                right_pressed = st.button(
                    "Right ▶️",
                    key="normal_pac_right",
                    use_container_width=True
                )

            bottom_pad, bottom_center, bottom_pad_right = st.columns(3)

            with bottom_center:
                down_pressed = st.button(
                    "🔽 Down",
                    key="normal_pac_down",
                    use_container_width=True
                )

            move = None

            if up_pressed:
                move = (0, -1)
            elif down_pressed:
                move = (0, 1)
            elif left_pressed:
                move = (-1, 0)
            elif right_pressed:
                move = (1, 0)

            if move is not None:

                new_x = max(
                    0,
                    min(4, st.session_state.pac_x + move[0])
                )

                new_y = max(
                    0,
                    min(4, st.session_state.pac_y + move[1])
                )

                st.session_state.pac_x = new_x
                st.session_state.pac_y = new_y

                caught = any(
                    ghost["x"] == new_x and ghost["y"] == new_y
                    for ghost in st.session_state.pac_ghosts
                )

                if not caught:

                    if (
                        st.session_state.pac_game_grid[new_y][new_x]
                        == "🍬"
                    ):

                        st.session_state.pac_game_grid[new_y][new_x] = "▪️"

                        st.session_state.pac_score += 10

                        st.toast(
                            "+10 points! Candy collected!",
                            icon="🍬"
                        )

                    for ghost in st.session_state.pac_ghosts:

                        directions = [
                            (0, -1),
                            (0, 1),
                            (-1, 0),
                            (1, 0)
                        ]

                        random.shuffle(directions)

                        for dx, dy in directions:

                            gx = ghost["x"] + dx
                            gy = ghost["y"] + dy

                            if 0 <= gx < 5 and 0 <= gy < 5:

                                ghost["x"] = gx
                                ghost["y"] = gy
                                break

                    caught = any(
                        ghost["x"] == st.session_state.pac_x
                        and ghost["y"] == st.session_state.pac_y
                        for ghost in st.session_state.pac_ghosts
                    )

                if caught:

                    st.session_state.pac_score = max(
                        0,
                        st.session_state.pac_score - 20
                    )

                    st.session_state.pac_x = 2
                    st.session_state.pac_y = 4

                    st.session_state.pac_ghosts = [
                        {"x": 0, "y": 0, "color": "🔴"},
                        {"x": 4, "y": 0, "color": "💖"},
                        {"x": 0, "y": 2, "color": "🔵"},
                        {"x": 4, "y": 2, "color": "🧡"}
                    ]

                    st.session_state.pac_last_event = "caught"

                    st.toast(
                        "A ghost caught you! -20 points. Try again!",
                        icon="👻"
                    )

                else:

                    st.session_state.pac_last_event = "moved"

                    remaining = sum(
                        cell == "🍬"
                        for row in st.session_state.pac_game_grid
                        for cell in row
                    )

                    if remaining == 0:
                        st.session_state.pac_game_won = True

                st.rerun()

        if st.button(
            "🔄 Reset Pac-Man Game",
            key="normal_pac_reset"
        ):

            st.session_state.pac_x = 2
            st.session_state.pac_y = 4
            st.session_state.pac_score = 0

            st.session_state.pac_game_grid = [
                ["🍬" for _ in range(5)] for _ in range(5)
            ]

            st.session_state.pac_game_grid[4][2] = "▪️"

            st.session_state.pac_ghosts = [
                {"x": 0, "y": 0, "color": "🔴"},
                {"x": 4, "y": 0, "color": "💖"},
                {"x": 0, "y": 2, "color": "🔵"},
                {"x": 4, "y": 2, "color": "🧡"}
            ]

            st.session_state.pac_game_won = False
            st.session_state.pac_last_event = ""

            st.rerun()


# ============================================================
# BONUS PAGE 9: PAC-MAN 67 ARCADE
# ============================================================

elif page == "🕹️ Pac-Man 67 Station":

    if not st.session_state.arcade_unlocked:

        st.error(
            "This arcade station is locked. Complete the Haunted "
            "Graveyard and knock on the Front Porch door!"
        )

    else:

        st.header("🕹️ Classic Pac-Man 67 Hardware Simulation")

        st.write(
            "Collect the four corner power orbs, avoid the ghost, "
            "and catch it while Super Mode is active."
        )

        if st.session_state.pm_game_over:

            st.error(
                "💀 GAME OVER! The ghost caught you in normal mode."
            )

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

            st.subheader(
                f"Score: {st.session_state.pm_score} 🌟"
            )

            if st.session_state.is_super_mode:

                st.warning(
                    f"⚡ SUPER MODE ACTIVE — "
                    f"{st.session_state.super_mode_timer} moves remaining"
                )

            grid = [
                ["▪️" for _ in range(5)] for _ in range(5)
            ]

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

                # Move the ghost one step toward the player.
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

                        st.toast(
                            "Ghost caught! +10 points",
                            icon="👻"
                        )

                        st.session_state.ghost_x, st.session_state.ghost_y = (
                            random.choice([
                                (0, 2),
                                (2, 0),
                                (4, 2),
                                (2, 4)
                            ])
                        )

                    else:

                        st.session_state.pm_game_over = True

                if st.session_state.is_super_mode:

                    st.session_state.super_mode_timer -= 1

                    if st.session_state.super_mode_timer <= 0:

                        st.session_state.is_super_mode = False

                        st.toast(
                            "Super Mode has expired!",
                            icon="⏳"
                        )

                st.rerun()


# ============================================================
# BONUS PAGE 10: GOOFY GANG TETRIS
# ============================================================

elif page == "🧩 Goofy Gang Tetris":

    if not st.session_state.arcade_unlocked:

        st.error(
            "This arcade station is locked. Complete the Haunted "
            "Graveyard and knock on the Front Porch door!"
        )

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

            score_col.metric(
                "Score",
                st.session_state.tetris_score
            )

            lines_col.metric(
                "Lines cleared",
                st.session_state.tetris_lines
            )

            if st.session_state.tetris_game_over:

                st.error(
                    "💀 GAME OVER! Your blocks reached the top."
                )

                if st.button(
                    "🔄 Play Again",
                    key="tetris_play_again"
                ):

                    reset_tetris_game()
                    st.rerun()

                return

            # Draw the settled board and active falling piece.
            display_board = [
                row[:] for row in st.session_state.tetris_board
            ]

            for row_index, row in enumerate(
                st.session_state.tetris_piece
            ):

                for col_index, cell in enumerate(row):

                    if cell:

                        board_y = (
                            st.session_state.piece_y + row_index
                        )

                        board_x = (
                            st.session_state.piece_x + col_index
                        )

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

            if st.button(
                "🧹 Reset Tetris",
                key="tetris_reset"
            ):

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
