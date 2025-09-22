#!/usr/bin/env python3
"""
Real-time Translator CLI Application
A command-line version for headless environments.
"""

import os
import time
import threading
import queue
from pathlib import Path
import speech_recognition as sr
from openai import OpenAI
from dotenv import load_dotenv

class RealTimeTranslatorCLI:
    def __init__(self):
        self.load_config()
        self.setup_audio()
        self.setup_openai()
        
        self.is_listening = False
        self.stop_listening = threading.Event()
        
    def load_config(self):
        """Load configuration from environment file"""
        config_path = Path(__file__).parent / "config.env"
        if config_path.exists():
            load_dotenv(config_path)
        
        self.config = {
            'openai_api_key': os.getenv('OPENAI_API_KEY', ''),
            'source_language': os.getenv('SOURCE_LANGUAGE', 'en'),
            'target_language': os.getenv('TARGET_LANGUAGE', 'es'),
            'translation_model': os.getenv('TRANSLATION_MODEL', 'gpt-3.5-turbo'),
        }
        
    def setup_audio(self):
        """Initialize audio components"""
        try:
            self.recognizer = sr.Recognizer()
            self.microphone = sr.Microphone()
            
            # Adjust for ambient noise
            print("Adjusting for ambient noise, please wait...")
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=2)
            print("Setup complete!")
                
        except Exception as e:
            print(f"Audio setup error: {e}")
            
    def setup_openai(self):
        """Initialize OpenAI client"""
        if self.config['openai_api_key']:
            try:
                self.openai_client = OpenAI(api_key=self.config['openai_api_key'])
                print("OpenAI client initialized successfully!")
            except Exception as e:
                print(f"OpenAI setup error: {e}")
                self.openai_client = None
        else:
            print("No OpenAI API key found. Please configure in config.env")
            self.openai_client = None
            
    def translate_text(self, text):
        """Translate text using OpenAI API"""
        if not self.openai_client:
            return "Translation unavailable - No API key"
            
        try:
            language_names = {
                'en': 'English', 'es': 'Spanish', 'fr': 'French', 'de': 'German',
                'it': 'Italian', 'pt': 'Portuguese', 'ru': 'Russian', 'ja': 'Japanese',
                'ko': 'Korean', 'zh': 'Chinese'
            }
            
            source_lang = language_names.get(self.config['source_language'], self.config['source_language'])
            target_lang = language_names.get(self.config['target_language'], self.config['target_language'])
            
            prompt = f"Translate the following {source_lang} text to {target_lang}. Only provide the translation:\n\n{text}"
            
            response = self.openai_client.chat.completions.create(
                model=self.config['translation_model'],
                messages=[{"role": "user", "content": prompt}],
                max_tokens=150,
                temperature=0.3
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            return f"Translation error: {str(e)}"
            
    def listen_once(self):
        """Listen for a single phrase and translate it"""
        try:
            print(f"Listening for {self.config['source_language']} speech... (speak now)")
            
            with self.microphone as source:
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                
            print("Processing speech...")
            text = self.recognizer.recognize_google(audio, language=self.config['source_language'])
            
            if text.strip():
                print(f"\nOriginal ({self.config['source_language']}): {text}")
                
                translated_text = self.translate_text(text)
                print(f"Translation ({self.config['target_language']}): {translated_text}")
                print("-" * 50)
                return True
            else:
                print("No speech detected.")
                return False
                
        except sr.WaitTimeoutError:
            print("No speech detected within 5 seconds.")
            return False
        except sr.UnknownValueError:
            print("Could not understand the speech.")
            return False
        except Exception as e:
            print(f"Error: {e}")
            return False
            
    def run_interactive(self):
        """Run interactive translation session"""
        print("\n" + "="*60)
        print("REAL-TIME TRANSLATOR CLI")
        print("="*60)
        print(f"Source Language: {self.config['source_language']}")
        print(f"Target Language: {self.config['target_language']}")
        print(f"OpenAI API: {'✓ Configured' if self.openai_client else '✗ Not configured'}")
        print("\nCommands:")
        print("- Press ENTER to translate speech")
        print("- Type 'config' to change languages")
        print("- Type 'quit' to exit")
        print("-" * 60)
        
        while True:
            try:
                command = input("\n> ").strip().lower()
                
                if command == 'quit':
                    break
                elif command == 'config':
                    self.configure_languages()
                elif command == '' or command == 'translate':
                    if not self.openai_client:
                        print("Please configure OpenAI API key first!")
                        continue
                    self.listen_once()
                else:
                    print("Unknown command. Press ENTER to translate, 'config' to configure, or 'quit' to exit.")
                    
            except KeyboardInterrupt:
                print("\nExiting...")
                break
                
    def configure_languages(self):
        """Configure source and target languages"""
        languages = {
            'en': 'English', 'es': 'Spanish', 'fr': 'French', 'de': 'German',
            'it': 'Italian', 'pt': 'Portuguese', 'ru': 'Russian', 'ja': 'Japanese',
            'ko': 'Korean', 'zh': 'Chinese'
        }
        
        print("\nAvailable languages:")
        for code, name in languages.items():
            print(f"  {code}: {name}")
            
        source = input(f"\nEnter source language code (current: {self.config['source_language']}): ").strip()
        if source and source in languages:
            self.config['source_language'] = source
            
        target = input(f"Enter target language code (current: {self.config['target_language']}): ").strip()
        if target and target in languages:
            self.config['target_language'] = target
            
        print(f"\nLanguages updated: {self.config['source_language']} → {self.config['target_language']}")

def main():
    """Entry point for CLI application"""
    # Check if config exists
    config_path = Path(__file__).parent / "config.env"
    if not config_path.exists():
        print("Config file not found. Creating from template...")
        template_path = Path(__file__).parent / "config.env.example"
        if template_path.exists():
            with open(template_path, 'r') as src, open(config_path, 'w') as dst:
                dst.write(src.read())
        print(f"Please edit {config_path} and add your OpenAI API key.")
        return
    
    app = RealTimeTranslatorCLI()
    app.run_interactive()

if __name__ == "__main__":
    main()