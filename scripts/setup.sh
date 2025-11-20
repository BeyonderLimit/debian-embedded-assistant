#!/bin/bash
# scripts/setup.sh

set -e

echo "🚀 Setting up Debian Embedded Assistant..."

# Update system
sudo apt update

# Install system dependencies
sudo apt install -y \
    python3 \
    python3-pip \
    python3-venv \
    python3-dev \
    portaudio19-dev \
    alsa-utils \
    pulseaudio \
    sox \
    ffmpeg \
    espeak \
    nano \
    calcurse \
    wget

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install Python dependencies
pip install -r requirements.txt

# Install Piper TTS
echo "📦 Installing Piper TTS..."
pip install piper-tts

# Alternative: Install Piper standalone binary
echo "🔧 Checking for Piper standalone..."
if ! command -v piper &> /dev/null; then
    echo "📥 Installing Piper standalone binary..."

    # Detect architecture
    ARCH=$(uname -m)
    if [ "$ARCH" = "x86_64" ]; then
        PIPER_URL="https://github.com/rhasspy/piper/releases/download/v1.2.0/piper_amd64.tar.gz"
    elif [ "$ARCH" = "aarch64" ]; then
        PIPER_URL="https://github.com/rhasspy/piper/releases/download/v1.2.0/piper_arm64.tar.gz"
    else
        echo "⚠️ Unsupported architecture: $ARCH"
        echo "Piper may not work correctly. espeak will be used as fallback."
    fi

    if [ ! -z "$PIPER_URL" ]; then
        wget -q --show-progress "$PIPER_URL" -O piper.tar.gz
        tar -xzf piper.tar.gz
        sudo mv piper/piper /usr/local/bin/
        sudo chmod +x /usr/local/bin/piper
        rm -rf piper piper.tar.gz
        echo "✅ Piper installed to /usr/local/bin/piper"
    fi
else
    echo "✅ Piper already installed"
fi

# Create necessary directories
mkdir -p data
mkdir -p models/piper

# Initialize tasks file
echo "[]" > data/tasks.json

# Download recommended Piper voice model
echo "📥 Downloading Piper voice model (en_US-lessac-medium)..."
echo "This may take a few minutes..."

# Create download script
cat > download_piper_model.py << 'EOF'
import sys
sys.path.insert(0, 'src')
from tts import TextToSpeech

tts = TextToSpeech()
print("\n🎤 Downloading default voice model...")
success = tts.download_model('en_US-lessac-medium')
if success:
    print("\n✅ Voice model downloaded successfully!")
    print("You can test it with: say Hello world")
else:
    print("\n⚠️ Voice model download failed.")
    print("Trying alternative model (en_US-amy-medium)...")
    success = tts.download_model('en_US-amy-medium')
    if success:
        print("✅ Alternative voice downloaded!")
    else:
        print("⚠️ Download failed. Using espeak as fallback.")
        print("\nTo download manually later, run:")
        print("  python -c 'from src.tts import TextToSpeech; tts = TextToSpeech(); tts.download_model(\"en_US-lessac-medium\")'")
EOF

python download_piper_model.py
rm download_piper_model.py

echo ""
echo "✅ Setup complete!"
echo ""
echo "📝 Available Piper voice models:"
echo "  - en_US-lessac-medium (default, balanced)"
echo "  - en_US-amy-low (faster, lower quality)"
echo "  - en_US-ryan-high (slower, higher quality)"
echo ""
echo "To download additional voices:"
echo "  python -c 'from src.tts import TextToSpeech; tts = TextToSpeech(); tts.download_model(\"MODEL_NAME\")'"
echo ""
echo "Run the assistant with: ./scripts/run-assistant.sh"
