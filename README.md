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
- The default recording duration is 5 seconds (can be modified in the code)

## To use this project:

First, install Python if you haven't already (Python 3.8 or higher recommended)
Create the directory structure and files as shown above
Follow the installation instructions in the README
You'll need a music notation software like MuseScore (free) to view the generated sheet music
The code uses several key libraries:

librosa for audio processing and pitch detection
sounddevice for recording audio from your microphone
music21 for creating and manipulating sheet music
numpy and scipy for numerical processing
The program will:

Record audio from your microphone
Analyze the audio to detect pitches
Convert the detected pitches into musical notes
Generate sheet music in MusicXML format

This is a basic implementation and has some limitations:

It works best with single-note melodies
It might not perfectly capture rhythm and timing
Very fast passages might not be accurately transcribed
Complex harmonies might not be properly detected