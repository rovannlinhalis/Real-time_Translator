#!/usr/bin/env python3
"""
Real-time Translator Application
A desktop application for seamless multilingual communication using OpenAI API.
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import queue
import time
import os
import json
from pathlib import Path
import speech_recognition as sr
import pyttsx3
import sounddevice as sd
import numpy as np
from openai import OpenAI
from dotenv import load_dotenv

class RealTimeTranslator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Real-time Translator")
        self.root.geometry("800x600")
        
        # Load configuration
        self.load_config()
        
        # Initialize components
        self.setup_audio()
        self.setup_openai()
        self.setup_gui()
        
        # Threading and queues
        self.audio_queue = queue.Queue()
        self.translation_queue = queue.Queue()
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
            'input_device': int(os.getenv('INPUT_DEVICE_INDEX', -1)) if os.getenv('INPUT_DEVICE_INDEX', 'default') != 'default' else None,
            'output_device': int(os.getenv('OUTPUT_DEVICE_INDEX', -1)) if os.getenv('OUTPUT_DEVICE_INDEX', 'default') != 'default' else None,
            'sample_rate': int(os.getenv('SAMPLE_RATE', 44100)),
            'chunk_size': int(os.getenv('CHUNK_SIZE', 1024))
        }
        
    def setup_audio(self):
        """Initialize audio components"""
        try:
            self.recognizer = sr.Recognizer()
            self.microphone = sr.Microphone(device_index=self.config['input_device'])
            self.tts_engine = pyttsx3.init()
            
            # Adjust for ambient noise
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                
        except Exception as e:
            messagebox.showerror("Audio Setup Error", f"Failed to initialize audio: {str(e)}")
            
    def setup_openai(self):
        """Initialize OpenAI client"""
        if self.config['openai_api_key']:
            try:
                self.openai_client = OpenAI(api_key=self.config['openai_api_key'])
            except Exception as e:
                messagebox.showerror("OpenAI Setup Error", f"Failed to initialize OpenAI: {str(e)}")
                self.openai_client = None
        else:
            self.openai_client = None
            
    def setup_gui(self):
        """Create the main GUI"""
        # Create main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configuration section
        config_frame = ttk.LabelFrame(main_frame, text="Configuration", padding="10")
        config_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # API Key configuration
        ttk.Label(config_frame, text="OpenAI API Key:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.api_key_var = tk.StringVar(value=self.config['openai_api_key'])
        self.api_key_entry = ttk.Entry(config_frame, textvariable=self.api_key_var, show="*", width=50)
        self.api_key_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 5))
        ttk.Button(config_frame, text="Save", command=self.save_api_key).grid(row=0, column=2)
        
        # Language configuration
        ttk.Label(config_frame, text="Source Language:").grid(row=1, column=0, sticky=tk.W, padx=(0, 5), pady=(5, 0))
        self.source_lang_var = tk.StringVar(value=self.config['source_language'])
        source_lang_combo = ttk.Combobox(config_frame, textvariable=self.source_lang_var, 
                                       values=['en', 'es', 'fr', 'de', 'it', 'pt', 'ru', 'ja', 'ko', 'zh'])
        source_lang_combo.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(0, 5), pady=(5, 0))
        
        ttk.Label(config_frame, text="Target Language:").grid(row=2, column=0, sticky=tk.W, padx=(0, 5), pady=(5, 0))
        self.target_lang_var = tk.StringVar(value=self.config['target_language'])
        target_lang_combo = ttk.Combobox(config_frame, textvariable=self.target_lang_var,
                                       values=['en', 'es', 'fr', 'de', 'it', 'pt', 'ru', 'ja', 'ko', 'zh'])
        target_lang_combo.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=(0, 5), pady=(5, 0))
        
        # Device configuration
        device_frame = ttk.LabelFrame(main_frame, text="Audio Devices", padding="10")
        device_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Button(device_frame, text="List Audio Devices", command=self.list_audio_devices).grid(row=0, column=0, pady=(0, 5))
        ttk.Button(device_frame, text="Test Microphone", command=self.test_microphone).grid(row=0, column=1, padx=(10, 0), pady=(0, 5))
        
        # Control buttons
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=2, column=0, columnspan=2, pady=(0, 10))
        
        self.start_button = ttk.Button(control_frame, text="Start Listening", command=self.start_listening)
        self.start_button.grid(row=0, column=0, padx=(0, 10))
        
        self.stop_button = ttk.Button(control_frame, text="Stop Listening", command=self.stop_listening_func, state="disabled")
        self.stop_button.grid(row=0, column=1)
        
        # Status display
        status_frame = ttk.LabelFrame(main_frame, text="Status", padding="10")
        status_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.status_label = ttk.Label(status_frame, text="Ready to start translation")
        self.status_label.grid(row=0, column=0, sticky=tk.W)
        
        # Translation display
        translation_frame = ttk.LabelFrame(main_frame, text="Translation Log", padding="10")
        translation_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.translation_text = scrolledtext.ScrolledText(translation_frame, height=15, width=80)
        self.translation_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(4, weight=1)
        config_frame.columnconfigure(1, weight=1)
        translation_frame.columnconfigure(0, weight=1)
        translation_frame.rowconfigure(0, weight=1)
        
    def save_api_key(self):
        """Save API key to configuration"""
        api_key = self.api_key_var.get().strip()
        if api_key:
            self.config['openai_api_key'] = api_key
            self.setup_openai()
            
            # Save to config file
            config_path = Path(__file__).parent / "config.env"
            config_content = f"""# OpenAI API Configuration
OPENAI_API_KEY={api_key}

