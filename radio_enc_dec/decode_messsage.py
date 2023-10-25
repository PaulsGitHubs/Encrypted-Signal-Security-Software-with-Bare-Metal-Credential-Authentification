import csv
import numpy as np
from scipy.io import wavfile
from numpy.fft import fft

def decode_audio(filename, sample_rate=44100, duration=0.01):
    rate, data = wavfile.read(filename)
    segment_length = int(sample_rate * duration)

    freq_to_symbol = {}
    with open('musical_keys.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header
        for row in reader:
            symbol, freq = row
            freq_to_symbol[float(freq)] = symbol

    decoded_symbols = []
    for i in range(0, len(data), segment_length):
        segment = data[i:i+segment_length]
        dominant_freq = get_dominant_freq(segment, sample_rate)
        closest_freq = min(freq_to_symbol.keys(), key=lambda x: abs(x - dominant_freq))
        decoded_symbols.append(freq_to_symbol[closest_freq])

    return ''.join(decoded_symbols)

def get_dominant_freq(segment, sample_rate):
    freq_spectrum = np.abs(fft(segment))
    frequencies = np.fft.fftfreq(len(segment), d=1/sample_rate)
    peak_index = np.argmax(freq_spectrum)
    dominant_freq = abs(frequencies[peak_index])
    return dominant_freq

decoded_message = decode_audio('message_audio.wav')
print(f"Decoded Message: {decoded_message}")
