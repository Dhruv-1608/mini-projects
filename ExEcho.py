import os
import wave
import argparse
import hashlib
import base64
import getpass

parser = argparse.ArgumentParser(description="Extract your secret message from a WAV audio file.")
parser.add_argument('-f', required=True, help='Select Audio File (in .wav format)', dest='audiofile')
parser.add_argument('-p', '--password', help='Password to decrypt the message (optional)', dest='password')
args = parser.parse_args()

def clear_console():
    os.system("clear" if os.name == "posix" else "cls")

def banner():
    print("🎵 Extract Your Secret Message from WAV Audio File! 🎵")

def derive_key(password):
    """Derive a 32-byte key from password using PBKDF2"""
    salt = b'EchoEncryptSalt2025'  # Must match encryption salt
    key = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
    return key

def decrypt_message(encrypted_message, password):
    """Decrypt message using XOR cipher with SHA256 key"""
    try:
        key = derive_key(password)
        key_bytes = bytearray(key) * (len(encrypted_message) // len(key) + 1)
        decoded = base64.b64decode(encrypted_message)
        decrypted_bytes = bytearray(decoded)
        for i in range(len(decrypted_bytes)):
            decrypted_bytes[i] ^= key_bytes[i]
        return decrypted_bytes.decode()
    except Exception:
        return None

def extract_message(audio_file, password=None):
    """Extract a hidden message from a WAV audio file"""
    
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
    
    try:
        with wave.open(audio_file, mode='rb') as wave_audio:
            frame_bytes = bytearray(list(wave_audio.readframes(wave_audio.getnframes())))
            extracted_bits = [frame_bytes[i] & 1 for i in range(len(frame_bytes))]

            chars = []
            for i in range(0, len(extracted_bits), 8):
                byte = extracted_bits[i:i + 8]
                byte_str = ''.join(str(bit) for bit in byte)

                if len(byte_str) < 8:
                    continue  # Skip incomplete bytes

                if byte_str == '00000000':  # Stop decoding when end signal is found
                    break

                chars.append(chr(int(byte_str, 2)))

            decoded_message = ''.join(chars)
            
            # If password provided, try to decrypt
            if password:
                decrypted = decrypt_message(decoded_message, password)
                if decrypted:
                    print(f"🔓 Your Secret Message is: {decrypted}")
                else:
                    print("❌ Wrong password! Could not decrypt message.")
                    print(f"🔓 Raw extracted message: {decoded_message}")
            else:
                print(f"🔓 Your Secret Message is: {decoded_message}")
            
            return True

    except Exception as e:
        print("❌ Something went wrong while extracting the message!")
        print(f"Error: {e}")
        return False

# Main execution
clear_console()
banner()

# Get password if not provided as argument (for security)
password = args.password
if password:
    print("🔐 Password provided - will attempt decryption")

# If no password argument but user wants to use one, prompt for it
if not args.password:
    use_password = input("🔑 Is this message password protected? (y/n): ").strip().lower()
    if use_password == 'y':
        password = getpass.getpass("Enter password: ")

extract_message(args.audiofile, password)
