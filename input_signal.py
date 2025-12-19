import numpy as np
import matplotlib.pyplot as plt


def input_signal(Nsamples, tmax, amplitude=1, freq=1, signal_type=0):
    t = np.linspace(0, tmax, Nsamples)
    if signal_type == 0:
        output_signal = np.zeros(Nsamples)
        output_signal[0] = 1 * amplitude
        return t, output_signal
    elif signal_type == 1:
        output_signal = amplitude * np.sin(2 * np.pi * freq * t)
        return t, output_signal

# L = 100
# tmax = 1.0
# t, output_signal = input_signal(L, tmax)
#
# # Wykres
# plt.figure(figsize=(8, 4))
# plt.plot(t, output_signal, marker='o')
# plt.title('Output Signal')
# plt.xlabel('Time [s]')
# plt.ylabel('Amplitude')
# plt.grid(True)
# plt.show()
