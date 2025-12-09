import sys
from PyQt6.QtWidgets import QWidget, QApplication, QGraphicsView, QPushButton, QVBoxLayout, QLabel, QLineEdit
from PyQt6.QtCore import QSize
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import ifft
from output_signal import greens_signal
import math
from input_signal import input_signal


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.max_size = QSize(400, 50)
        self.resize(400, 300)
        self.view = QGraphicsView()
        self.initUI()
        self.setWindowTitle("Main menu")

    def initUI(self):
        self.layout = QVBoxLayout()

        tmax_label = QLabel("Max simulation time:")
        self.tmax_line = QLineEdit("1")
        nsamples_label = QLabel("Number of samples:")
        self.nsamples_line = QLineEdit("2**20")
        alpha_label = QLabel("Alpha:")
        self.alpha_line = QLineEdit("5/6")
        beta_label = QLabel("Beta:")
        self.beta_line = QLineEdit("2/3")
        gamma_label = QLabel("Gamma:")
        self.gamma_line = QLineEdit("2/3")
        a_label = QLabel("A:")
        self.a_line = QLineEdit("2*(9**(1/3))")
        b_label = QLabel("B:")
        self.b_line = QLineEdit("450")

        x_label = QLabel("Enter distances after decimal point:")
        self.x_line = QLineEdit("0.1,0.125,0.15,0.175,0.2")

        save_button = QPushButton("Save and proceed")
        save_button.setMaximumSize(self.max_size)
        save_button.clicked.connect(self.draw_figures)


        self.layout.addWidget(tmax_label)
        self.layout.addWidget(self.tmax_line)
        self.layout.addWidget(nsamples_label)
        self.layout.addWidget(self.nsamples_line)
        self.layout.addWidget(alpha_label)
        self.layout.addWidget(self.alpha_line)
        self.layout.addWidget(beta_label)
        self.layout.addWidget(self.beta_line)
        self.layout.addWidget(gamma_label)
        self.layout.addWidget(self.gamma_line)
        self.layout.addWidget(a_label)
        self.layout.addWidget(self.a_line)
        self.layout.addWidget(b_label)
        self.layout.addWidget(self.b_line)
        self.layout.addWidget(x_label)
        self.layout.addWidget(self.x_line)
        self.layout.addWidget(save_button)

        self.setLayout(self.layout)

    def eval_with_power(self, expr):
        expr = expr.replace("^", "**")
        return expr

    def draw_figures(self):
        line_styles = line_styles = ['-', '--', ':', '-.']
        safe_globals = {
            '__builtins__': {},
            'np': np,
            'math': math
        }

        try:
            tmax = eval(self.eval_with_power(self.tmax_line.text()), safe_globals)
            L = eval(self.eval_with_power(self.nsamples_line.text()), safe_globals)
            alpha = eval(self.eval_with_power(self.alpha_line.text()), safe_globals)
            beta = eval(self.eval_with_power(self.beta_line.text()), safe_globals)
            gamma = eval(self.eval_with_power(self.gamma_line.text()), safe_globals)
            a = eval(self.eval_with_power(self.a_line.text()), safe_globals)
            b = eval(self.eval_with_power(self.b_line.text()), safe_globals)
            raw_x_values = self.x_line.text().split(",")
            x_values = [float(x_value.strip()) for x_value in raw_x_values if x_value.strip() != ""]
            in_sig = input_signal(L, tmax)
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
                plt.plot(t, output_signal, style, label=f'x={x}')

        plt.legend(loc="best")
        plt.xlim([0, 0.1])
        plt.ylim([-5, 15])
        plt.xlabel('t\n(d)')
        plt.ylabel('u(x,t)')
        plt.grid(True)
        plt.tight_layout()
        plt.show()


def main():
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
