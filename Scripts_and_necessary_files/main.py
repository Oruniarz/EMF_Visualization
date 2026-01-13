import customtkinter as ctk
import tkinter as tk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import numpy as np
import math
from output_signal import output_signal
from Scripts_and_necessary_files.input_signal import input_signal
from Scripts_and_necessary_files.error_window import show_error

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.example_dict = dict(tmax_example="1.0",
                                 nsamples_example="2**20",
                                 alpha_example="5/6",
                                 beta_example="2/3",
                                 gamma_example="2/3",
                                 aparam_example="2*(9**(1/3))",
                                 bparam_example="450",
                                 x_example="0.1,0.125,0.15,0.175,0.2",
                                 time_axis_example="0,0.125",
                                 y_axis_example="-5,30")

        self.title("Main menu")
        self.geometry("1500x715")
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=0)
        self.grid_columnconfigure(3, weight=1)
        self.grid_rowconfigure(0, weight=0)

        self.first_panel_init()
        self.second_panel_init()
        self.figure_panel_init()

    def first_panel_init(self):
        # Left panel
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_label = ctk.CTkLabel(self.sidebar_frame, text="Parameters",
                                          font=ctk.CTkFont(size=20, weight="bold"))
        self.sidebar_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Max simulation time
        self.label_tmax = ctk.CTkLabel(self.sidebar_frame, text="Max simulation time [s]:")
        self.label_tmax.grid(row=1, column=0, padx=20, pady=(10, 0))
        self.entry_tmax = ctk.CTkEntry(self.sidebar_frame, placeholder_text=f"e.g. {self.example_dict['tmax_example']}",width=160)
        self.entry_tmax.grid(row=2, column=0, padx=20, pady=(0, 10))
        self.entry_tmax.insert(0, self.example_dict['tmax_example'])

        # Number of samples
        self.label_nsamples = ctk.CTkLabel(self.sidebar_frame, text="Number of samples:")
        self.label_nsamples.grid(row=3, column=0, padx=20, pady=(10, 0))
        self.entry_nsamples = ctk.CTkEntry(self.sidebar_frame, placeholder_text=f"e.g. {self.example_dict['nsamples_example']}", width=160)
        self.entry_nsamples.grid(row=4, column=0, padx=20, pady=(0, 10))
        self.entry_nsamples.insert(0, self.example_dict['nsamples_example'])

        # Alpha
        self.label_alpha = ctk.CTkLabel(self.sidebar_frame, text="Alpha:")
        self.label_alpha.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.entry_alpha = ctk.CTkEntry(self.sidebar_frame, placeholder_text=f"e.g. {self.example_dict['alpha_example']}", width=160)
        self.entry_alpha.grid(row=6, column=0, padx=20, pady=(0, 10))
        self.entry_alpha.insert(0, self.example_dict['alpha_example'])

        # Beta
        self.label_beta = ctk.CTkLabel(self.sidebar_frame, text="Beta:")
        self.label_beta.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.entry_beta = ctk.CTkEntry(self.sidebar_frame, placeholder_text=f"e.g. {self.example_dict['beta_example']}", width=160)
        self.entry_beta.grid(row=8, column=0, padx=20, pady=(0, 10))
        self.entry_beta.insert(0, self.example_dict['beta_example'])

        # Gamma
        self.label_gamma = ctk.CTkLabel(self.sidebar_frame, text="Gamma:")
        self.label_gamma.grid(row=9, column=0, padx=20, pady=(10, 0))
        self.entry_gamma = ctk.CTkEntry(self.sidebar_frame, placeholder_text=f"e.g. {self.example_dict['gamma_example']}", width=160)
        self.entry_gamma.grid(row=10, column=0, padx=20, pady=(0, 10))
        self.entry_gamma.insert(0, self.example_dict['gamma_example'])

        # Parameter A
        self.label_aparam = ctk.CTkLabel(self.sidebar_frame, text="A:")
        self.label_aparam.grid(row=11, column=0, padx=20, pady=(10, 0))
        self.entry_aparam = ctk.CTkEntry(self.sidebar_frame, placeholder_text=f"e.g. {self.example_dict['aparam_example']}", width=160)
        self.entry_aparam.grid(row=12, column=0, padx=20, pady=(0, 10))
        self.entry_aparam.insert(0, self.example_dict['aparam_example'])

        # Parameter B
        self.label_bparam = ctk.CTkLabel(self.sidebar_frame, text="B:")
        self.label_bparam.grid(row=13, column=0, padx=20, pady=(10, 0))
        self.entry_bparam = ctk.CTkEntry(self.sidebar_frame, placeholder_text=f"e.g. {self.example_dict['bparam_example']}", width=160)
        self.entry_bparam.grid(row=14, column=0, padx=20, pady=(0, 10))
        self.entry_bparam.insert(0, self.example_dict['bparam_example'])

        # Delta x
        self.label_x = ctk.CTkLabel(self.sidebar_frame, text="Enter distances after decimal point [m]:")
        self.label_x.grid(row=15, column=0, padx=20, pady=(10, 0))
        self.entry_x = ctk.CTkEntry(self.sidebar_frame, placeholder_text=f"e.g. {self.example_dict['x_example']}", width=160)
        self.entry_x.grid(row=16, column=0, padx=20, pady=(0, 20))
        self.entry_x.insert(0, self.example_dict['x_example'])

        # Draw figure button
        self.button_draw = ctk.CTkButton(self, text="Save and proceed", command=self.save_button)
        self.button_draw.grid(row=17, column=0, columnspan=3, sticky='ew', padx=(10, 10), pady=5)

    def second_panel_init(self):
        # Third panel
        self.sidebar2_frame = ctk.CTkFrame(self, width=100, corner_radius=0)
        self.sidebar2_frame.grid(row=0, column=1, sticky="nsew")
        self.sidebar2_label = ctk.CTkLabel(self.sidebar2_frame, text="Axes",
                                           font=ctk.CTkFont(size=20, weight="bold"))
        self.sidebar2_label.grid(row=0, column=1, padx=20, pady=(20, 10))

        # Axis "x" params
        self.label_xaxis = ctk.CTkLabel(self.sidebar2_frame, text="Time axis limits after decimal point:")
        self.label_xaxis.grid(row=1, column=1, padx=20, pady=(10, 0))
        self.entry_xaxis = ctk.CTkEntry(self.sidebar2_frame, placeholder_text=f"e.g. {self.example_dict['time_axis_example']}", width=100)
        self.entry_xaxis.grid(row=2, column=1, padx=20, pady=(0, 10))
        self.entry_xaxis.insert(0, self.example_dict['time_axis_example'])

        # Axis "y" params
        self.label_yaxis = ctk.CTkLabel(self.sidebar2_frame, text="'Y' axis limits after decimal point:")
        self.label_yaxis.grid(row=3, column=1, padx=20, pady=(10, 0))
        self.entry_yaxis = ctk.CTkEntry(self.sidebar2_frame, placeholder_text=f"e.g. {self.example_dict['y_axis_example']}", width=100)
        self.entry_yaxis.grid(row=4, column=1, padx=20, pady=(0, 10))
        self.entry_yaxis.insert(0, self.example_dict['y_axis_example'])

    def figure_panel_init(self):
        # Right panel
        self.plot_frame = ctk.CTkFrame(self)
        self.plot_frame.grid(row=0, column=3, padx=20, pady=20, sticky="nsew")

        # Figure
        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.ax.set_title("Waiting for data...")
        self.ax.grid(True, linestyle='--', alpha=0.6)
        self.ax.set_xlim(0, 0.1)
        self.ax.set_ylim(-5, 15)
        self.ax.set_xlabel('t')
        self.ax.set_ylabel('u(x,t)')

        # Figure in TKinter
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.plot_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.plot_frame)
        self.toolbar.update()

    def save_button(self):
        line_styles = line_styles = ['-', '--', ':', '-.']
        safe_globals = {
            '__builtins__': {},
            'np': np,
            'math': math
        }
        eval_with_power = lambda expr: expr.replace("^", "**")
        try:
            # Getting data from inputs
            tmax = eval(eval_with_power(self.entry_tmax.get()), safe_globals)
            L = eval(eval_with_power(self.entry_nsamples.get()), safe_globals)
            alpha = eval(eval_with_power(self.entry_alpha.get()), safe_globals)
            beta = eval(eval_with_power(self.entry_beta.get()), safe_globals)
            gamma = eval(eval_with_power(self.entry_gamma.get()), safe_globals)
            a = eval(eval_with_power(self.entry_aparam.get()), safe_globals)
            b = eval(eval_with_power(self.entry_bparam.get()), safe_globals)
            raw_x_values = self.entry_x.get().split(",")
            x_values = [float(x_value.strip()) for x_value in raw_x_values if x_value.strip() != ""]
            in_sig = input_signal(L, tmax)
        except (SyntaxError, TypeError, NameError, ZeroDivisionError, ValueError):
            show_error(self, "Please insert correct input")
        except Exception as e:
            error_msg = f"Fatal error:\n{str(type(e).__name__)}: {str(e)}\n Closing application"
            show_error(self, error_msg, True)
        else:
            try:
                # Drawing graphs
                self.ax.clear()
                # self.ax.plot(in_sig[0], in_sig[1], label='Input signal')
                for i, x in enumerate(x_values):
                    style = line_styles[i % len(line_styles)]
                    output_data = output_signal(L, tmax, x, alpha, beta, gamma, a, b, in_sig)
                    self.ax.plot(output_data[0], output_data[1], style, label=f'x={x}')

            except (SyntaxError, TypeError, NameError, ZeroDivisionError, ValueError):
                error_msg = ("Inserted values do not allow for generating a valid output. "
                             "Please insert different inputs.")
                show_error(self, error_msg)
            except Exception as e:
                error_msg = f"Fatal error:\n{str(type(e).__name__)}: {str(e)}\n Closing application"
                show_error(self, error_msg, True)
            else:
                time_axis = self.entry_xaxis.get().split(',')
                self.ax.set_xlim(float(time_axis[0]), float(time_axis[1]))
                y_axis = self.entry_yaxis.get().split(',')
                self.ax.set_ylim(float(y_axis[0]), float(y_axis[1]))

                self.ax.set_title('Impulse response of the system')
                self.ax.legend(loc="best")
                self.ax.grid(True, linestyle='--', alpha=0.6)
                self.ax.set_xlabel('t [s]')
                self.ax.set_ylabel('u(x,t) [V]')
                self.canvas.draw()


if __name__ == "__main__":
    app = App()
    app.mainloop()
