import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import simps
import sounddevice as sd

def generate_mechanical_sound(frequencies, magnitudes, phases, duration, sampling_rate):
    time = np.arange(0, duration, 1/sampling_rate)
    
    mechanical_sound = np.zeros_like(time)

    for freq, mag, phase in zip(frequencies, magnitudes, phases):
        harmonic = mag * (np.cos(2 * np.pi * freq * time + phase) + np.sin(2 * np.pi * freq * time + phase))
        mechanical_sound += harmonic

    return time, mechanical_sound

def calculate_fourier_coefficients(signal, resolution, sampling_rate):
    num_samples = len(signal)
    time_interval = 1 / sampling_rate

    frequencies = np.fft.fftfreq(num_samples, time_interval)
    magnitudes = np.zeros_like(frequencies)
    phases = np.zeros_like(frequencies)

    for i, freq in enumerate(frequencies):
        if freq >= 0:
            integrand = signal * np.exp(-2j * np.pi * freq * np.arange(num_samples) * time_interval)
            magnitudes[i] = np.abs(simps(integrand, dx=time_interval))
            phases[i] = np.angle(simps(integrand, dx=time_interval))

    return frequencies, magnitudes, phases

# Set parameters
frequency_resolution = 1000  # Frequency resolution for obtaining spectral components
frequency_mechanical = 1000  # 1 kHz
amplitude_mechanical = 0.5
duration = 5  # seconds
sampling_rate = 44100  # samples per second

# Generate mechanical engine sound
time, engine_sound = generate_mechanical_sound([frequency_mechanical], [amplitude_mechanical], [0], duration, sampling_rate)

# Calculate Fourier coefficients from the actual engine sound
frequencies_actual, magnitudes_actual, phases_actual = calculate_fourier_coefficients(engine_sound, frequency_resolution, sampling_rate)

# Synthesize mechanical engine sound based on Fourier coefficients
time_synthesized, mechanical_sound_synthesized = generate_mechanical_sound(frequencies_actual, magnitudes_actual, phases_actual, duration, sampling_rate)

# Play the synthesized sound
#sd.play(mechanical_sound_synthesized, sampling_rate)
#sd.wait()

# Plotting
plt.figure(figsize=(10, 6))
plt.subplot(2, 1, 1)
plt.plot(time, engine_sound, label='Actual Mechanical Sound')
plt.title('Actual Mechanical Engine Sound')
plt.xlabel('Time (seconds)')
plt.ylabel('Amplitude')
plt.legend()

plt.subplot(2, 1, 2)
plt.plot(time_synthesized, mechanical_sound_synthesized, label='Synthesized Mechanical Sound')
plt.title('Synthesized Mechanical Engine Sound')
plt.xlabel('Time (seconds)')
plt.ylabel('Amplitude')
plt.legend()

plt.tight_layout()
plt.show()
