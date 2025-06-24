# Importing necessary modules
import os  # For accessing environment variables (like API keys)
from langchain.prompts import ChatPromptTemplate  # To format prompts for the LLM
from langchain_groq import ChatGroq  # ChatGroq is the LLM interface (like LLaMA 3 from Groq)
from dotenv import load_dotenv  # Loads environment variables from a .env file

# Load all the environment variables from the .env file
load_dotenv()


# Define a class to handle all LLM-related tasks for music generation
class MusicLLM:
    # Constructor function: initializes the LLM with a specified temperature
    def __init__(self, temperature=0.7):
        # Create a ChatGroq object using API key and model name
        self.llm = ChatGroq(
            temperature=temperature,  # Controls randomness of output (higher = more creative)
            groq_api_key=os.getenv("GROQ_API_KEY"),  # Get the API key from environment
            model_name="llama-3.1-8b-instant"  # Use Groq's LLaMA 3.1 model
        )

    # Method to generate a melody (sequence of notes) from user input
    def generate_melody(self, user_input):
        # Define a prompt template to instruct the LLM to generate a melody
        prompt = ChatPromptTemplate.from_template(
            "Generate a melody based on this input: {input}. Represent it as space-separated notes (e.g., C4 D4 E4)."
        )
        # Combine the prompt with the LLM into a chain
        chain = prompt | self.llm
        # Invoke the LLM with the user input and return the cleaned result
        return chain.invoke({"input": user_input}).content.strip()

    # Method to generate harmony chords for the given melody
    def generate_harmony(self, melody):
        # Prompt tells the LLM to generate chords that match the melody
        prompt = ChatPromptTemplate.from_template(
            "Create harmony chords for this melody: {melody}. Format: C4-E4-G4 F4-A4-C5."
        )
        # Create chain of prompt + LLM
        chain = prompt | self.llm
        # Provide melody and get LLM output
        return chain.invoke({"melody": melody}).content.strip()

    # Method to generate rhythm durations (beats) for each melody note
    def generate_rhythm(self, melody):
        # Prompt LLM to suggest durations like 1.0, 0.5, etc. for each note
        prompt = ChatPromptTemplate.from_template(
            "Suggest rhythm durations (in beats) for this melody: {melody}. Format: 1.0 0.5 0.5 2.0."
        )
        # Create prompt + LLM chain
        chain = prompt | self.llm
        # Pass melody and get response
        return chain.invoke({"melody": melody}).content.strip()

    # Method to adapt the entire musical structure to a specific style (e.g., Jazz, Sad, Pop)
    def adapt_style(self, style, melody, harmony, rhythm):
        # Prompt LLM to take melody, harmony, and rhythm and convert/adapt to a specific style
        prompt = ChatPromptTemplate.from_template(
            "Adapt to {style} style:\nMelody: {melody}\nHarmony: {harmony}\nRhythm: {rhythm}\nOutput single string summary."
        )
        # Create the prompt + LLM chain
        chain = prompt | self.llm
        # Pass all components and get stylized result
        return chain.invoke({
            "style": style,
            "melody": melody,
            "harmony": harmony,
            "rhythm": rhythm
        }).content.strip()
