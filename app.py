# -------------------- Importing Required Libraries --------------------

import streamlit as st  # Streamlit is used to build the web user interface
from app.main import MusicLLM  # Import the MusicLLM class that generates melody, harmony, rhythm, and style using AI
from app.utills import (  # Import utility functions for handling music and audio
    generate_wav_bytes_from_notes,  # Converts frequencies into playable WAV audio
    note_to_frequencies  # Converts note names like C4 into actual sound frequencies
)
from io import BytesIO  # Used to store and stream audio data in memory (no file saving needed)
from dotenv import load_dotenv  # Used to load environment variables securely from a .env file

# -------------------- Load Environment Variables --------------------

# This loads sensitive values (like API keys) from a file named .env so you don't write them directly in your code
load_dotenv()

# -------------------- Set Page Details --------------------

# Sets the title of the browser tab and centers the layout on the page
st.set_page_config(page_title="🎵 AI Music Generator", layout="centered")

# Adds the main heading/title to the Streamlit app
st.title("🎼 AI Music Composer")

# Adds a short description under the title to explain what the app does
st.markdown("Generate AI music by describing the style and content.")

# -------------------- User Input Section --------------------

# Text input box where the user can describe the music they want (like "sad violin solo")
music_input = st.text_input("Describe the music (e.g., sad flute solo in A minor):")

# Dropdown menu where the user selects a musical style (used for stylizing the final result)
style = st.selectbox("Choose a style", ["Sad", "Happy", "Jazz", "Extreme", "Romantic", "Epic"])

# -------------------- Music Generation Logic --------------------

# This block runs only when the user clicks the "Generate Music" button AND has entered a prompt
if st.button("Generate Music") and music_input:
    
    # Create an object of the MusicLLM class that can interact with the LLM (AI model)
    generator = MusicLLM()

    # Show a spinner/loading message while the AI is working
    with st.spinner("Generating music..."):

        # Ask the AI to generate a melody based on user input (returns space-separated notes like "C4 D4 E4")
        melody = generator.generate_melody(music_input)

        # Ask the AI to create harmony chords that match the melody (e.g., "C4-E4-G4 F4-A4-C5")
        harmony = generator.generate_harmony(melody)

        # Ask the AI to suggest rhythm durations for each melody note (e.g., "1.0 0.5 0.5 2.0")
        rhythm = generator.generate_rhythm(melody)

        # Ask the AI to rewrite the full composition in the chosen style (e.g., Jazz or Sad)
        composition = generator.adapt_style(style, melody, harmony, rhythm)

        # -------------------- Audio Generation --------------------

        # Split the melody string into individual note names (e.g., "C4 D4 E4" → ["C4", "D4", "E4"])
        melody_notes = melody.split()

        # Convert each note into its actual sound frequency (e.g., "C4" → 261.63 Hz)
        frequencies = note_to_frequencies(melody_notes)

        # Generate audio data from those frequencies using a sine wave synthesizer
        wav_bytes = generate_wav_bytes_from_notes(frequencies)

    # -------------------- Streamlit Output Section --------------------

    # Play the generated audio directly in the app
    st.audio(BytesIO(wav_bytes), format='audio/wav')

    # Show a success message once music is generated
    st.success("Music generated!")

    # This expandable box shows a text summary of the full composition styled by the AI
    with st.expander("🎵 Composition Summary"):
        st.text(composition)
