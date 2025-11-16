# Music to Sheet Music Transcriber

This project converts live musical instrument audio into sheet music notation.

## Requirements
- Python 3.8 or higher
- See requirements.txt for Python packages

## Installation
1. Create a virtual environment (recommended):
python -m venv venv source venv/bin/activate # On Windows: venv\Scripts\activate
2. Install requirements:
pip install -r requirements.txt

## Usage
1. Run the script:
python musicMaker.py
2. When prompted, play your instrument for 5 seconds
3. The script will create a MusicXML file that you can open with any sheet music software (like MuseScore, Finale, or Sibelius)

## Notes
- The transcription works best with clear, single-note melodies
- Make sure your microphone is properly configured
- To see the results, open the generated MusicXML file in your preferred sheet music software or use an online MusicXML viewer as SoundSlice

## Limitations
- It works best with single-note melodies
- It might not perfectly capture rhythm and timing
- Very fast passages might not be accurately transcribed
- Complex harmonies might not be properly detected