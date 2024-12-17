import librosa
import numpy as np
import sounddevice as sd
import music21
from scipy.io import wavfile
import time

class MusicTranscriber:
    def __init__(self):
        self.sample_rate = 44100
        self.duration = 5  # recording duration in seconds
        
    def record_audio(self):
        print("Recording... Please play your instrument")
        audio_data = sd.rec(int(self.sample_rate * self.duration),
                          samplerate=self.sample_rate,
                          channels=1)
        sd.wait()
        return audio_data
        
    def process_audio(self, audio_data):
        # Convert to mono if necessary
        if len(audio_data.shape) > 1:
            audio_data = audio_data.mean(axis=1)
            
        # Perform pitch detection using librosa
        pitches, magnitudes = librosa.piptrack(y=audio_data.flatten(),
                                             sr=self.sample_rate)
        
        # Get the most prominent pitch at each time
        pitches_with_mag = []
        for i in range(len(pitches[0])):
            index = magnitudes[:,i].argmax()
            pitch = pitches[index][i]
            if pitch > 0:  # Filter out silence
                pitches_with_mag.append(pitch)
                
        return pitches_with_mag
    
    def create_sheet_music(self, pitches):
        # Create a music21 stream
        stream = music21.stream.Stream()
        
        # Convert frequencies to notes
        for pitch in pitches:
            # Convert frequency to midi note number
            midi_note = librosa.hz_to_midi(pitch)
            # Create a music21 note
            note = music21.note.Note(midi_note)
            note.duration.quarterLength = 0.5  # Set duration (adjust as needed)
            stream.append(note)
            
        return stream
    
    def save_sheet_music(self, stream, filename="output.xml"):
        # Save as MusicXML file
        stream.write('musicxml', fp=filename)
        print(f"Sheet music saved as {filename}")
        
    def transcribe(self):
        # Main workflow
        audio_data = self.record_audio()
        pitches = self.process_audio(audio_data)
        stream = self.create_sheet_music(pitches)
        self.save_sheet_music(stream)

if __name__ == "__main__":
    transcriber = MusicTranscriber()
    transcriber.transcribe()