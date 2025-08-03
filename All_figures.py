import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import ifft
from output_signal import greens_signal

tmax = 100
L = 2**20
a_val = 2 * (9**(1 / 3))
x_values = [0.1, 0.125, 0.15, 0.175, 0.2]
line_styles = ['-', '--', ':', '-.', '-']
line_widths = [1, 1, 1, 1, 2]

# Parameteres
fig_params = [
    # (alpha, beta, gamma, b, xlim_max, ylim, xlabel_tag)
    (0.25, 2/3, 2/3, 450, 0.005, (0, 100), '(a)'),  # Fig. 7
    (5/6, 2/3, 2/3, 4.5,  0.15,  (0, 25),  '(b)'),  # Fig. 8
    (5/6, 2/3, 2/3, 9,    0.15,  (0, 25),  '(c)'),  # Fig. 9
    (5/6, 2/3, 2/3, 450,  0.1,   (-5, 15), '(d)'),  # Fig.10
]


# Plots
fig, axs = plt.subplots(2, 2, figsize=(14, 10))
axs = axs.flatten()

for idx, (alpha, beta, gamma, b, xlim_max, ylim, xlabel_tag) in enumerate(fig_params):
    ax = axs[idx]
    for x, style, lw in zip(x_values, line_styles, line_widths):
        print(f'Fig. {idx+7} – processing x = {x}...')
        t, output_signal = greens_signal(L, tmax, x, alpha, beta, gamma, a_val, b)
        mask = t <= xlim_max
        ax.plot(t[mask], output_signal[mask], style, linewidth=lw, label=f'x={x}')

    ax.set_xlim([0, xlim_max])
    ax.set_ylim(ylim)
    ax.set_xlabel(f't\n{xlabel_tag}')
    ax.set_ylabel('u(x,t)')
    ax.grid(True)
    if idx == 0:
        ax.legend(fontsize=8)

fig.tight_layout()
plt.show()