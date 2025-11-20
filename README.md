# debian-embedded-assistant
## 🔧 `README.md`

```markdown
# 🚀 Debian Embedded Assistant (DEA)

A FOSS, TTY-based embedded assistant for Debian 12 with voice input, task management, system monitoring, and app launching.

## Features

- ✅ Voice input via faster-whisper (offline)
- ✅ Text input support
- ✅ Task creation and tracking
- ✅ Real-time system monitoring (CPU, RAM, Battery, Brightness)
- ✅ Weather display (Open-Meteo, no API key)
- ✅ App launching (volume, brightness, notes, calendar)
- ✅ Runs in TTY without GUI
- ✅ 100% FOSS, no external APIs required

## Requirements

- Debian 12 (or similar Linux)
- 8GB RAM minimum
- Python 3.10+
- Microphone (for voice input)

## Quick Start

1. **Clone repository:**
   ```bash
   git clone https://github.com/BeyonderLimit/debian-embedded-assistant.git
   cd debian-embedded-assistant
   ```

2. **Run setup:**
   ```bash
   chmod +x scripts/*.sh
   ./scripts/setup.sh
   ```

3. **Start assistant:**
   ```bash
   ./scripts/run-assistant.sh
   ```

## Usage

### Available Commands

- `dictation` - Record voice input and add as task
- `show tasks` - List all tasks
- `add task [text]` - Add a task manually
- `volume up/down` - Adjust system volume
- `brightness up/down` - Adjust screen brightness
- `mute/unmute` - Mute/unmute audio
- `weather` - Show current weather
- `status` - Show system status
- `notes` - Open notes editor
- `calendar` - Show calendar
- `help` - Show command menu
- `exit` - Quit assistant

## Technical Details

### Voice Recognition
- Uses faster-whisper (Whisper model optimized for CPU)
- Default model: "tiny" (fast, low memory)
- Can be changed to "base", "small", or "medium" in code

### Storage
- Tasks stored in `data/tasks.json`
- All data is local, no cloud sync

### System Requirements
- CPU: Any modern x86-64 processor
- RAM: 8GB (voice model uses ~1-2GB)
- Disk: ~500MB for models and dependencies

## Troubleshooting

### Audio Issues
```bash
# Test microphone
arecord -d 5 test.wav
aplay test.wav

# Fix PulseAudio
pulseaudio --kill
pulseaudio --start
```

### Brightness Control Not Working
```bash
# Install brightnessctl
sudo apt install brightnessctl

# Add user to video group
sudo usermod -aG video $USER
```

## Future Enhancements

- [ ] Wikipedia search integration
- [ ] DuckDuckGo search via w3m
- [ ] Persistent reminders/notifications
- [ ] SQLite database instead of JSON
- [ ] Cron integration for scheduled tasks
- [ ] Email notifications

## License

MIT License - see LICENSE file

## Contributing

Pull requests welcome! Please test on Debian 12 before submitting.
```

---

## Key Fixes Applied:

1. **Fixed imports** - All necessary imports added to each file
2. **Fixed voice_input.py** - Properly handles audio recording and transcription
3. **Fixed main.py** - Corrected function calls and imports
4. **Added proper error handling** throughout
5. **Fixed system_monitor.py** - Added proper battery/brightness detection
6. **Fixed app_launcher.py** - Updated commands for modern Linux
7. **Created proper setup scripts**
8. **Added .gitignore**
9. **Fixed UI functions** - All properly defined with correct imports
10. **Fixed task_manager.py** - Ensures data directory exists

The project is now ready to clone and run!
  
