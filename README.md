# Real-time Translator

Real-time desktop translator for seamless multilingual communication using OpenAI's API and speech recognition technology.

## Features

- **Real-time Speech Translation**: Capture audio from your microphone and translate it in real-time
- **Multiple Languages**: Support for 10+ languages including English, Spanish, French, German, Italian, Portuguese, Russian, Japanese, Korean, and Chinese
- **OpenAI Integration**: Uses OpenAI's powerful language models for accurate translations
- **Audio Input/Output**: Configurable microphone input and speaker output
- **User-friendly GUI**: Easy-to-use desktop interface with device configuration
- **Cross-platform**: Works on Windows, macOS, and Linux

## Quick Start

### Try the Demo First

Before setting up the full application, try the demo to see how it works:

```bash
git clone https://github.com/rovannlinhalis/Real-time_Translator.git
cd Real-time_Translator
python3 demo.py
```

This will show mock translations and help you set up the configuration file.

### Option 1: Download Pre-built Binary (Recommended for End Users)

1. **Download the application binary** from the [Releases](../../releases) page
2. **Configure OpenAI API Key**:
   - Copy `config.env.example` to `config.env`
   - Edit `config.env` and add your OpenAI API key:
     ```
     OPENAI_API_KEY=your_actual_api_key_here
     ```
3. **Configure Input/Output Devices**:
   - Run the application
   - Click "List Audio Devices" to see available devices
   - Click "Test Microphone" to verify your microphone is working
4. **Enable and Enjoy**:
   - Select source and target languages
   - Click "Start Listening"
   - Speak into your microphone and see real-time translations!

### Option 2: Run from Source (Recommended for Developers)

#### Easy Installation

```bash
git clone https://github.com/rovannlinhalis/Real-time_Translator.git
cd Real-time_Translator

# Linux/macOS
./install.sh

# Windows
install.bat
```

#### Manual Installation

1. **Prerequisites**:
   - Python 3.8 or higher
   - OpenAI API key (get one at [OpenAI Platform](https://platform.openai.com/))

2. **System Dependencies** (install first):
   ```bash
   # Ubuntu/Debian
   sudo apt-get update
   sudo apt-get install python3-tk portaudio19-dev

   # macOS
   brew install portaudio tk

   # Windows: No additional system packages needed
   ```

3. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure API key**:
   ```bash
   cp config.env.example config.env
   # Edit config.env and add your OpenAI API key
   ```

5. **Run the application**:
   ```bash
   # GUI version (recommended)
   python translator_app.py

   # CLI version (for headless systems)
   python translator_cli.py

   # Demo version (no dependencies needed)
   python demo.py
   ```

## Building from Source

### Build Executable

To create a standalone executable:

#### On Linux/macOS:
```bash
./build.sh
```

#### On Windows:
```cmd
build.bat
```

The executable will be created in the `dist/` directory.

## Configuration

### Environment Variables

Create a `config.env` file based on `config.env.example`:

```env
# OpenAI API Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Translation Settings
SOURCE_LANGUAGE=en
TARGET_LANGUAGE=es
TRANSLATION_MODEL=gpt-3.5-turbo

# Audio Settings
INPUT_DEVICE_INDEX=default
OUTPUT_DEVICE_INDEX=default
SAMPLE_RATE=44100
CHUNK_SIZE=1024
```

### Supported Languages

- `en` - English
- `es` - Spanish
- `fr` - French
- `de` - German
- `it` - Italian
- `pt` - Portuguese
- `ru` - Russian
- `ja` - Japanese
- `ko` - Korean
- `zh` - Chinese

## Application Versions

This project includes three versions to suit different needs:

### 1. GUI Version (`translator_app.py`)
- **Best for**: Desktop users who want a visual interface
- **Features**: Full GUI with device selection, real-time translation display, audio controls
- **Requirements**: tkinter, full audio dependencies
- **Usage**: `python translator_app.py`

### 2. CLI Version (`translator_cli.py`)
- **Best for**: Headless systems, servers, or users who prefer command-line interfaces
- **Features**: Interactive command-line interface, speech recognition, text-based output
- **Requirements**: Basic audio dependencies (no GUI libraries needed)
- **Usage**: `python translator_cli.py`

### 3. Demo Version (`demo.py`)
- **Best for**: Testing setup, demonstrations, or environments with limited dependencies
- **Features**: Shows translation workflow with mock data, configuration setup
- **Requirements**: Only Python standard library and dotenv
- **Usage**: `python demo.py`

## Usage Instructions

1. **Start the Application**
   - Run the executable or `python translator_app.py`

2. **Configure API Key**
   - Enter your OpenAI API key in the configuration section
   - Click "Save" to store the key

3. **Set Languages**
   - Select your source language (language you'll speak)
   - Select your target language (language for translation)

4. **Test Audio Devices**
   - Click "List Audio Devices" to see available microphones and speakers
   - Click "Test Microphone" to verify your microphone is working

5. **Start Translation**
   - Click "Start Listening"
   - Speak into your microphone
   - See real-time translations in the log area
   - Hear the translated text spoken aloud

6. **Stop Translation**
   - Click "Stop Listening" to end the session

## System Requirements

- **Operating System**: Windows 10+, macOS 10.14+, or Linux
- **Python**: 3.8+ (if running from source)
- **Memory**: 4GB RAM minimum, 8GB recommended
- **Audio**: Microphone and speakers/headphones
- **Internet**: Required for OpenAI API calls

## Troubleshooting

### Common Issues

1. **"No module named 'pyaudio'" error**:
   ```bash
   # On Ubuntu/Debian:
   sudo apt-get install portaudio19-dev
   pip install pyaudio
   
   # On macOS:
   brew install portaudio
   pip install pyaudio
   
   # On Windows:
   pip install pyaudio
   ```

2. **Microphone not working**:
   - Check microphone permissions in your OS settings
   - Try different microphone devices using "List Audio Devices"
   - Ensure microphone is not muted

3. **OpenAI API errors**:
   - Verify your API key is correct
   - Check your OpenAI account has sufficient credits
   - Ensure internet connection is stable

4. **Translation quality issues**:
   - Speak clearly and at a moderate pace
   - Reduce background noise
   - Try different source languages if detection is poor

## Development

### Project Structure

```
Real-time_Translator/
├── translator_app.py      # GUI application (main)
├── translator_cli.py      # CLI application 
├── demo.py               # Demo version (minimal dependencies)
├── requirements.txt      # Python dependencies
├── setup.py             # Package setup configuration
├── config.env.example   # Configuration template
├── install.sh           # Installation script (Linux/macOS)
├── install.bat          # Installation script (Windows)
├── build.sh             # Build script (Linux/macOS)
├── build.bat            # Build script (Windows)
├── LICENSE              # MIT License
├── .gitignore           # Git ignore rules
└── README.md            # This file
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For issues and questions:
- Create an issue on GitHub
- Check the troubleshooting section above
- Ensure you have the latest version

## Acknowledgments

- OpenAI for providing the translation API
- Google for speech recognition services
- Python community for excellent audio processing libraries
