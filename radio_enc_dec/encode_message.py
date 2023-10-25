import csv
import numpy as np
from scipy.io import wavfile

# Constants and setup
symbols = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890 !"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
LOW_FREQ = 100
HIGH_FREQ = 20000
FREQ_SPACING = 200
musical_notes = list(np.arange(LOW_FREQ, HIGH_FREQ, FREQ_SPACING)[:len(symbols)])
true_keys = {k: f for k, f in zip(symbols, musical_notes)}

def fibonacci(n):
    fib_sequence = [0, 1]
    while len(fib_sequence) < n:
        fib_sequence.append(fib_sequence[-1] + fib_sequence[-2])
    return fib_sequence

# Writing the CSV file
with open('musical_keys.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Symbol", "Frequency"])
    for key, value in true_keys.items():
        writer.writerow([key, value])

def generate_audio_file(sentence, sample_rate=44100, duration=0.01, noise_amplitude=0.1):
    total_signal = np.array([], dtype=np.float32)
    fib_sequence = fibonacci(len(sentence))
    max_fib = max(fib_sequence)
    scaled_fib_sequence = [0.5 + (x/max_fib) * 0.5 for x in fib_sequence]

    for idx, char in enumerate(sentence):
        t = np.linspace(0, duration, int(sample_rate * duration))
        freq = true_keys.get(char, musical_notes[0])
        amplitude = scaled_fib_sequence[idx % len(scaled_fib_sequence)]
        noise = np.random.normal(0, noise_amplitude, len(t))
        signal = amplitude * np.sin(2 * np.pi * freq * t) + noise
        total_signal = np.concatenate((total_signal, signal))

    total_signal = np.int16((total_signal / np.max(np.abs(total_signal))) * 32767)
    wavfile.write("message_audio.wav", int(sample_rate), total_signal)

message = "This is a test sentence for HackRF."
generate_audio_file(message)
