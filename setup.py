from setuptools import setup, find_packages

setup(
    name="real-time-translator",
    version="1.0.0",
    description="Real-time desktop translator for seamless multilingual communication",
    author="Real-time Translator Team",
    packages=find_packages(),
    install_requires=[
        "openai>=1.0.0",
        "pyaudio>=0.2.11",
        "speechrecognition>=3.10.0",
        "python-dotenv>=1.0.0",
        "numpy>=1.24.0",
        "sounddevice>=0.4.6",
    ],
    extras_require={
        'gui': ['pyttsx3>=2.90'],  # TTS for GUI version
        'all': ['pyttsx3>=2.90'],
    },
    entry_points={
        "console_scripts": [
            "real-time-translator=translator_cli:main",
            "real-time-translator-gui=translator_app:main",
        ],
    },
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)