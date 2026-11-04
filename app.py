
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
    "tetris_lines": 0
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# Tetris uses real rotating tetrominoes rather than single falling squares.
TETROMINOES = [
    [[1, 1, 1, 1]],                         # I
