import os
import subprocess
import yaml
from pathlib import Path
from rich.console import Console

console = Console()


class TextToSpeech:
    def __init__(self, config_path="config/config.yaml"):
        """Initialize TTS with Piper (primary) and espeak (fallback)"""
        self.load_config(config_path)

        self.piper_available = self.check_piper()
        self.espeak_available = self.check_espeak()

        if not self.piper_available:
            console.print("[yellow]⚠️ Piper unavailable — espeak will be used as fallback.[/yellow]")
        if not self.espeak_available:
            console.print("[yellow]⚠️ espeak unavailable — Piper only mode.[/yellow]")
        if not self.piper_available and not self.espeak_available:
            console.print("[red]❌ No TTS engines available![/red]")

    # ------------------------------------------------------
    # CONFIG
    # ------------------------------------------------------
    def load_config(self, config_path):
        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
        except Exception:
            config = {}

        self.tts_engine = config.get("tts_engine", "piper")
        self.piper_model = config.get("piper_model", "en_US-lessac-medium")
        self.piper_model_path = config.get("piper_model_path", "models/piper")

    # ------------------------------------------------------
    # ENGINE CHECKS
    # ------------------------------------------------------
    def check_piper(self):
        """Check if Piper is installed (binary or module)."""
        # Check for piper executable
        try:
            result = subprocess.run(["piper", "--version"], capture_output=True, timeout=2)
            if result.returncode == 0:
                console.print("[green]✅ Piper executable detected[/green]")
                return True
        except Exception:
            pass

        # Check for Python module ("piper-tts")
        try:
            import piper
            console.print("[green]✅ Piper Python module detected[/green]")
            return True
        except ImportError:
            pass

        return False

    def check_espeak(self):
        """Check if espeak binary exists."""
        try:
            result = subprocess.run(["espeak", "--version"], capture_output=True, timeout=2)
            return result.returncode == 0
        except Exception:
            return False

    # ------------------------------------------------------
    # PATHS AND MODELS
    # ------------------------------------------------------
    def get_model_path(self):
        """Return ONNX model path if available."""
        onnx = Path(self.piper_model_path) / f"{self.piper_model}.onnx"
        json = Path(self.piper_model_path) / f"{self.piper_model}.onnx.json"
        return str(onnx) if onnx.exists() and json.exists() else None

    # ------------------------------------------------------
    # SPEAK — MAIN ENTRY
    # ------------------------------------------------------
    def speak(self, text, force_engine=None):
        if not text or not text.strip():
            return

        console.print(f"[cyan]🔊 Speaking: {text[:50]}...[/cyan]")

        # Forced engine
        if force_engine == "piper":
            if not self.piper_available:
                console.print("[red]Piper forced but NOT available[/red]")
                return False
            return self.speak_piper(text)

        if force_engine == "espeak":
            if not self.espeak_available:
                console.print("[red]espeak forced but NOT available[/red]")
                return False
            return self.speak_espeak(text)

        # AUTO: Piper first
        if self.piper_available:
            if self.speak_piper(text):
                return True
            console.print("[yellow]⚠️ Piper failed — falling back to espeak[/yellow]")

        # Fallback
        if self.espeak_available:
            return self.speak_espeak(text)

        console.print("[red]❌ No TTS engine available[/red]")
        return False

    # ------------------------------------------------------
    # PIPER SPEAKING
    # ------------------------------------------------------
    def speak_piper(self, text):
        """Speak using Piper either via Python module or CLI."""
        model_path = self.get_model_path()
        if not model_path:
            console.print(f"[red]❌ Piper model missing: {self.piper_model}[/red]")
            return False

        # 1) Try Python module first (BEST, stable)
        try:
            import piper
            synthesizer = piper.PiperVoice.load(model_path)
            wav = synthesizer.synthesize(text)
            return self._play_wav_bytes(wav)
        except Exception as e:
            console.print(f"[yellow]Python Piper failed: {e}[/yellow]")

        # 2) Try CLI fallback
        try:
            import tempfile

            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tf:
                wav_file = tf.name

            cmd = ["piper", "--model", model_path, "--output_file", wav_file]
            process = subprocess.Popen(cmd, stdin=subprocess.PIPE)
            process.communicate(text.encode(), timeout=20)

            if os.path.exists(wav_file):
                self._play_file(wav_file)
                os.remove(wav_file)
                return True
        except Exception as e:
            console.print(f"[red]Piper CLI failed: {e}[/red]")

        return False

    # ------------------------------------------------------
    # ESPEAK SPEAKING
    # ------------------------------------------------------
    def speak_espeak(self, text):
        try:
            result = subprocess.run(
                ["espeak", "-s", "150", "-a", "100", text],
                capture_output=True,
                timeout=30
            )
            return result.returncode == 0
        except Exception as e:
            console.print(f"[red]espeak error: {e}[/red]")
            return False

    # ------------------------------------------------------
    # AUDIO PLAYBACK HELPERS
    # ------------------------------------------------------
    def _play_file(self, path):
        subprocess.run(["aplay", "-q", path], capture_output=True)

    def _play_wav_bytes(self, wav_bytes):
        """Play WAV bytes from piper Python module."""
        import tempfile
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tf:
            tf.write(wav_bytes)
            tf.flush()
            self._play_file(tf.name)
        os.remove(tf.name)
        return True
