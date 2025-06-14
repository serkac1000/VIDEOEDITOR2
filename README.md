# Video Editor GUI - Cross Platform

A desktop application for voice-controlled video editing with a graphical user interface.

## Features

- 🎬 Load and preview video files
- ✂️ Cut video segments with precise timing
- 🎤 Voice command support (when audio is available)
- 🖱️ Manual time selection with visual controls
- 🎯 Real-time video playback with seeking
- 📊 Progress tracking for video processing
- 🔊 Audio transcription using Hugging Face API

## System Requirements

- Python 3.8 or higher
- Windows 10/11, macOS 10.14+, or Linux with GUI support
- 2GB RAM minimum
- Internet connection for voice transcription features

## Installation

### Windows (Recommended)

1. Extract the zip file to a folder
2. Double-click `run_windows.bat`
3. The setup will automatically install required packages
4. The application will start automatically

### Manual Installation (All Platforms)

1. Install Python 3.8+ from https://python.org
2. Extract the application files
3. Open terminal/command prompt in the application folder
4. Run: `python setup.py`
5. Start the app: `python main.py`

## Usage

### Basic Video Editing

1. **Load Video**: Click "Browse" to select your video file
2. **Set Times**: 
   - Use the video player to find start/end points
   - Click "Set as Start" and "Set as End" buttons
   - Or manually enter times in seconds
3. **Process**: Click "Cut and Save Video" and choose output location

### Voice Commands (Optional)

1. **Setup API**: Enter your Hugging Face API token
2. **Test Connection**: Click "Test API" to verify
3. **Record Command**: Click "Record Voice Command" and speak
   - Example: "Cut from 10 to 30 seconds"
4. **Apply**: Times will be automatically filled

### API Token Setup

1. Visit https://huggingface.co/settings/tokens
2. Create a new token with read permissions
3. Enter the token in the API Token field
4. Click "Test API" to verify connection

## Supported Formats

- **Input**: MP4, AVI, MOV, MKV, WMV
- **Output**: MP4 (H.264 with AAC audio)

## Troubleshooting

### Audio Recording Issues
- Audio recording requires system audio drivers
- On some systems, voice commands may not be available
- The app will work without audio for manual editing

### Video Playback Issues
- Ensure video codecs are supported
- Try converting video to MP4 format first
- Check that the video file is not corrupted

### Performance Tips
- Close other applications while processing large videos
- Use shorter video segments for faster processing
- Ensure sufficient disk space for output files

## File Structure

```
video-editor-gui/
├── main.py              # Main application entry
├── setup.py             # Cross-platform setup
├── run_windows.bat      # Windows launcher
├── video_editor_gui.py  # Main GUI interface
├── video_player.py      # Video playback component
├── video_processor.py   # Video editing logic
├── audio_processor.py   # Voice command handling
├── utils.py             # Utility functions
└── README.md           # This file
```

## License

This project is provided as-is for educational and personal use.

## Support

For issues or questions, check the log section in the application for error details.