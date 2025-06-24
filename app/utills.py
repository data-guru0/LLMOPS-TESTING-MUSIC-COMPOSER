# Importing music21 for music theory (notes, chords, durations)
import music21
# NumPy for handling audio signal data
import numpy as np
# io for handling in-memory file objects (like BytesIO buffer)
import io
# write for saving audio files in WAV format
from scipy.io.wavfile import write as write_wav
# Synthesizer for generating sound waves (e.g., sine waves) from notes
from synthesizer import Synthesizer, Waveform


# Function to convert note names (e.g., "C4", "E4") into frequencies in Hz
def note_to_frequencies(note_list):
    freqs = []  # List to store frequencies
    for note_str in note_list:
        try:
            # Create a Note object
            note = music21.note.Note(note_str)
            # Append the frequency of that note to the list
            freqs.append(note.pitch.frequency)
        except:
            # Skip invalid note names
            continue
    return freqs  # Return the list of frequencies


# Function to generate WAV audio bytes from note frequencies
def generate_wav_bytes_from_notes(notes):
    # Create a Synthesizer object using sine wave and one oscillator
    synth = Synthesizer(osc1_waveform=Waveform.sine, osc1_volume=1.0, use_osc2=False)
    sample_rate = 44100  # Set sample rate (standard for audio files)

    # Generate audio signal by creating a wave for each note and joining them
    audio = np.concatenate([synth.generate_constant_wave(freq, 0.5) for freq in notes])
    
    # Create a BytesIO buffer to hold the WAV file in memory
    buffer = io.BytesIO()
    # Write the audio data to the buffer in WAV format
    write_wav(buffer, sample_rate, audio.astype(np.float32))
    # Return the audio data as raw bytes
    return buffer.getvalue()
