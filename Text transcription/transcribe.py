import assemblyai as aai
import streamlit as st

aai.settings.api_key = "14dce84777f54270a567892aa18f4c51"

FILE_PATH = "audio.mp3"

config = aai.TranscriptionConfig(speaker_labels=True,
                                 iab_categories=True,
                                 sentiment_analysis=True,
                                 summarization=True,
                                 language_detection=True)

transcriber = aai.Transcriber()
transcript = transcriber.transcribe(FILE_PATH, config=config)
