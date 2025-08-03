import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import ifft


def greens_signal(Nsamples, tmax, x, alpha, beta, gamma, a, b):
    # Time step
    dt = tmax / (Nsamples - 1)

    # Simulation time
    t = np.linspace(0, tmax, Nsamples)

    # Frequency, omega and s
    f = np.arange(Nsamples) / (dt * Nsamples)
    w = 2 * np.pi * f
    s = 1j * w

    # Media parameteres
    psi = ((s**(alpha + beta) + a * s**alpha + b) * (s**gamma + 1)) / (s**beta + a)
    k = np.sqrt(psi)

    # Positive value of k
    k = np.where(np.real(k) < 0, -k, k)

    # Output in the frequency domain
    # signal_fd = fft(hilbert(delta_signal)) – pomijamy, zakładamy jednostkowy impuls
    output_fd = np.exp(-k * x)

    # Output in the time domain
    output = (2 / dt) * ifft(output_fd)

    # Real part of th eoutput
    output_signal = np.real(output)

    return t, output_signal


# # Parameteres
# Nsamples = 1024
# tmax = 1.0
# x = 0.5
# alpha = 0.4
# beta = 0.2
# gamma = 0.1
# a = 1.0
# b = 0.5
#
# # Output
# t, output_signal = greens_signal(Nsamples, tmax, x, alpha, beta, gamma, a, b)
#
# # Plot
# plt.figure(figsize=(10, 4))
# plt.plot(t, output_signal, label='Green\'s Function Response')
# plt.title('Green\'s Function Response in Time Domain')
# plt.xlabel('Time [s]')
# plt.ylabel('Amplitude')
# plt.grid(True)
# plt.legend()
# plt.tight_layout()
# plt.show()
