import streamlit as st
import random

# Load words from file
@st.cache_data
def load_words():
    with open("my_dict.txt", "r") as file:
        return [word.strip().lower() for word in file if word.strip().isalpha()]

# Reset game session
def reset_game(difficulty):
    word_list = load_words()
    word = random.choice(word_list)
    st.session_state.word = word
    st.session_state.guessed_letters = set()
    st.session_state.wrong_attempts = 0
    st.session_state.difficulty = difficulty
    st.session_state.max_attempts = {"Easy": 10, "Medium": 8, "Hard": 5}[difficulty]
    st.session_state.game_active = True
    st.session_state.game_over = False
    st.rerun()

# Show word with blanks and correct guesses
def display_word():
    return " ".join([letter if letter in st.session_state.guessed_letters else "_" for letter in st.session_state.word])

# --- App Title ---
st.set_page_config(page_title="Word Guessing Game", page_icon="🎯")
st.title("🎯 Word Guessing Game")

# --- Game State Initialization ---
if "game_active" not in st.session_state:
    st.session_state.game_active = False
    st.session_state.word = ""
    st.session_state.guessed_letters = set()
    st.session_state.wrong_attempts = 0
    st.session_state.max_attempts = 0
    st.session_state.difficulty = ""
    st.session_state.game_over = False

# --- Home Page (Choose Difficulty) ---
if not st.session_state.game_active:
    st.subheader("🕹️ Select Difficulty to Start")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🟢 Easy\n(10 Guesses)"):
            reset_game("Easy")
    with col2:
        if st.button("🟡 Medium\n(8 Guesses)"):
            reset_game("Medium")
    with col3:
        if st.button("🔴 Hard\n(5 Guesses)"):
            reset_game("Hard")
    st.markdown("---")
    st.info("Choose a difficulty to start playing. You'll have to guess a hidden word letter by letter.")

# --- Game Interface ---
else:
    st.subheader(f"🔠 Difficulty: {st.session_state.difficulty}")
    st.markdown(f"#### 📏 Word Length: {len(st.session_state.word)} letters")
    st.markdown(f"### 🧩 `{display_word()}`")
    st.markdown(f"**❌ Wrong Guesses:** `{st.session_state.wrong_attempts}` / `{st.session_state.max_attempts}`")

    # --- Guess Form ---
    guess = ""
    submitted = False
    with st.form("guess_form", clear_on_submit=True):
        guess = st.text_input("🔤 Enter a letter", max_chars=1).lower()
        submitted = st.form_submit_button("Submit")

    # --- Process Guess AFTER Submit ---
    if submitted and guess and not st.session_state.game_over:
        if guess in st.session_state.guessed_letters:
            st.warning("⚠️ Letter already guessed!")
        else:
            st.session_state.guessed_letters.add(guess)
            if guess not in st.session_state.word:
                st.session_state.wrong_attempts += 1

            # Check win
            if all(letter in st.session_state.guessed_letters for letter in st.session_state.word):
                st.success(f"🎉 You guessed it! The word was: `{st.session_state.word.upper()}`")
                st.session_state.game_over = True

            # Check loss
            elif st.session_state.wrong_attempts >= st.session_state.max_attempts:
                st.error("💀 You lost!")
                st.markdown(f"### 🔍 The word was: **:red[{st.session_state.word.upper()}]**")
                st.session_state.game_over = True

            if not st.session_state.game_over:
                st.rerun()

    # --- Restart Button ---
    if st.session_state.game_over:
        st.markdown("---")
        st.markdown("## 🔁 Play Again")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🟢 Easy"):
                reset_game("Easy")
        with col2:
            if st.button("🟡 Medium"):
                reset_game("Medium")
        with col3:
            if st.button("🔴 Hard"):
                reset_game("Hard")

        st.markdown("---")
        st.markdown("Made with ❤️ using Streamlit")
