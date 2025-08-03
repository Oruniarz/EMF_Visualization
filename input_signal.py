import numpy as np
import matplotlib.pyplot as plt


def input_signal(L, tmax):
    dt = tmax / (L - 1)
    t = np.linspace(0, tmax, L)
    output_signal = np.zeros(L)
    output_signal[0] = 1
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
