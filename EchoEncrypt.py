#!/usr/bin/env python3

import os
import sys
import subprocess

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
    print("                        v2.1")
    print("    =================================================")
    print("          Audio & Image Steganography Tool")
    print("    =================================================")
    print("")

def show_menu():
    print("  +-----------------------------------------+")
    print("  |           MAIN MENU                     |")
    print("  +-----------------------------------------+")
    print("  |  [1] Audio Steganography                |")
    print("  |  [2] Image Steganography                |")
    print("  |  [3] About                              |")
    print("  |  [0] Exit                               |")
    print("  +-----------------------------------------+")
    print("")

def get_script_path(filename):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_dir, "modules", filename)

def run_module(module_name):
    script_path = get_script_path(module_name)
    
    if not os.path.exists(script_path):
        print(f"\n[-] Error: Module '{module_name}' not found!")
        print(f"    Expected path: {script_path}")
        input("\nPress Enter to return to main menu...")
        return False
    
    try:
        subprocess.run([sys.executable, script_path])
        return True
    except KeyboardInterrupt:
        print("\n\n[!] Module interrupted by user.")
        return True
    except Exception as e:
        print(f"\n[-] Error running module: {e}")
        input("\nPress Enter to return to main menu...")
        return False

def show_about():
    clear_console()
    print("")
    print("  +===========================================================+")
    print("  |                    ABOUT ECHOENCRYPT                      |")
    print("  +===========================================================+")
    print("  |                                                           |")
    print("  |  EchoEncrypt is a steganography tool that allows you     |")
    print("  |  to hide secret messages inside audio and image files.   |")
    print("  |                                                           |")
    print("  |  FEATURES:                                                |")
    print("  |  - Hide messages in WAV audio files (LSB encoding)       |")
    print("  |  - Hide messages in PNG images (LSB encoding)            |")
    print("  |  - Password protection with XOR encryption               |")
    print("  |  - Extract hidden messages from files                    |")
    print("  |                                                           |")
    print("  |  MODULES:                                                 |")
    print("  |  - AudioEcho.py - Audio steganography                    |")
    print("  |  - ImageEcho.py - Image steganography                    |")
    print("  |                                                           |")
    print("  |  LICENSE: MIT                                             |")
    print("  |  VERSION: 2.1                                             |")
    print("  |                                                           |")
    print("  +===========================================================+")
    print("")
    input("  Press Enter to return to main menu...")

def main():
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
            print("\n  [*] Loading Audio Steganography...\n")
            run_module("AudioEcho.py")
        
        elif choice == "2":
            clear_console()
            print("\n  [*] Loading Image Steganography...\n")
            run_module("ImageEcho.py")
        
        elif choice == "3":
            show_about()
        
        elif choice == "0":
            clear_console()
            print("")
            print("  +===========================================================+")
            print("  |                                                           |")
            print("  |           Thank you for using EchoEncrypt!                |")
            print("  |                    Goodbye!                               |")
            print("  |                                                           |")
            print("  +===========================================================+")
            print("")
            sys.exit(0)
        
        else:
            print("\n  [-] Invalid choice! Please try again.")
            input("  Press Enter to continue...")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[!] Program terminated by user.")
        sys.exit(0)