# Morse Code Audio Decoder

## Overview
An audio-based Morse code decoder that uses digital signal processing techniques to extract and decode signals from .wav files.

## Technologies Used
- Python (Scipy, Numpy)
- Bandpass Filtering (Butterworth Filter)
- Short-Time Fourier Transform (STFT)
- Spectrogram Visualization
- Morse Dictionary Mapping

## Workflow
1. Read Morse audio file (.wav)
2. Apply bandpass filter to isolate signal
3. Normalize and threshold the signal
4. Convert audio to binary sequence
5. Decode Morse characters and output text

## Performance
- High decoding accuracy
- Fast and memory-efficient
- Robust to noise and amplitude variation
- Real-time spectrogram and signal visualization

## Applications
- Military communication
- Ham radio decoding
- Puzzles and encrypted messages
- Assistive tech for audio-based input
