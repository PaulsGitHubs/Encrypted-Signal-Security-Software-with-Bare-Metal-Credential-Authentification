import numpy as np
import wavio
# Generate a random serial number
serial_number = np.random.randint(0, 99999999)

# Generate RF signal based on serial number
fs = 44100  # Sampling rate
T = 1.0    # Seconds
t = np.linspace(0, T, int(fs * T), endpoint=False)  # Time array
x = 0.5 * np.sin(2 * np.pi * serial_number * t)  # Signal

# Save as WAV file
wavio.write("signal.wav", x, fs, sampwidth=2)
