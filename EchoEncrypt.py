import os
import wave
import argparse
import hashlib
import base64

parser = argparse.ArgumentParser(description="Hide a secret message in a WAV audio file.")
parser.add_argument('-f', required=True, help='Select Audio File (in .wav format)', dest='audiofile')
parser.add_argument('-m', required=True, help='Enter your Secret Message', dest='secretmsg')
parser.add_argument('-o', required=True, help='Output file path and name', dest='outputfile')
parser.add_argument('-p', '--password', help='Password to encrypt the message (optional)', dest='password')
args = parser.parse_args()

def clear_console():
    os.system("clear" if os.name == "posix" else "cls")

def banner():
    print("🎶 Hide Your Secret Message in WAV Audio File! 🎶")

def derive_key(password):
    """Derive a 32-byte key from password using PBKDF2"""
    salt = b'EchoEncryptSalt2025'  # Static salt for simplicity
    key = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
    return key

def encrypt_message(message, password):
    """Encrypt message using XOR cipher with SHA256 key"""
    key = derive_key(password)
    key_bytes = bytearray(key) * (len(message) // len(key) + 1)
    encrypted = bytearray(message.encode())
    for i in range(len(encrypted)):
        encrypted[i] ^= key_bytes[i]
    return base64.b64encode(encrypted).decode()

def hide_message(audio_file, secret_msg, output_file, password=None):
    """Hide a secret message in a WAV audio file using LSB steganography"""
    
    # Handle password encryption if provided
    if password:
        secret_msg = encrypt_message(secret_msg, password)
        print("🔐 Message encrypted with password")
    
    # Validate input file
    if not os.path.exists(audio_file):
        print(f"❌ Error: Audio file '{audio_file}' not found!")
        return False
    
    # Check if it's a valid WAV file
    try:
        with wave.open(audio_file, 'rb') as wave_audio:
            if wave_audio.getnchannels() < 1 or wave_audio.getsampwidth() < 1:
                print("❌ Error: Invalid WAV file format!")
                return False
    except wave.Error as e:
        print(f"❌ Error: Not a valid WAV file! {e}")
        return False
    except Exception as e:
        print(f"❌ Error reading audio file: {e}")
        return False
    
    # Open the input audio file
    with wave.open(audio_file, 'rb') as wave_audio:
        num_frames = wave_audio.getnframes()
        frame_bytes = bytearray(list(wave_audio.readframes(num_frames)))

        # Prepare message with end signal (0b00000000)
        bits = [int(bit) for char in secret_msg for bit in format(ord(char), '08b')]
        end_signal = [0] * 8  # Signal end of message
        bits += end_signal  # Append end signal

        available_bits = num_frames

        if len(bits) > available_bits:
            print("💡 The message is too large to fit in the audio file.")
            print(f"📏 Available capacity: {available_bits} bits")
            print(f"📝 Your message size: {len(bits)} bits including end signal")
            return False

        # Modify frame bytes with the message bits
        for i in range(len(bits)):
            frame_bytes[i] = (frame_bytes[i] & 254) | bits[i]  # Set LSB according to message bits

        with wave.open(output_file, 'wb') as out_audio:
            out_audio.setparams(wave_audio.getparams())
            out_audio.writeframes(bytes(frame_bytes))

    print("✅ Message hidden successfully in the audio file!")
    if password:
        print("🔑 Remember your password to decrypt the message!")
    return True

# Main execution
clear_console()
banner()
try:
    success = hide_message(args.audiofile, args.secretmsg, args.outputfile, args.password)
    if not success:
        print("\n❌ Failed to hide message.")
except Exception as e:
    print("❌ Something went wrong! Please try again.")
    print(f"Error: {e}")
