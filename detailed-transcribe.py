import assemblyai as aai
import streamlit as st

aai.settings.api_key = "14dce84777f54270a567892aa18f4c51"

FILE_PATH = "/Users/lanedenson/repos/Personal/AssemblyAI-Sandbox/Text transcription/meeting-notes.m4a"

config = aai.TranscriptionConfig(speaker_labels=True,
                                 iab_categories=True,
                                 sentiment_analysis=True,
                                 summarization=True,
                                 language_detection=True)

transcriber = aai.Transcriber()
transcript = transcriber.transcribe(FILE_PATH, config=config)
