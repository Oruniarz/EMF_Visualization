import sys
from PyQt6.QtWidgets import QWidget, QApplication, QGraphicsView, QPushButton, QVBoxLayout, QLabel, QLineEdit
from PyQt6.QtCore import QSize
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import ifft
from output_signal import greens_signal
import math


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
        self.tmax_line = QLineEdit()
        nsamples_label = QLabel("Number of samples:")
        self.nsamples_line = QLineEdit()
        alpha_label = QLabel("Alpha:")
        self.alpha_line = QLineEdit()
        beta_label = QLabel("Beta:")
        self.beta_line = QLineEdit()
        gamma_label = QLabel("Gamma:")
        self.gamma_line = QLineEdit()
        a_label = QLabel("A:")
        self.a_line = QLineEdit()
        b_label = QLabel("B:")
        self.b_line = QLineEdit()

        x_label = QLabel("Enter distances after decimal point:")
        self.x_line = QLineEdit()

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

    def draw_figures(self):
        line_styles = line_styles = ['-', '--', ':', '-.']
        safe_globals = {
            '__builtins__': {},
            'np': np,
            'math': math
        }
        try:
            tmax = eval(self.tmax_line.text(), safe_globals)
            L = eval(self.nsamples_line.text(), safe_globals)
            alpha = eval(self.alpha_line.text(), safe_globals)
            beta = eval(self.beta_line.text(), safe_globals)
            gamma = eval(self.gamma_line.text(), safe_globals)
            a = eval(self.a_line.text(), safe_globals)
            b = eval(self.b_line.text(), safe_globals)
            raw_x_values = self.x_line.text().split(",")
            x_values = [float(x_value.strip()) for x_value in raw_x_values if x_value.strip() != ""]
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

        plt.legend()
        plt.xlim([0, 0.005])
        plt.ylim([0, 100])
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
