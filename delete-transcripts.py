import assemblyai as aai
import os
import shutil
from dotenv import load_dotenv

def setup_environment():
    """Setup and verify environment variables"""
    print("\n=== Environment Setup ===")
    
    # Load environment variables from .env file
    load_dotenv()
    
    # Load API key from environment variable
    api_key = os.getenv('ASSEMBLYAI_API_KEY')
    if not api_key:
        raise ValueError("ASSEMBLYAI_API_KEY environment variable is not set")
    
    aai.settings.api_key = api_key
    print("API key loaded successfully")

def delete_local_transcripts():
    """Delete all transcripts from the local output directory"""
    OUTPUT_DIR = "output"
    
    # Check if output directory exists
    if not os.path.exists(OUTPUT_DIR):
        print("\nNo local output directory found.")
        return
    
    # Get list of transcript files
    transcript_files = [f for f in os.listdir(OUTPUT_DIR) if f.endswith('.txt')]
    
    if not transcript_files:
        print("\nNo local transcripts found in output directory.")
        return
    
    # Ask for confirmation
    print(f"\nFound {len(transcript_files)} local transcript(s) in the output directory.")
    confirm = input("Are you sure you want to delete all local transcripts? This cannot be undone! (y/n): ")
    
    if confirm.lower() != 'y':
        print("Local deletion cancelled.")
        return
    
    # Delete files and count successes/failures
    deleted_count = 0
    error_count = 0
    
    print("\nDeleting local transcripts...")
    for file in transcript_files:
        try:
            file_path = os.path.join(OUTPUT_DIR, file)
            os.remove(file_path)
            deleted_count += 1
            print(f"Deleted {file} ({deleted_count}/{len(transcript_files)})")
        except Exception as e:
            error_count += 1
            print(f"Error deleting {file}: {str(e)}")
    
    # Optionally remove the output directory if empty
    if deleted_count == len(transcript_files):
        try:
            os.rmdir(OUTPUT_DIR)
            print("Removed empty output directory")
        except:
            pass
    
    print(f"\nLocal deletion complete:")
    print(f"Successfully deleted: {deleted_count}")
    print(f"Errors encountered: {error_count}")

def get_all_remote_transcripts():
    """Retrieve all transcripts from AssemblyAI"""
    transcriber = aai.Transcriber()
    all_transcripts = []
    
    print("\nRetrieving all remote transcripts...")
    
    # Setup pagination parameters
    params = aai.ListTranscriptParameters()
    
    # Get first page
    page = transcriber.list_transcripts(params)
    all_transcripts.extend(page.transcripts)
    
    # Continue getting pages until no more are available
    while page.page_details.before_id_of_prev_url is not None:
        print(f"Retrieved {len(all_transcripts)} transcripts so far...")
        params.before_id = page.page_details.before_id_of_prev_url
        page = transcriber.list_transcripts(params)
        all_transcripts.extend(page.transcripts)
    
    print(f"\nTotal remote transcripts found: {len(all_transcripts)}")
    return all_transcripts

def delete_remote_transcripts(transcripts):
    """Delete all provided remote transcripts"""
    if not transcripts:
        print("No remote transcripts to delete.")
        return
    
    # Ask for confirmation
    confirm = input(f"\nAre you sure you want to delete {len(transcripts)} remote transcripts from AssemblyAI? This cannot be undone! (y/n): ")
    if confirm.lower() != 'y':
        print("Remote deletion cancelled.")
        return
    
    print("\nDeleting remote transcripts...")
    deleted_count = 0
    error_count = 0
    
    for transcript in transcripts:
        try:
            aai.Transcript.delete_by_id(transcript.id)
            deleted_count += 1
            print(f"Deleted transcript {transcript.id} ({deleted_count}/{len(transcripts)})")
        except Exception as e:
            error_count += 1
            print(f"Error deleting transcript {transcript.id}: {str(e)}")
    
    print(f"\nRemote deletion complete:")
    print(f"Successfully deleted: {deleted_count}")
    print(f"Errors encountered: {error_count}")

def main():
    print("AssemblyAI Transcript Deletion Tool")
    print("==================================")
    
    try:
        # Setup environment
        setup_environment()
        
        # Handle local transcripts
        local_delete = input("\nWould you like to delete all local transcripts from the output folder? (y/n): ")
        if local_delete.lower() == 'y':
            delete_local_transcripts()
        else:
            print("Skipping local transcript deletion.")
        
        # Handle remote transcripts
        remote_delete = input("\nWould you like to delete all remote transcripts from AssemblyAI? (y/n): ")
        if remote_delete.lower() == 'y':
            transcripts = get_all_remote_transcripts()
            delete_remote_transcripts(transcripts)
        else:
            print("Skipping remote transcript deletion.")
        
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")
        return 1
    
    print("\nOperation complete!")
    return 0

if __name__ == "__main__":
    exit(main())