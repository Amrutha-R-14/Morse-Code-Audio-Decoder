import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy import signal
# Read the audio file
rate, audio = wavfile.read(r"dataset path")

# Bandpass filter parameters
lowcut =100  # Set the lower cutoff frequency
highcut = 3500  # Set the higher cutoff frequency

# Calculate the cutoff frequency using the geometric mean
cutoff_frequency = np.sqrt(lowcut * highcut) # Set the cutoff frequency
filter_order = 2  # Set the filter order

# Sampling period
T = 1.0 / rate

# Calculate filter coefficients using bilinear transformation
wc = 2 * np.pi * cutoff_frequency
alpha = np.tan(wc * T / 2)
beta = np.cos(wc * T)

# Difference equation coefficients
b0 = 1
b1 = -1
a0 = 1 + alpha
a1 = -2 * beta
a2 = 1 - alpha

# Apply bandpass filter using the difference equation
filtered_audio = np.zeros_like(audio)
for i in range(len(audio)):
    x_n = audio[i]
    y_n = (b0 / a0) * x_n + (b1 / a0) * audio[i-1] - (a1 / a0) * filtered_audio[i-1] - (a2 / a0) * filtered_audio[i-2]
    filtered_audio[i] = y_n

# Normalizes the amplitude of the filtered signal to be between -1 and 1
normalized_filtered_audio = filtered_audio / np.max(np.abs(filtered_audio))

# Plots the original and filtered signals
plt.figure(figsize=(12, 6))


T_original = np.linspace(0, len(audio) / rate, num=len(audio))
plt.title('Original Signal Wave')
plt.plot(T_original, audio)
plt.show()

T_filtered = np.linspace(0, len(normalized_filtered_audio) / rate, num=len(normalized_filtered_audio))
plt.title('Filtered Signal Wave')
plt.plot(T_filtered, normalized_filtered_audio)

plt.show()
plt.figure(figsize=(12, 6))
plt.specgram(filtered_audio, Fs=rate, NFFT=256, noverlap=128, cmap='viridis')
plt.title('Spectrogram of Filtered Audio')
plt.xlabel('Time (s)')
plt.ylabel('Frequency (Hz)')
plt.colorbar(label='Intensity (dB)')
plt.show()

# Generates and plots the spectrogram for the original audio
plt.figure(figsize=(12, 6))
plt.subplot(1, 3, 1)
plt.specgram(audio, Fs=rate, NFFT=256, noverlap=128, cmap='viridis')
plt.title('Spectrogram of Original Audio')
plt.xlabel('Time (s)')
plt.ylabel('Frequency (Hz)')
plt.colorbar(label='Intensity (dB)')
plt.show()

# Applys minimum and maximum volume filters
min_volume = -60
max_volume = -30
freqs, times, Sxx = signal.spectrogram(audio, rate, nfft=256)
Sxx_filtered = np.clip(1* np.log10(Sxx), min_volume, max_volume)  

# Adjust the volume threshold based on the filtered audio
volume_threshold = -45

normalized_audio = (Sxx_filtered > volume_threshold).astype(int)
normalized_audio = np.append(normalized_audio, 0)

one_count = 0
zero_count = 0
output = ''

for value in normalized_audio:
    if value == 1:
        if zero_count > 2:
            output += '/'

        zero_count = 0
        one_count += 1
    if value == 0:
        if one_count <= 4 and one_count > 0:
            output += '.'
            one_count = 0
        elif one_count > 4:
            output += '-'
            one_count = 0

        zero_count += 1


# Morse Code Dictionary for decryption
MORSE_CODE_DICT = {'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.', 'H': '....',
                   'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---', 'P': '.--.',
                   'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
                   'Y': '-.--', 'Z': '--..'}

def decrypt(message):
    splitted_message = message.split('/')
    decrypted_message = ''

    for word in splitted_message:
        morse_codes = word.split(' ')
        for morse_code in morse_codes:
            letter = dict(zip(MORSE_CODE_DICT.values(), MORSE_CODE_DICT.keys())).get(morse_code)
            decrypted_message += letter if letter else ' '
        decrypted_message += ' '

    return decrypted_message.strip()

decoded_message = decrypt(output)

print("Decoded Morse Code:", output)
print("Decrypted Message:", decoded_message)
