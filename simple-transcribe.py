import assemblyai as aai
import os
from pathlib import Path
import shutil
from dotenv import load_dotenv

# Add debugging before loading .env
print("\n=== Environment Setup Debugging ===")
print(f"Current working directory: {os.getcwd()}")
print(f".env file exists: {os.path.exists('.env')}")

if os.path.exists('.env'):
    print("\n.env file contents:")
    with open('.env', 'r') as f:
        print(f.read())

# Load environment variables from .env file
print("\nAttempting to load .env file...")
load_dotenv(verbose=True)  # Added verbose=True to see more details

print("\n=== Environment Variables ===")
# Print all environment variables (excluding their values for security)
env_vars = [k for k in os.environ.keys() if 'ASSEMBLY' in k]
print(f"Found environment variables containing 'ASSEMBLY': {env_vars}")

# Load API key from environment variable
api_key = os.getenv('ASSEMBLYAI_API_KEY')
print(f"\nAPI key found: {'Yes' if api_key else 'No'}")
print(f"API key length: {len(api_key) if api_key else 0}")

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

def delete_all_transcripts():
    """Prompt and delete all existing transcripts from AssemblyAI"""
    delete_all = input("\nWould you like to delete all existing transcripts from AssemblyAI? (y/n): ")
    if delete_all.lower() == 'y':
        confirm = input("Are you sure? This cannot be undone! (y/n): ")
        if confirm.lower() == 'y':
            try:
                # Get all transcripts
                transcriber = aai.Transcriber()
                transcripts = transcriber.transcripts()
                
                if not transcripts:
                    print("No existing transcripts found.")
                    return
                
                print(f"\nFound {len(transcripts)} transcripts. Deleting...")
                
                # Delete each transcript
                for transcript in transcripts:
                    try:
                        aai.Transcript.delete_by_id(transcript.id)
                        print(f"Deleted transcript {transcript.id}")
                    except Exception as e:
                        print(f"Error deleting transcript {transcript.id}: {str(e)}")
                
                print("\nFinished deleting all transcripts.")
            except Exception as e:
                print(f"Error accessing transcripts: {str(e)}")
        else:
            print("Deletion cancelled.")
    else:
        print("Skipping deletion of existing transcripts.")

def get_output_filename(input_path):
    """Convert input audio filename to output txt filename"""
    input_stem = Path(input_path).stem
    return os.path.join(OUTPUT_DIR, f"{input_stem}.txt")

def process_audio_files():
    transcriber = aai.Transcriber()
    
    # Get list of supported audio file extensions
    AUDIO_EXTENSIONS = ('.mp3', '.mp4', '.wav', '.m4a', '.flac')
    
    # Process each audio file in input directory
    for filename in os.listdir(INPUT_DIR):
        # Skip the completed directory itself
        if filename == "completed":
            continue
            
        if filename.lower().endswith(AUDIO_EXTENSIONS):
            input_path = os.path.join(INPUT_DIR, filename)
            output_path = get_output_filename(input_path)
            completed_path = os.path.join(COMPLETED_DIR, filename)
            
            # Skip if output file already exists or if file is in completed folder
            if os.path.exists(output_path) or os.path.exists(completed_path):
                print(f"Skipping {filename} - already processed")
                continue
                
            print(f"Processing {filename}...")
            
            try:
                transcript = transcriber.transcribe(input_path)
                
                if transcript.status == aai.TranscriptStatus.error:
                    print(f"Error processing {filename}: {transcript.error}")
                else:
                    # Write transcript to output file
                    with open(output_path, 'w', encoding='utf-8') as f:
                        f.write(transcript.text)
                    
                    # Move the processed file to completed directory
                    shutil.move(input_path, completed_path)
                    print(f"Successfully transcribed {filename} and moved to completed folder")
                    
                    # Prompt for transcript deletion
                    delete_prompt = input(f"Do you want to delete the transcript for {filename} from AssemblyAI? (y/n): ")
                    if delete_prompt.lower() == 'y':
                        try:
                            aai.Transcript.delete_by_id(transcript.id)
                            print(f"Transcript for {filename} deleted from AssemblyAI")
                        except Exception as delete_error:
                            print(f"Error deleting transcript: {str(delete_error)}")
                    
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")

if __name__ == "__main__":
    # First prompt to delete all existing transcripts
    delete_all_transcripts()
    
    # Then process new audio files
    print("\nStarting audio file processing...")
    process_audio_files()