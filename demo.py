#!/usr/bin/env python3
"""
Demo script to show Real-time Translator functionality
This version simulates the translation process for demonstration purposes.
"""

import os
import time
from pathlib import Path

def demo_translation():
    """Demonstrate translation functionality"""
    print("\n" + "="*60)
    print("REAL-TIME TRANSLATOR DEMO")
    print("="*60)
    
    # Check for config file
    config_path = Path(__file__).parent / "config.env"
    example_path = Path(__file__).parent / "config.env.example"
    
    if not config_path.exists():
        print("Setting up configuration...")
        if example_path.exists():
            # Copy example to config
            with open(example_path, 'r') as src:
                content = src.read()
            with open(config_path, 'w') as dst:
                dst.write(content)
            print(f"✓ Created config.env from template")
        else:
            print("✗ No configuration template found")
            return
    
    # Read config
    config = {}
    try:
        with open(config_path, 'r') as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    config[key] = value
    except Exception as e:
        print(f"Error reading config: {e}")
        return
    
    # Check API key
    api_key = config.get('OPENAI_API_KEY', '')
    if not api_key or api_key == 'your_openai_api_key_here':
        print("\n⚠️  OpenAI API Key not configured!")
        print("To use real translation:")
        print("1. Get an API key from https://platform.openai.com/")
        print("2. Edit config.env and replace 'your_openai_api_key_here' with your key")
        print("3. Run the full application with: python translator_cli.py")
        print("\nFor now, showing demo with mock translations...")
        use_real_api = False
    else:
        print("✓ OpenAI API key configured")
        use_real_api = True
    
    # Demo translations
    demo_phrases = [
        ("Hello, how are you today?", "Hola, ¿cómo estás hoy?"),
        ("I would like to order some food", "Me gustaría pedir algo de comida"),
        ("Where is the nearest hospital?", "¿Dónde está el hospital más cercano?"),
        ("Thank you very much", "Muchas gracias"),
        ("What time is it?", "¿Qué hora es?")
    ]
    
    source_lang = config.get('SOURCE_LANGUAGE', 'en')
    target_lang = config.get('TARGET_LANGUAGE', 'es')
    
    print(f"\nTranslation: {source_lang} → {target_lang}")
    print("Demonstrating translation functionality...\n")
    
    for i, (original, translation) in enumerate(demo_phrases, 1):
        print(f"Example {i}:")
        print(f"  Original ({source_lang}): {original}")
        
        if use_real_api:
            print("  [Using OpenAI API for real translation...]")
            # Here we would use the actual API
            print(f"  Translation ({target_lang}): [Real API translation would appear here]")
        else:
            print("  [Demo translation]")
            print(f"  Translation ({target_lang}): {translation}")
        
        print()
        time.sleep(1)
    
    print("Demo completed!")
    print("\nNext steps:")
    print("1. Install dependencies: pip install -r requirements.txt")
    print("2. Configure your OpenAI API key in config.env")
    print("3. Run the CLI version: python translator_cli.py")
    print("4. Or run the GUI version: python translator_app.py (requires tkinter)")

def main():
    """Main demo function"""
    demo_translation()

if __name__ == "__main__":
    main()