# src/voice_input.py
import pyaudio
import numpy as np
import time
import os
import wave
from faster_whisper import WhisperModel
from rich.console import Console

console = Console()

class VoiceInput:
    def __init__(self, model_size="tiny"):
        self.model_size = model_size
        try:
            console.print(f"[cyan]Loading Whisper model ({model_size})...[/cyan]")
            self.model = WhisperModel(model_size, device="cpu", compute_type="int8")
            console.print("[green]✅ Model loaded successfully[/green]")
        except Exception as e:
            console.print(f"[red]❌ Failed to load model: {e}[/red]")
            self.model = None

        self.audio_buffer = []
        self.is_recording = False
        self.vad_threshold = 0.02
        self.record_duration = 10
        self.sample_rate = 16000
        self.chunk_size = 1024

    def record_audio(self, duration=None):
        """Record audio for specified duration"""
        if duration is None:
            duration = self.record_duration

        console.print(f"[cyan]🎤 Recording for {duration} seconds...[/cyan]")

        try:
            p = pyaudio.PyAudio()
            stream = p.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=self.sample_rate,
                input=True,
                frames_per_buffer=self.chunk_size
            )

            frames = []
            for _ in range(0, int(self.sample_rate / self.chunk_size * duration)):
                data = stream.read(self.chunk_size)
                frames.append(data)

            stream.stop_stream()
            stream.close()
            p.terminate()

            # Save to temporary WAV file
            temp_file = "/tmp/dea_recording.wav"
            wf = wave.open(temp_file, 'wb')
            wf.setnchannels(1)
            wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
            wf.setframerate(self.sample_rate)
            wf.writeframes(b''.join(frames))
            wf.close()

            console.print("[green]✅ Recording complete[/green]")
            return temp_file

        except Exception as e:
            console.print(f"[red]❌ Recording failed: {e}[/red]")
            return None

    def transcribe_audio(self, audio_file):
        """Transcribe audio file using Whisper"""
        if not self.model:
            console.print("[red]❌ Model not loaded[/red]")
            return ""

        try:
            console.print("[cyan]🔄 Transcribing...[/cyan]")
            segments, info = self.model.transcribe(audio_file, beam_size=5)

            text = " ".join([segment.text for segment in segments])
            console.print(f"[green]✅ Transcription: {text}[/green]")
            return text.strip()

        except Exception as e:
            console.print(f"[red]❌ Transcription failed: {e}[/red]")
            return ""

    def get_voice_input(self):
        """Record and transcribe voice input"""
        audio_file = self.record_audio()
        if audio_file:
            text = self.transcribe_audio(audio_file)
            # Clean up temp file
            try:
                os.remove(audio_file)
            except:
                pass
            return text
        return ""
