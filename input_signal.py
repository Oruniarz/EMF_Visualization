import numpy as np
import matplotlib.pyplot as plt


def input_signal(Nsamples, tmax):
    t = np.linspace(0, tmax, Nsamples)
    output_signal = np.zeros(Nsamples)
    output_signal[0] = 1
    return t, output_signal
