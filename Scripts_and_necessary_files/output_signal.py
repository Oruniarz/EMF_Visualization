import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import ifft, fft
from scipy.signal import hilbert


def output_signal(Nsamples, tmax, x, alpha, beta, gamma, a, b, input_signal):
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
    signal_fd = fft(input_signal[1]) + 1j * (-1j * np.sign(w) * fft(input_signal[1]))
    output_fd = signal_fd*np.exp(-k * x)
    # output_fd = np.exp(-k * x)

    # Output in the time domain
    output = (2 / dt) * ifft(output_fd)

    # Real part of the output
    output_signal = np.real(output)

    return t, output_signal