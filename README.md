# AssemblyAI Audio Transcription Tool

A Python-based tool for automated audio transcription using AssemblyAI's API. This project provides scripts for batch processing audio files, managing transcripts both locally and remotely, and cleaning up transcription data.

## Features

### Audio Transcription (`simple-transcribe.py`)
- Automatically transcribes audio files from an input directory
- Supports multiple audio formats (.mp3, .mp4, .wav, .m4a, .flac)
- Moves processed files to a completed folder
- Saves transcripts to an output directory
- Option to delete individual transcripts from AssemblyAI after processing

### Transcript Management (`delete-transcripts.py`)
- Manages both local and remote transcripts
- Option to delete all local transcripts from the output folder
- Option to delete all remote transcripts stored on AssemblyAI
- Provides detailed progress updates and confirmation prompts
- Error handling and operation summaries

## Directory Structure

```
├── input/ # Place audio files here for transcription
│ └── completed/ # Processed audio files are moved here
├── output/ # Transcription text files are saved here
├── .env # Environment variables (API key)
├── simple-transcribe.py # Main transcription script
└── delete_all_transcripts.py # Transcript management script
```

## Setup

1. Install required Python packages:
```bash
pip install assemblyai python-dotenv
```

2. Create a `.env` file in the project root with your AssemblyAI API key:

ASSEMBLYAI_API_KEY=your_api_key_here


3. Create the required directories (or let the scripts create them automatically):
```bash
mkdir input output
mkdir input/completed
```

## Usage

### Transcription Script
To transcribe audio files:

1. Place audio files in the `input` directory
2. Run the transcription script:
```bash
python simple-transcribe.py
```
- Transcribed files will be saved to the `output` directory
- Original audio files will be moved to `input/completed`
- You'll be prompted about deleting transcripts from AssemblyAI

### Transcript Management Script
To manage existing transcripts:

1. Run the management script:
```bash
python delete-transcripts.py
```
- You'll be prompted about deleting local transcripts
- You'll be prompted about deleting remote transcripts
- Detailed progress will be shown for each operation

## Important Notes

- Supported audio formats: .mp3, .mp4, .wav, .m4a, .flac
- Keep your API key secure and never commit the `.env` file
- Transcript deletions cannot be undone
- The scripts include confirmation prompts before deletions

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## License

MIT License

Copyright (c) 2025 Lane Denson

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Acknowledgments

- [AssemblyAI](https://www.assemblyai.com/) for their transcription API
- [python-dotenv](https://github.com/theskumar/python-dotenv) for environment management