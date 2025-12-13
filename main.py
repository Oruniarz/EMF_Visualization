import sys
import customtkinter as ctk
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
import math
from output_signal import greens_signal

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Main menu")
        self.geometry("1200x800")
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Left panel
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="Parametres", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Max simulation time
        self.label_tmax = ctk.CTkLabel(self.sidebar_frame, text="Max simulation time [s]:")
        self.label_tmax.grid(row=1, column=0, padx=20, pady=(10, 0))
        self.entry_tmax = ctk.CTkEntry(self.sidebar_frame, placeholder_text="e.g. 1", width=160)
        self.entry_tmax.grid(row=2, column=0, padx=20, pady=(0, 10))
        self.entry_tmax.insert(0, "1.0")

        # Number of samples
        self.label_nsamples = ctk.CTkLabel(self.sidebar_frame, text="Number of samples:")
        self.label_nsamples.grid(row=3, column=0, padx=20, pady=(10, 0))
        self.entry_nsamples = ctk.CTkEntry(self.sidebar_frame, placeholder_text="e.g. 2**20", width=160)
        self.entry_nsamples.grid(row=4, column=0, padx=20, pady=(0, 10))
        self.entry_nsamples.insert(0, "2**20")

        # Alpha
        self.label_alpha = ctk.CTkLabel(self.sidebar_frame, text="Alpha:")
        self.label_alpha.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.entry_alpha = ctk.CTkEntry(self.sidebar_frame, placeholder_text="e.g. 5/6", width=160)
        self.entry_alpha.grid(row=6, column=0, padx=20, pady=(0, 10))
        self.entry_alpha.insert(0, "5/6")

        # Beta
        self.label_beta = ctk.CTkLabel(self.sidebar_frame, text="Beta:")
        self.label_beta.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.entry_beta = ctk.CTkEntry(self.sidebar_frame, placeholder_text="e.g. 2/3", width=160)
        self.entry_beta.grid(row=8, column=0, padx=20, pady=(0, 10))
        self.entry_beta.insert(0, "2/3")

        # Gamma
        self.label_gamma = ctk.CTkLabel(self.sidebar_frame, text="Gamma:")
        self.label_gamma.grid(row=9, column=0, padx=20, pady=(10, 0))
        self.entry_gamma = ctk.CTkEntry(self.sidebar_frame, placeholder_text="e.g. 2/3", width=160)
        self.entry_gamma.grid(row=10, column=0, padx=20, pady=(0, 10))
        self.entry_gamma.insert(0, "2/3")

        # Parameter A
        self.label_aparam = ctk.CTkLabel(self.sidebar_frame, text="A:")
        self.label_aparam.grid(row=11, column=0, padx=20, pady=(10, 0))
        self.entry_aparam = ctk.CTkEntry(self.sidebar_frame, placeholder_text="e.g. 2*(9**(1/3))", width=160)
        self.entry_aparam.grid(row=12, column=0, padx=20, pady=(0, 10))
        self.entry_aparam.insert(0, "2*(9**(1/3))")

        # Parameter B
        self.label_bparam = ctk.CTkLabel(self.sidebar_frame, text="B:")
        self.label_bparam.grid(row=13, column=0, padx=20, pady=(10, 0))
        self.entry_bparam = ctk.CTkEntry(self.sidebar_frame, placeholder_text="e.g. 450", width=160)
        self.entry_bparam.grid(row=14, column=0, padx=20, pady=(0, 10))
        self.entry_bparam.insert(0, "450")

        # Delta x
        self.label_x = ctk.CTkLabel(self.sidebar_frame, text="Enter distances after decimal point:")
        self.label_x.grid(row=15, column=0, padx=20, pady=(10, 0))
        self.entry_x = ctk.CTkEntry(self.sidebar_frame, placeholder_text="e.g. 0.1,0.125,0.15,0.175,0.2", width=160)
        self.entry_x.grid(row=16, column=0, padx=20, pady=(0, 10))
        self.entry_x.insert(0, "0.1,0.125,0.15,0.175,0.2")

        # Button
        self.button_draw = ctk.CTkButton(self.sidebar_frame, text="Save and proceed", command=self.save_button)
        self.button_draw.grid(row=17, column=0, padx=20, pady=20)

        # Right panel
        self.plot_frame = ctk.CTkFrame(self)
        self.plot_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        # Figure
        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.ax.set_title("Waiting for data...")
        self.ax.grid(True, linestyle='--', alpha=0.6)

        # Figure in TKinter
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.plot_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.plot_frame)
        self.toolbar.update()

    def eval_with_power(self, expr):
        expr = expr.replace("^", "**")
        return expr

    def save_button(self):
        line_styles = line_styles = ['-', '--', ':', '-.']
        safe_globals = {
            '__builtins__': {},
            'np': np,
            'math': math
        }
        try:
            # Getting data from inputs
            tmax = eval(self.eval_with_power(self.entry_tmax.get()), safe_globals)
            L = eval(self.eval_with_power(self.entry_nsamples.get()), safe_globals)
            alpha = eval(self.eval_with_power(self.entry_alpha.get()), safe_globals)
            beta = eval(self.eval_with_power(self.entry_beta.get()), safe_globals)
            gamma = eval(self.eval_with_power(self.entry_gamma.get()), safe_globals)
            a = eval(self.eval_with_power(self.entry_aparam.get()), safe_globals)
            b = eval(self.eval_with_power(self.entry_bparam.get()), safe_globals)
            raw_x_values = self.entry_x.get().split(",")
            x_values = [float(x_value.strip()) for x_value in raw_x_values if x_value.strip() != ""]
            # in_sig = input_signal(L, tmax)
            # plt.plot(in_sig[0], in_sig[1])
            # print(x_values)
        except (SyntaxError, TypeError, NameError, ZeroDivisionError):
            print("Insert correct input")
        except Exception as e:
            print(f"Error:\n{str(type(e).__name__)}: {str(e)}")
            sys.exit(1)
        else:
            for i, x in enumerate(x_values):
                style = line_styles[i % len(line_styles)]
                t, output_signal = greens_signal(L, tmax, x, alpha, beta, gamma, a, b)
                self.ax.plot(t, output_signal, style, label=f'x={x}')

        self.ax.legend(loc="best")
        self.ax.set_xlim(0,0.1)
        self.ax.set_ylim(-5, 15)
        self.ax.set_xlabel('t')
        self.ax.set_ylabel('u(x,t)')
        self.ax.grid(True, linestyle='--', alpha=0.6)
        self.ax.set_title('Figure')
        self.canvas.draw()

        # Czyszczenie i rysowanie nowego wykresu
        # self.ax.clear()
        # self.ax.plot(t, y, color='#3B8ED0', linewidth=2)  # Kolor pasujący do motywu
        # self.ax.set_title(f"Wykres funkcji: $y = {A} \cdot \sin(2\pi \cdot {f} \cdot t)$")
        # self.ax.set_xlabel("Czas [s]")
        # self.ax.set_ylabel("Amplituda")
        # self.ax.grid(True, linestyle='--', alpha=0.6)

        # Odświeżenie widoku


if __name__ == "__main__":
    app = App()
    app.mainloop()