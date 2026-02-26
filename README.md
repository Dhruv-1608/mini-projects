# 🎵 EchoEncrypt - Audio Steganography Tool

A Python-based steganography tool that allows you to hide secret messages inside WAV audio files using LSB (Least Significant Bit) technique.

![Python](https://img.shields.io/badge/Python-3.x-blue)
![License](https://img.shields.io/badge/License-MIT-green)

## 🔐 Features

- **Hide Messages** - Embed secret text into WAV audio files
- **Extract Messages** - Retrieve hidden messages from encoded audio
- **Password Protection** - Encrypt your messages with AES-256 encryption (optional)
- **User-Friendly** - Simple command-line interface with emoji feedback
- **Error Handling** - Robust validation and helpful error messages

## 📦 Installation

### Prerequisites
- Python 3.x

```bash
# No external dependencies required!
# Uses only Python standard library
```

### Clone the Repository
```bash
git clone https://github.com/Dhruv-1608/EchoEncrypt.git
cd EchoEncrypt
```

## 🚀 Usage

### Hiding a Message (Encryption)

```bash
# Without password (basic)
python EchoEncrypt.py -f input.wav -m "Your secret message" -o output.wav

# With password protection (encrypted)
python EchoEncrypt.py -f input.wav -m "Your secret message" -o output.wav -p "your_password"
```

**Arguments:**
| Flag | Description | Required |
|------|-------------|----------|
| `-f` | Input WAV audio file | Yes |
| `-m` | Secret message to hide | Yes |
| `-o` | Output file name | Yes |
| `-p, --password` | Password for encryption | No |

### Extracting a Message (Decryption)

```bash
# Extract without password
python ExEcho.py -f output.wav

# Extract with password
python ExEcho.py -f output.wav -p "your_password"
```

**Arguments:**
| Flag | Description | Required |
|------|-------------|----------|
| `-f` | Encoded WAV audio file | Yes |
| `-p, --password` | Password for decryption | No |

## 💡 Examples

### Example 1: Basic Usage
```bash
# Hide a message
python EchoEncrypt.py -f Test.wav -m "Hello World" -o hidden.wav

# Extract the message
python ExEcho.py -f hidden.wav
# Output: Your Secret Message is: Hello World
```

### Example 2: With Password
```bash
# Hide a message with password
python EchoEncrypt.py -f Test.wav -m "Secret Data" -o hidden.wav -p "MySecurePass123"

# Extract using password
python ExEcho.py -f hidden.wav -p "MySecurePass123"
# Output: Your Secret Message is: Secret Data
```

## 🔒 How It Works

### LSB Steganography
The tool uses the **Least Significant Bit** technique:
1. Each audio sample contains bytes of data
2. We modify the last bit of each byte to store our message
3. The change is virtually undetectable to the human ear
4. The end of the message is marked with a null byte (`00000000`)

### Password Encryption
When a password is provided:
1. The message is encrypted using **AES-256** (via Fernet)
2. A key is derived from your password using **SHA256**
3. Only someone with the correct password can decrypt the message

## ⚠️ Limitations

- Only supports **WAV** audio files
- Message size is limited by audio file size
- Encrypted messages are longer than plaintext

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License.

## 👤 Author

**Dhruv-1608**
- GitHub: [@Dhruv-1608](https://github.com/Dhruv-1608)

---

⭐ Star this repo if you found it useful!
