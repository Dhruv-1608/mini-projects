# EchoEncrypt v2.1

Audio & Image Steganography Tool

## Project Structure

| File | Description |
|------|-------------|
| EchoEncrypt.py | Main dashboard - run this to start |
| AudioEcho.py | Audio steganography module |
| ImageEcho.py | Image steganography module |

## Installation

```bash
pip install pillow
```

## Usage

### 1. Run Main Dashboard
```bash
python EchoEncrypt.py
```

### 2. Choose Option
- [1] Audio Steganography
- [2] Image Steganography
- [0] Exit

### Audio Commands
```bash
python AudioEcho.py -f input.wav -m "message" -o output.wav
python AudioEcho.py -f input.wav -m "message" -o output.wav -p password
python AudioEcho.py -f output.wav
python AudioEcho.py -f output.wav -p password
```

### Image Commands
```bash
python ImageEcho.py -f input.png -m "message" -o output.png
python ImageEcho.py -f input.png -m "message" -o output.png -p password
python ImageEcho.py -f output.png
python ImageEcho.py -f output.png -p password
```

## Features
- Hide messages in WAV audio files
- Hide messages in PNG images
- Password protection
- Extract hidden messages

## License
MIT