# Translation Settings
SOURCE_LANGUAGE={self.source_lang_var.get()}
TARGET_LANGUAGE={self.target_lang_var.get()}
TRANSLATION_MODEL=gpt-3.5-turbo

# Audio Settings
INPUT_DEVICE_INDEX=default
OUTPUT_DEVICE_INDEX=default
SAMPLE_RATE=44100
CHUNK_SIZE=1024
"""
            with open(config_path, 'w') as f:
                f.write(config_content)
                
            messagebox.showinfo("Success", "API key saved successfully!")
        else:
            messagebox.showwarning("Warning", "Please enter a valid API key")
            
    def list_audio_devices(self):
        """List available audio devices"""
        try:
            devices = sd.query_devices()
            device_info = "Available Audio Devices:\n\n"
            for i, device in enumerate(devices):
                device_info += f"Device {i}: {device['name']} - "
                device_info += f"Inputs: {device['max_input_channels']}, "
                device_info += f"Outputs: {device['max_output_channels']}\n"
            
            messagebox.showinfo("Audio Devices", device_info)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to list audio devices: {str(e)}")
            
    def test_microphone(self):
        """Test microphone functionality"""
        try:
            with self.microphone as source:
                self.status_label.config(text="Testing microphone... Speak something!")
                audio = self.recognizer.listen(source, timeout=3, phrase_time_limit=5)
                
            text = self.recognizer.recognize_google(audio)
            messagebox.showinfo("Microphone Test", f"Microphone working! Heard: '{text}'")
            self.status_label.config(text="Microphone test completed")
        except sr.WaitTimeoutError:
            messagebox.showwarning("Timeout", "No speech detected within 3 seconds")
            self.status_label.config(text="Microphone test timeout")
        except sr.UnknownValueError:
            messagebox.showwarning("Recognition Error", "Could not understand audio")
            self.status_label.config(text="Speech recognition failed")
        except Exception as e:
            messagebox.showerror("Error", f"Microphone test failed: {str(e)}")
            self.status_label.config(text="Microphone test failed")
            
    def start_listening(self):
        """Start the real-time translation process"""
        if not self.openai_client:
            messagebox.showerror("Error", "Please configure OpenAI API key first")
            return
            
        self.is_listening = True
        self.stop_listening.clear()
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")
        self.status_label.config(text="Listening for speech...")
        
        # Start listening thread
        threading.Thread(target=self.listen_continuously, daemon=True).start()
        
    def stop_listening_func(self):
        """Stop the real-time translation process"""
        self.is_listening = False
        self.stop_listening.set()
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")
        self.status_label.config(text="Stopped listening")
        
    def listen_continuously(self):
        """Continuously listen for audio and process translations"""
        while self.is_listening and not self.stop_listening.is_set():
            try:
                with self.microphone as source:
                    # Listen for audio with a shorter timeout
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=5)
                    
                # Process audio in a separate thread
                threading.Thread(target=self.process_audio, args=(audio,), daemon=True).start()
                
            except sr.WaitTimeoutError:
                # Normal timeout, continue listening
                continue
            except Exception as e:
                self.root.after(0, lambda: self.status_label.config(text=f"Error: {str(e)}"))
                break
                
    def process_audio(self, audio):
        """Process audio data and perform translation"""
        try:
            # Convert speech to text
            text = self.recognizer.recognize_google(audio, language=self.source_lang_var.get())
            
            if text.strip():
                # Update status
                self.root.after(0, lambda: self.status_label.config(text=f"Translating: {text}"))
                
                # Translate text
                translated_text = self.translate_text(text)
                
                # Display results
                timestamp = time.strftime("%H:%M:%S")
                result = f"[{timestamp}] Original ({self.source_lang_var.get()}): {text}\n"
                result += f"[{timestamp}] Translation ({self.target_lang_var.get()}): {translated_text}\n\n"
                
                self.root.after(0, lambda: self.translation_text.insert(tk.END, result))
                self.root.after(0, lambda: self.translation_text.see(tk.END))
                
                # Speak translation
                self.speak_text(translated_text)
                
                # Update status
                self.root.after(0, lambda: self.status_label.config(text="Listening for speech..."))
                
        except sr.UnknownValueError:
            # Could not understand audio, continue listening
            pass
        except Exception as e:
            self.root.after(0, lambda: self.status_label.config(text=f"Processing error: {str(e)}"))
            
    def translate_text(self, text):
        """Translate text using OpenAI API"""
        try:
            language_names = {
                'en': 'English', 'es': 'Spanish', 'fr': 'French', 'de': 'German',
                'it': 'Italian', 'pt': 'Portuguese', 'ru': 'Russian', 'ja': 'Japanese',
                'ko': 'Korean', 'zh': 'Chinese'
            }
            
            source_lang = language_names.get(self.source_lang_var.get(), self.source_lang_var.get())
            target_lang = language_names.get(self.target_lang_var.get(), self.target_lang_var.get())
            
            prompt = f"Translate the following {source_lang} text to {target_lang}. Only provide the translation, no explanations:\n\n{text}"
            
            response = self.openai_client.chat.completions.create(
                model=self.config['translation_model'],
                messages=[{"role": "user", "content": prompt}],
                max_tokens=150,
                temperature=0.3
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            return f"Translation error: {str(e)}"
            
    def speak_text(self, text):
        """Convert text to speech"""
        try:
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
        except Exception as e:
            print(f"TTS error: {str(e)}")
            
    def run(self):
        """Start the application"""
        self.root.mainloop()

def main():
    """Entry point for the application"""
    app = RealTimeTranslator()
    app.run()

if __name__ == "__main__":
    main()