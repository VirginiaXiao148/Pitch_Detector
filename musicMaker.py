import librosa
import numpy as np
import music21

import gradio as gr

class MusicTranscriber:
    
    def __init__(self):
        """
        The function initializes variables for sample rate in a Python class.
        """
        self.sample_rate = 44100
        
    def process_audio(self, audio_data):
        # Convert to mono if necessary
        if len(audio_data.shape) > 1:
            audio_data = audio_data.mean(axis=1)
            
        # Perform pitch detection using librosa
        pitches, magnitudes = librosa.piptrack(y=audio_data,
                                                sr=self.sample_rate)
        
        onset_frames = librosa.onset.onset_detect(y=audio_data,
                                                    sr=self.sample_rate,
                                                    units = 'frames'
                                                )
        # Get the most prominent pitch at each time
        pitches_found = []
        for frame in onset_frames:
            index = magnitudes[:, frame].argmax()
            pitch = pitches[index, frame]
            if pitch > 250 and pitch < 3000 and np.isfinite(pitch):
                pitches_found.append(pitch)
                
        return pitches_found
    
    def create_sheet_music(self, pitches):
        # Create a music21 stream
        stream = music21.stream.Stream()
        
        # Convert frequencies to notes
        for pitch in pitches:
            # Convert frequency to midi note number
            midi_float = librosa.hz_to_midi(pitch)
            midi_note = round(midi_float)
            # Create a music21 note
            note = music21.note.Note(midi_note)
            note.duration.quarterLength = 0.5  # Set duration (adjust as needed)
            stream.append(note)
            
        return stream
    
    def save_sheet_music(self, stream, filename="output.xml"):
        # Save as MusicXML file
        stream.write('musicxml', fp=filename)
        print(f"Sheet music saved as {filename}")
    
    def transcribe_from_file(self, audio_file):
        
        try:
            if audio_file is None:
                print("No audio file provided.")
                return
            
            # 1. Load audio file
            sr_original, audio_data = audio_file
            
            # Transform to float32
            audio_data_float = librosa.util.buf_to_float(audio_data)
            
            # 2. Resample if necessary
            if sr_original != self.sample_rate:
                audio_data_float = librosa.resample(y=audio_data_float, orig_sr=sr_original, target_sr=self.sample_rate)
                
            # 3. Process audio to get pitches
            pitches = self.process_audio(audio_data_float)
            
            if pitches is None or len(pitches) == 0:
                print("No pitches detected in the audio file.")
                return
            
            # 4. Create sheet music
            stream = self.create_sheet_music(pitches)
            # 5. Save sheet music
            output_filename = "output_sheet_music.xml"
            self.save_sheet_music(stream, filename=output_filename)

            # 6. Read XML file
            with open(output_filename, "r", encoding="utf-8") as f:
                xml_content = f.read()
            
            # 7. Return the output filename for GUI display
            return f"Transcriptión completed. {len(pitches)} detected pitchs.", output_filename, xml_content
        
        except Exception as e:
            print(f"An error occurred during transcription: {e}")
            return f"An error occurred: {e}", None, None


# GUI

# Create instance of MusicTranscriber
transcriber = MusicTranscriber()

# Create Gradio interface
app = gr.Interface(
    fn=transcriber.transcribe_from_file,
    
    inputs=gr.Audio(type="numpy", label="Upload .wav/.mp3 Audio File or record your melody"),
    
    outputs=[
        gr.Textbox(label="Result"),
        gr.File(label="Download sheet music (MusicXML)"),
        gr.Code(label="Sheet Music (MusicXML Content)")
    ],
    
    title="Pitch Detector: Audio to Note Extractor",
    description="Upload an audio file or record your melody to get the sheet music (MusicXML format)."
    
)


if __name__ == "__main__":
    app.launch()