# EchoEncrypt v2.1

Audio & Image Steganography Tool

## Project Structure

```
EchoEncrypt/
├── EchoEncrypt.py      # Main dashboard - run this to start
├── modules/
│   ├── AudioEcho.py    # Audio steganography module
│   └── ImageEcho.py    # Image steganography module
├── assets/
│   ├── hello.wav       # Test audio file
│   └── Test.wav        # Test audio file
├── .gitignore
├── LICENSE
└── README.md
```

## Installation

```bash
pip install pillow
```

## Usage

### 1. Run Main Dashboard
```bash
python EchoEncrypt.py
```

### 2. Run Modules Standalone (Interactive Mode)
```bash
# Audio Steganography - Interactive
python modules/AudioEcho.py

# Image Steganography - Interactive
python modules/ImageEcho.py
```

### 3. Main Menu Options
- [1] Audio Steganography
- [2] Image Steganography
- [3] About
- [0] Exit

### Audio Commands (CLI Mode)
```bash
python modules/AudioEcho.py -f input.wav -m "message" -o output.wav
python modules/AudioEcho.py -f input.wav -m "message" -o output.wav -p password
python modules/AudioEcho.py -f output.wav
python modules/AudioEcho.py -f output.wav -p password
```

### Image Commands (CLI Mode)
```bash
python modules/ImageEcho.py -f input.png -m "message" -o output.png
python modules/ImageEcho.py -f input.png -m "message" -o output.png -p password
python modules/ImageEcho.py -f output.png
python modules/ImageEcho.py -f output.png -p password
```

## Features
- Hide messages in WAV audio files
- Hide messages in PNG images
- Password protection
- Extract hidden messages

## License
MIT