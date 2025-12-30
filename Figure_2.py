import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import ifft
from output_signal import output_signal

tmax = 100
L = 2 ** 20

# Parameters
alpha = 5 / 6
beta = 2 / 3
gamma = 2 / 3
a = 2 * (9 ** (1 / 3))
b = 4.5

x_values = [0.1, 0.125, 0.15, 0.175, 0.2]
line_styles = ['-', '--', ':', '-.', '-']
line_widths = [1, 1, 1, 1, 2]

plt.figure(figsize=(10, 5))

for x, style, lw in zip(x_values, line_styles, line_widths):
    print(f'Processing x = {x} ...')
    t, output_signal = output_signal(L, tmax, x, alpha, beta, gamma, a, b)

    mask = t <= 0.15
    plt.plot(t, output_signal, style, linewidth=lw, label=f'x={x}')

# Plot
plt.legend()
plt.xlim([0, 0.15])
plt.ylim([0, 25])
plt.xlabel('t')
plt.ylabel('u(x,t)')
plt.grid(True)
plt.tight_layout()
plt.show()