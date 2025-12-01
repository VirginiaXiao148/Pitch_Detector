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
with gr.Blocks(title="Pitch Detector: Audio to Note Extractor") as app:
    
    # Header and Instructions
    gr.Markdown(
        """
        # 🎵 Pitch Detector: Audio to Note Extractor
        
        **Turn your melody into sheet music!** 
        
        This tool analyzes your audio file or recording, detects the pitch, and generates a MusicXML file that you can open in MuseScore, Finale, or other notation software.
        
        ### 📝 How to use:
        1. **Upload** an audio file (.wav, .mp3) OR **Record** your melody directly.
        2. Click **Submit** (or just wait if auto-submit is on).
        3. **Download** the generated MusicXML file.
        
        ### 💡 Tips for best results:
        - **Single Note Melodies**: This tool works best with monophonic melodies (one note at a time).
        - **Clear Audio**: Ensure your recording is clear and free of background noise.
        - **Instrument**: Works well with voice, piano, guitar, etc.
        """
    )
    
    with gr.Row():
        with gr.Column(scale=1):
            # Input Section
            audio_input = gr.Audio(
                type="numpy", 
                label="🎤 Upload or Record",
                sources=["upload", "microphone"]
            )
            submit_btn = gr.Button("🎼 Transcribe", variant="primary")
        
        with gr.Column(scale=1):
            # Output Section
            result_text = gr.Textbox(label="ℹ️ Status Info")
            download_file = gr.File(label="📥 Download Sheet Music (MusicXML)")
            # Optional: Show code if needed, or keep it hidden/secondary
            # xml_code = gr.Code(label="XML Content", language="xml") 

    # Footer / Limitations
    with gr.Accordion("⚠️ Limitations & Technical Details", open=False):
        gr.Markdown(
            """
            - **Monophonic Only**: Does not support chords or polyphony.
            - **Rhythm**: All notes are exported as eighth notes (rhythm agnostic).
            - **Frequency Range**: Filters out frequencies below 250Hz to focus on melody.
            - **Accuracy**: Fast passages or complex harmonics might not be perfectly detected.
            """
        )

    # Event Listeners
    submit_btn.click(
        fn=transcriber.transcribe_from_file,
        inputs=audio_input,
        outputs=[result_text, download_file, gr.Code(label="XML Content", visible=False)] # Hidden code output for compatibility if needed, or just remove from return
    )


if __name__ == "__main__":
    app.launch()