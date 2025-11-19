# Pitch Detector: Audio to Note Extractor

## Description

Tool made with Python for musicians and composers that automates the process of transcribing songs by ear. The algorithm isolates the main melody, tunes the frequencies (Auto-Tune), and generates a 'Raw' sheet music with the correct note sequence, ready for the musician to add rhythm in their preferred editor.

## Features
- Pitch detection with `librosa.piptrack`
- Onset detection (`librosa.onset.onset_detect`) to segment notes
- High‑pass melodic focus (ignora notas graves: filtro lógico > 250 Hz)
- Export to MusicXML vía `music21`
- Simple Gradio web GUI (subir archivo o grabar desde micrófono)
- Monophonic focus (melody; rhythm exported uniformly as eighth notes)
- WAV/MP3 input (handled by Gradio; resample automático)
- Adjustable recording duration (by default 5 s)

## Requirements
- Python 3.8 or higher
- See requirements.txt for Python packages (expected: librosa, numpy, sounddevice, music21, scipy, gradio)

## Installation
1. Create a virtual environment (recommended):
python -m venv venv source venv/bin/activate # On Windows: venv\Scripts\activate
2. Install requirements:
pip install -r requirements.txt

### Windows
```bash
python -m venv venv
venv\Scripts\activate
pip install -r [requirements.txt](http://_vscodecontentref_/0)
```

### macOS/Linux
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r [requirements.txt](http://_vscodecontentref_/0)
```

## Usage
1. Run the script:
python musicMaker.py
2. When prompted, play your instrument at least for 5 seconds
3. The script will create a MusicXML file that you can open with any sheet music software (like MuseScore, Finale, or Sibelius) or an online MusicXML viewer as SoundSlice

## Notes
- The transcription works best with clear, single-note melodies
- Make sure your microphone is properly configured

## Limitations
- It works best with single-note melodies
- It might not perfectly capture rhythm and timing
- Very fast passages might not be accurately transcribed
- Complex harmonies might not be properly detected
- Rhythm Agnostic: Every note is exported as an eighth note for easier post-editing.
- Melody Focus: Includes a high-pass filter to ignore low-pitched accompaniments (left hand of piano).
- Background Noise: Ensure a quiet environment for better pitch detection.