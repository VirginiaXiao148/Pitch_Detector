import librosa
import numpy as np
import sounddevice as sd
import music21
from scipy.io import wavfile
import time

import gradio as gr

class MusicTranscriber:
    
    def __init__(self):
        """
        The function initializes variables for sample rate and recording duration in a Python class.
        """
        self.sample_rate = 44100
        self.duration = 5  # recording duration in seconds
    
    def record_audio(self):
        """
        The `record_audio` function records audio input from an instrument for a specified duration
        using the sounddevice library in Python.
        :return: The function `record_audio` returns the audio data recorded from the input source
        (e.g., instrument) as a NumPy array.
        """
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
            if pitch > 0 and np.isfinite(pitch):
                pitches_found.append(pitch)
                
        return pitches_found
    
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
        
    def transcribe_from_mic(self):
        # Main workflow
        """
        The function transcribes audio data into sheet music by recording audio, processing it to
        extract pitches, creating sheet music, and saving the result.
        """
        audio_data = self.record_audio()
        pitches = self.process_audio(audio_data)
        stream = self.create_sheet_music(pitches)
        self.save_sheet_music(stream)
    
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
    
    def save_wav(self, audio_data, filename="output.wav"):
        """
        The `save_wav` function saves audio data as a WAV file with a specified filename and sample
        rate.
        
        :param audio_data: The `audio_data` parameter in the `save_wav` method is the actual audio data
        that you want to save as a WAV file. This data could be in the form of a NumPy array or a list
        containing the audio samples
        :param filename: The `filename` parameter is a string that specifies the name of the file where
        the audio data will be saved. By default, it is set to "output.wav" if no value is provided when
        calling the `save_wav` method, defaults to output.wav (optional)
        """
        wavfile.write(filename, self.sample_rate, audio_data)
        print(f"Audio saved as {filename}")
        
    def load_archive(self, filename):
        """
        The function `load_archive` loads an audio file using the librosa library with a specified
        sample rate.
        
        :param filename: The `filename` parameter is a string that represents the path to the audio file
        that you want to load and process. It is the name of the file that contains the audio data you
        want to work with
        :return: the audio waveform `y` loaded from the specified filename.
        """
        y, sr = librosa.load(filename, sr=self.sample_rate)
        return y



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
    
    title="Music Transcriber",
    description="Upload an audio file or record your melody to transcribe it into sheet music (MusicXML format)."
    
)
app.launch()


if __name__ == "__main__":
    ''' transcriber = MusicTranscriber()
    transcriber.transcribe() '''


    # Optionally save the recorded audio
    # audio_data = transcriber.record_audio()
    # transcriber.save_wav(audio_data)
    # Optionally load and process an archived audio file
    # archived_audio = transcriber.load_archive("path_to_your_file.wav")
    # pitches = transcriber.process_audio(archived_audio)
    # stream = transcriber.create_sheet_music(pitches)
    # transcriber.save_sheet_music(stream, filename="archived_output.xml")
    
    
    app.launch()