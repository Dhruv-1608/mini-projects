#!/usr/bin/env python3
import os
import argparse
import hashlib
import base64
import getpass
import sys

try:
    from PIL import Image
except ImportError:
    print("[-] PIL not installed. Run: pip install pillow")
    exit(1)

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
    print("          Image Steganography Module")
    print("   ========================================")
    print("")

def show_menu():
    print("  +-----------------------------------------+")
    print("  |         IMAGE STEGANOGRAPHY             |")
    print("  +-----------------------------------------+")
    print("  |  [1] Hide Message in Image              |")
    print("  |  [2] Extract Message from Image         |")
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

def hide_message(image_file, secret_msg, output_file, password=None):
    if password:
        secret_msg = encrypt_message(secret_msg, password)
        print("[+] Message encrypted with password")
    
    if not os.path.exists(image_file):
        print(f"[-] Error: Image file '{image_file}' not found!")
        return False
    
    try:
        img = Image.open(image_file)
        if img.mode != 'RGB':
            img = img.convert('RGB')
    except Exception as e:
        print(f"[-] Error reading image: {e}")
        return False
    
    bits = [int(bit) for char in secret_msg for bit in format(ord(char), '08b')]
    end_signal = [0] * 8
    bits += end_signal
    
    required_pixels = len(bits) // 3 + 1
    img_pixels = img.width * img.height
    
    if required_pixels > img_pixels:
        print("[-] Message too large for this image!")
        return False
    
    pixels = list(img.get_flattened_data())
    new_pixels = []
    bit_index = 0
    
    for pixel in pixels:
        if bit_index >= len(bits):
            new_pixels.append(pixel)
            continue
        
        pixel = list(pixel)
        for i in range(3):
            if bit_index < len(bits):
                pixel[i] = (pixel[i] & 254) | bits[bit_index]
                bit_index += 1
        new_pixels.append(tuple(pixel[:3]))
    
    new_img = Image.new(img.mode, img.size)
    new_img.putdata(new_pixels)
    
    try:
        new_img.save(output_file)
        print("[+] Message hidden successfully!")
        return True
    except Exception as e:
        print(f"[-] Error saving image: {e}")
        return False

def extract_message(image_file, password=None):
    if not os.path.exists(image_file):
        print(f"[-] Error: Image file '{image_file}' not found!")
        return False
    
    try:
        img = Image.open(image_file)
    except Exception as e:
        print(f"[-] Error reading image: {e}")
        return False
    
    pixels = list(img.get_flattened_data())
    bits = []
    
    for pixel in pixels:
        pixel = list(pixel)[:3]
        for channel in pixel:
            bits.append(channel & 1)
    
    chars = []
    for i in range(0, len(bits), 8):
        if i + 8 > len(bits):
            break
        byte = bits[i:i + 8]
        byte_str = ''.join(str(bit) for bit in byte)
        if byte_str == '00000000':
            break
        try:
            chars.append(chr(int(byte_str, 2)))
        except:
            break
    
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

def hide_message_interactive():
    print("")
    print("  [*] Hide Message in Image")
    print("  -------------------------")
    print("")
    
    image_file = input("  Enter input image file path (PNG): ").strip()
    if not image_file:
        print("  [-] No file specified!")
        input("\n  Press Enter to continue...")
        return
    
    secret_msg = input("  Enter secret message: ").strip()
    if not secret_msg:
        print("  [-] No message specified!")
        input("\n  Press Enter to continue...")
        return
    
    output_file = input("  Enter output image file path: ").strip()
    if not output_file:
        print("  [-] No output file specified!")
        input("\n  Press Enter to continue...")
        return
    
    use_pwd = input("  Use password protection? (y/n): ").strip().lower()
    password = None
    if use_pwd == 'y':
        password = getpass.getpass("  Enter password: ")
    
    print("")
    hide_message(image_file, secret_msg, output_file, password)
    input("\n  Press Enter to continue...")

def extract_message_interactive():
    print("")
    print("  [*] Extract Message from Image")
    print("  ------------------------------")
    print("")
    
    image_file = input("  Enter image file path: ").strip()
    if not image_file:
        print("  [-] No file specified!")
        input("\n  Press Enter to continue...")
        return
    
    use_pwd = input("  Is message password protected? (y/n): ").strip().lower()
    password = None
    if use_pwd == 'y':
        password = getpass.getpass("  Enter password: ")
    
    print("")
    extract_message(image_file, password)
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
            print("  |   Thank you for using ImageEcho!        |")
            print("  +=========================================+")
            print("")
            sys.exit(0)
        
        else:
            print("\n  [-] Invalid choice! Please try again.")
            input("  Press Enter to continue...")

def cli_mode(args):
    clear_console()
    show_banner()
    
    if args.secretmsg and args.imagefile and args.outputfile:
        hide_message(args.imagefile, args.secretmsg, args.outputfile, args.password)
    elif args.imagefile:
        password = args.password
        if not password:
            use_pwd = input("[?] Is message password protected? (y/n): ").strip().lower()
            if use_pwd == 'y':
                password = getpass.getpass("Enter password: ")
        extract_message(args.imagefile, password)
    else:
        print("Usage (Hide): python ImageEcho.py -f input.png -m 'message' -o output.png [-p password]")
        print("Usage (Extract): python ImageEcho.py -f output.png [-p password]")
        print("")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="EchoEncrypt - Image Steganography")
    parser.add_argument('-m', help='Secret message to hide', dest='secretmsg')
    parser.add_argument('-f', help='Input image file', dest='imagefile')
    parser.add_argument('-o', help='Output image file', dest='outputfile')
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