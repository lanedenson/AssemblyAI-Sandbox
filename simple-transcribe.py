import assemblyai as aai
import os
from pathlib import Path
import shutil
from dotenv import load_dotenv

# Load environment variables silently
load_dotenv()

# Load API key from environment variable
api_key = os.getenv('ASSEMBLYAI_API_KEY')
if not api_key:
    raise ValueError("ASSEMBLYAI_API_KEY environment variable is not set")

aai.settings.api_key = api_key

# Define input and output directories
INPUT_DIR = "input"
OUTPUT_DIR = "output"
COMPLETED_DIR = os.path.join(INPUT_DIR, "completed")

# Create required directories if they don't exist
os.makedirs(INPUT_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(COMPLETED_DIR, exist_ok=True)

def get_output_filename(input_path):
    """Convert input audio filename to output txt filename"""
    input_stem = Path(input_path).stem
    return os.path.join(OUTPUT_DIR, f"{input_stem}.txt")

def process_audio_files():
    # Configure transcription options
    config = aai.TranscriptionConfig(
        speaker_labels=True
    )
    
    transcriber = aai.Transcriber()
    
    # Get list of supported audio file extensions
    AUDIO_EXTENSIONS = ('.mp3', '.mp4', '.wav', '.m4a', '.flac')
    
    # Debug: Print current directory and input directory contents
    print(f"\nInput directory: {os.path.abspath(INPUT_DIR)}")
    print("Files in input directory:")
    all_files = os.listdir(INPUT_DIR)
    for file in all_files:
        print(f"- {file}")
    
    # Process each audio file in input directory
    found_audio = False
    for filename in os.listdir(INPUT_DIR):
        # Skip the completed directory itself
        if filename == "completed":
            continue
            
        # Debug: Print file extension check
        file_ext = os.path.splitext(filename)[1].lower()
        print(f"\nChecking file: {filename}")
        print(f"File extension: {file_ext}")
        print(f"Is audio file: {file_ext in AUDIO_EXTENSIONS}")
        
        if filename.lower().endswith(AUDIO_EXTENSIONS):
            found_audio = True
            input_path = os.path.join(INPUT_DIR, filename)
            output_path = get_output_filename(input_path)
            completed_path = os.path.join(COMPLETED_DIR, filename)
            
            # Check if file was previously transcribed
            if os.path.exists(output_path) or os.path.exists(completed_path):
                reprocess = input(f"\nFile {filename} has already been transcribed. Would you like to transcribe it again? (y/n): ")
                if reprocess.lower() != 'y':
                    print(f"Skipping {filename}")
                    continue
                print(f"Reprocessing {filename}...")
            else:
                print(f"Processing {filename}...")
            
            try:
                transcript = transcriber.transcribe(input_path, config=config)
                
                if transcript.status == aai.TranscriptStatus.error:
                    print(f"Error processing {filename}: {transcript.error}")
                else:
                    # Write transcript and analysis to output file
                    with open(output_path, 'w', encoding='utf-8') as f:
                        # Write summary if available
                        if transcript.summary:
                            f.write("=== Summary ===\n\n")
                            f.write(transcript.summary)
                            f.write("\n\n")
                        
                        # Write speaker labels if available
                        if transcript.utterances:
                            f.write("=== Speaker Labels ===\n\n")
                            for utterance in transcript.utterances:
                                f.write(f"Speaker {utterance.speaker}: {utterance.text}\n")
                            f.write("\n\n")
                        
                        # Write raw transcript at the bottom
                        f.write("=" * 80 + "\n")
                        f.write("=== Raw Transcript ===\n\n")
                        f.write(transcript.text)
                    
                    # Move the processed file to completed directory
                    shutil.move(input_path, completed_path)
                    print(f"Successfully transcribed {filename} and moved to completed folder")
                    
                    # Prompt for transcript deletion
                    delete_prompt = input(f"Delete the transcript for {filename} from AssemblyAI? (y/n): ")
                    if delete_prompt.lower() == 'y':
                        try:
                            aai.Transcript.delete_by_id(transcript.id)
                            print(f"Transcript for {filename} deleted from AssemblyAI")
                        except Exception as delete_error:
                            print(f"Error deleting transcript: {str(delete_error)}")
                    
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")
    
    if not found_audio:
        print("\nNo audio files found with supported extensions:", AUDIO_EXTENSIONS)
        print("Make sure your audio files:")
        print("1. Are directly in the 'input' directory (not in 'input/completed')")
        print("2. Have one of these extensions:", AUDIO_EXTENSIONS)

if __name__ == "__main__":
    # Process audio files
    print("\nStarting audio file processing...")
    process_audio_files()