import assemblyai as aai
import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Load API key from environment variable
api_key = os.getenv('ASSEMBLYAI_API_KEY')
if not api_key:
    raise ValueError("ASSEMBLYAI_API_KEY environment variable is not set")

aai.settings.api_key = api_key

FILE_PATH = ""

config = aai.TranscriptionConfig(speaker_labels=True,
                               iab_categories=True,
                               sentiment_analysis=True,
                               summarization=True,
                               language_detection=True)

transcriber = aai.Transcriber()
transcript = transcriber.transcribe(FILE_PATH, config=config)