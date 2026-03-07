#!/usr/bin/env python3
import os
import wave
import argparse
import hashlib
import base64
import getpass
import sys

def clear_console():
    os.system("clear" if os.name == "posix" else "cls")

def show_banner():
    print("")
    print("                                                 ")
    print(" _____     _       _____                     _   ")
    print("|   __|___| |_ ___|   __|___ ___ ___ _ _ ___| |_ ")
    print("|   __|  _|   | . |   __|   |  _|  _| | | . |  _|")
    print("|_____|___|_|_|___|_____|_|_|___|_| |_  |  _|_|  ")
    print("                                    |___|_|      ")
    print("")
    print("          Audio Steganography Module")
    print("   ========================================")
    print("")

def show_menu():
    print("  +-----------------------------------------+")
    print("  |         AUDIO STEGANOGRAPHY             |")
    print("  +-----------------------------------------+")
    print("  |  [1] Hide Message in Audio              |")
    print("  |  [2] Extract Message from Audio         |")
    print("  |  [0] Exit                               |")
    print("  +-----------------------------------------+")
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

def hide_message_interactive():
    print("")
    print("  [*] Hide Message in Audio")
    print("  -------------------------")
    print("")
    
    audio_file = input("  Enter input audio file path (WAV): ").strip()
    if not audio_file:
        print("  [-] No file specified!")
        input("\n  Press Enter to continue...")
        return
    
    secret_msg = input("  Enter secret message: ").strip()
    if not secret_msg:
        print("  [-] No message specified!")
        input("\n  Press Enter to continue...")
        return
    
    output_file = input("  Enter output audio file path: ").strip()
    if not output_file:
        print("  [-] No output file specified!")
        input("\n  Press Enter to continue...")
        return
    
    use_pwd = input("  Use password protection? (y/n): ").strip().lower()
    password = None
    if use_pwd == 'y':
        password = getpass.getpass("  Enter password: ")
    
    print("")
    hide_message(audio_file, secret_msg, output_file, password)
    input("\n  Press Enter to continue...")

def extract_message_interactive():
    print("")
    print("  [*] Extract Message from Audio")
    print("  ------------------------------")
    print("")
    
    audio_file = input("  Enter audio file path: ").strip()
    if not audio_file:
        print("  [-] No file specified!")
        input("\n  Press Enter to continue...")
        return
    
    use_pwd = input("  Is message password protected? (y/n): ").strip().lower()
    password = None
    if use_pwd == 'y':
        password = getpass.getpass("  Enter password: ")
    
    print("")
    extract_message(audio_file, password)
    input("\n  Press Enter to continue...")

def interactive_mode():
    while True:
        clear_console()
        show_banner()
        show_menu()
        
        try:
            choice = input("  Enter your choice: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n\n  Goodbye!")
            sys.exit(0)
        
        if choice == "1":
            clear_console()
            hide_message_interactive()
        
        elif choice == "2":
            clear_console()
            extract_message_interactive()
        
        elif choice == "0":
            clear_console()
            print("")
            print("  +=========================================+")
            print("  |   Thank you for using AudioEcho!        |")
            print("  +=========================================+")
            print("")
            sys.exit(0)
        
        else:
            print("\n  [-] Invalid choice! Please try again.")
            input("  Press Enter to continue...")

def cli_mode(args):
    clear_console()
    show_banner()
    
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

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="EchoEncrypt - Audio Steganography")
    parser.add_argument('-m', help='Secret message to hide', dest='secretmsg')
    parser.add_argument('-f', help='Input audio file', dest='audiofile')
    parser.add_argument('-o', help='Output audio file', dest='outputfile')
    parser.add_argument('-p', '--password', help='Password for encryption/decryption')
    args = parser.parse_args()
    
    try:
        # If no arguments provided, run interactive mode
        if len(sys.argv) == 1:
            interactive_mode()
        else:
            cli_mode(args)
    except KeyboardInterrupt:
        print("\n\n[!] Program terminated by user.")
        sys.exit(0)