#!/usr/bin/env python3
import os
import wave
import argparse
import hashlib
import base64
import getpass

parser = argparse.ArgumentParser(description="EchoEncrypt - Audio Steganography")
parser.add_argument('-m', help='Secret message to hide', dest='secretmsg')
parser.add_argument('-f', help='Input audio file', dest='audiofile')
parser.add_argument('-o', help='Output audio file', dest='outputfile')
parser.add_argument('-p', '--password', help='Password for encryption/decryption')
args = parser.parse_args()

def clear_console():
    os.system("clear" if os.name == "posix" else "cls")

def banner():
    print("")
    print("   EchoEncrypt - Audio Steganography")
    print("   ================================")
    print("")

def derive_key(password):
    salt = b'EchoEncryptSalt2025'
    key = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
    return key

def encrypt_message(message, password):
    key = derive_key(password)
    key_bytes = bytearray(key) * (len(message) // len(key) + 1)
    encrypted = bytearray(message.encode())
    for i in range(len(encrypted)):
        encrypted[i] ^= key_bytes[i]
    return base64.b64encode(encrypted).decode()

def decrypt_message(encrypted_message, password):
    try:
        key = derive_key(password)
        key_bytes = bytearray(key) * (len(encrypted_message) // len(key) + 1)
        decoded = base64.b64decode(encrypted_message)
        decrypted_bytes = bytearray(decoded)
        for i in range(len(decrypted_bytes)):
            decrypted_bytes[i] ^= key_bytes[i]
        return decrypted_bytes.decode()
    except:
        return None

def hide_message(audio_file, secret_msg, output_file, password=None):
    if password:
        secret_msg = encrypt_message(secret_msg, password)
        print("[+] Message encrypted with password")
    
    if not os.path.exists(audio_file):
        print(f"[-] Error: Audio file '{audio_file}' not found!")
        return False
    
    try:
        with wave.open(audio_file, 'rb') as wave_audio:
            num_frames = wave_audio.getnframes()
            frame_bytes = bytearray(list(wave_audio.readframes(num_frames)))

            bits = [int(bit) for char in secret_msg for bit in format(ord(char), '08b')]
            end_signal = [0] * 8
            bits += end_signal

            if len(bits) > num_frames:
                print("[-] Message too large for audio file!")
                return False

            for i in range(len(bits)):
                frame_bytes[i] = (frame_bytes[i] & 254) | bits[i]

            with wave.open(output_file, 'wb') as out_audio:
                out_audio.setparams(wave_audio.getparams())
                out_audio.writeframes(bytes(frame_bytes))

        print("[+] Message hidden successfully!")
        return True
    except Exception as e:
        print(f"[-] Error: {e}")
        return False

def extract_message(audio_file, password=None):
    if not os.path.exists(audio_file):
        print(f"[-] Error: Audio file '{audio_file}' not found!")
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
                    continue
                if byte_str == '00000000':
                    break
                chars.append(chr(int(byte_str, 2)))

            decoded_message = ''.join(chars)
            
            if password:
                decrypted = decrypt_message(decoded_message, password)
                if decrypted:
                    print(f"[*] Your Secret Message is: {decrypted}")
                else:
                    print("[-] Wrong password!")
                    print(f"[*] Raw message: {decoded_message}")
            else:
                print(f"[*] Your Secret Message is: {decoded_message}")
            
            return True
    except Exception as e:
        print(f"[-] Error: {e}")
        return False

clear_console()
banner()

if args.secretmsg and args.audiofile and args.outputfile:
    hide_message(args.audiofile, args.secretmsg, args.outputfile, args.password)
elif args.audiofile:
    password = args.password
    if not password:
        use_pwd = input("[?] Is message password protected? (y/n): ").strip().lower()
        if use_pwd == 'y':
            password = getpass.getpass("Enter password: ")
    extract_message(args.audiofile, password)
else:
    print("Usage (Hide): python AudioEcho.py -f input.wav -m 'message' -o output.wav [-p password]")
    print("Usage (Extract): python AudioEcho.py -f output.wav [-p password]")
    print("")
