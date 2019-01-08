import sys

from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QDesktopWidget, QGridLayout, QLabel, QTextEdit, \
    QVBoxLayout, QRadioButton, QHBoxLayout, QGroupBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
from PyQt5 import QtWidgets, QtCore
import errors
import exact as graph
import numericals
from fractions import Fraction
import warnings


def represents_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


class Window(QDialog):
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def initUI(self):
        self.setWindowTitle("Differential equation grapher")
        self.q = QDesktopWidget().availableGeometry()
        self.setGeometry(self.q.width() / 6, self.q.height() / 6, self.q.width() / 2, self.q.height() / 2)
        self.show()

    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        self.center()
        self.initUI()
        self.figure = plt.figure()

        ax1 = self.figure.add_subplot(311)
        ax1.grid(True)
        ax1.set_title("Numerical methods", fontweight="bold", size=13)

        ax2 = self.figure.add_subplot(312)
        ax2.grid(True)
        ax2.set_title("Exact solution", fontweight="bold", size=13)

        ax3 = self.figure.add_subplot(313)
        ax3.grid(True)
        ax3.set_title("Local errors", fontweight="bold", size=13)

        self.figure.tight_layout()
        grid = QGridLayout()
        self.setLayout(grid)
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.button = QPushButton('Plot')
        self.button.clicked.connect(self.plot)

        self.sld = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)
        # self.x_sld = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)
        # self.y_sld = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)
        self.sld.setStyleSheet("""
                     QSlider{
                        background: #E3DEE2;
                        min-width:450px;
                        max-width:450px;
                     }
                     QSlider::groove:horizontal {  
                        height: 10px;
                        margin: 0px;
                        border-radius: 5px;
                        background: #B0AEB1;
                     }
                     QSlider::handle:horizontal {
                        background: #fff;
                        border: 1px solid #E3DEE2;
                        width: 17px;
                        margin: -5px 0px; 
                        border-radius: 8px;
                     }
                     QSlider::sub-page:qlineargradient {
                        background: #3B99FC;
                        border-radius: 5px;
                     }
                     """)

        self.sld.setMinimum(2)
        self.sld.setMaximum(100)

        # optimal approximation
        self.NUMBERS = 25
        self.sld.setValue(self.NUMBERS)

        self.X_STEP = 1
        self.Y_STEP = 1

        # self.x_sld.valueChanged.connect(self.x_change, self.x_sld.value())
        # self.y_sld.valueChanged.connect(self.y_change, self.y_sld.value())
        self.sld.valueChanged.connect(self.value_change, self.sld.value())

        self.function_label = QLabel("Function: ")
        self.function_le = QTextEdit()
        self.function_le.setFixedSize(self.q.width() / 8.5, self.q.height() / 41.2)
        self.function_le.setText("y'=sin(x)+y")

        self.label = QLabel("Number of points: " + str(self.sld.value()))
        # self.x_label = QLabel("Grid x step: " + str(self.x_sld.value() / 100))
        # self.y_label = QLabel("Grid y step: " + str(self.y_sld.value() / 100))
        self.x0_label = QLabel("x0: ")
        self.y0_label = QLabel("y0:")
        self.X_label = QLabel("X: ")
        self.N0_label = QLabel("Initial number of points (N0): ")
        self.NF_label = QLabel("Final number of points (NF): ")

        grid.setSpacing(25)
        self.x0_le = QTextEdit()
        self.x0_le.setFixedSize(self.q.width() / 8.5, self.q.height() / 41.2)
        self.x0_le.setText(str(0))

        self.y0_le = QTextEdit()
        self.y0_le.setFixedSize(self.q.width() / 8.5, self.q.height() / 41.2)
        self.y0_le.setText(str(1))

        self.X_le = QTextEdit()
        self.X_le.setFixedSize(self.q.width() / 8.5, self.q.height() / 41.2)
        self.X_le.setText(str(12 / 5))

        self.N0_le = QTextEdit()
        self.N0_le.setFixedSize(self.q.width() / 8.5, self.q.height() / 41.2)
        self.N0_le.setText(str(2))

        self.NF_le = QTextEdit()
        self.NF_le.setFixedSize(self.q.width() / 8.5, self.q.height() / 41.2)
        self.NF_le.setText(str(10))

        self.radio1 = QRadioButton("&Yes")
        self.radio2 = QRadioButton("&No")
        self.radio1.setChecked(True)

        self.radio1.toggled.connect(lambda: self.show_total_approximation_error(self.radio1))
        self.radio2.toggled.connect(lambda: self.show_total_approximation_error(self.radio2))

        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.radio1)
        self.hbox.addWidget(self.radio2)
        self.box = QGroupBox("&Show total approximation errors?")
        self.box.setLayout(self.hbox)

        self.mradio1 = QRadioButton("&Yes")
        self.mradio2 = QRadioButton("&No")
        self.mradio1.setChecked(True)

        self.mbox = QHBoxLayout()
        self.mbox.addWidget(self.mradio1)
        self.mbox.addWidget(self.mradio2)

        self.mGroupBox = QGroupBox("&Mark dots?")
        self.mGroupBox.setLayout(self.mbox)

        grid.addWidget(self.toolbar, 0, 0, 1, 25)
        grid.addWidget(self.canvas, 1, 0, 25, 25)
        grid.addWidget(self.function_label, 1, 25)
        grid.addWidget(self.function_le, 2, 25)
        grid.addWidget(self.label, 3, 25)
        grid.addWidget(self.sld, 4, 25)
        # grid.addWidget(self.x_label, 10, 25)
        # grid.addWidget(self.x_sld, 11, 25)
        # grid.addWidget(self.y_label, 12, 25)
        # grid.addWidget(self.y_sld, 13, 25)
        grid.addWidget(self.x0_label, 5, 25)
        grid.addWidget(self.x0_le, 6, 25)
        grid.addWidget(self.y0_label, 7, 25)
        grid.addWidget(self.y0_le, 8, 25)
        grid.addWidget(self.X_label, 9, 25)
        grid.addWidget(self.X_le, 10, 25)
        grid.addWidget(self.box, 11, 25)
        grid.addWidget(self.N0_label, 12, 25)
        grid.addWidget(self.N0_le, 13, 25)
        grid.addWidget(self.NF_label, 14, 25)
        grid.addWidget(self.NF_le, 15, 25)
        grid.addWidget(self.mGroupBox, 16, 25)
        grid.addWidget(self.button, 25, 25)

    def show_total_approximation_error(self, button):
        if button.text() == "&No" and button.isChecked():

            self.N0_label.hide()
            self.N0_le.hide()
            self.NF_label.hide()
            self.NF_le.hide()
            self.mGroupBox.hide()
        elif button.text() == "&Yes" and button.isChecked():
            self.N0_label.show()
            self.N0_le.show()
            self.NF_label.show()
            self.NF_le.show()
            self.mGroupBox.show()

    def x_change(self, value):
        self.x_sld.setValue(value)
        self.x_label.setText("Grid x step: " + str(self.x_sld.value() / 100))
        self.X_STEP = self.x_sld.value() / 100

    def y_change(self, value):
        self.y_sld.setValue(value)
        self.y_label.setText("Grid y step: " + str(self.y_sld.value() / 100))
        self.Y_STEP = self.y_sld.value() / 100

    def value_change(self, value):
        self.sld.setValue(value)
        self.label.setText("Number of points: " + str(self.sld.value()))
        self.NUMBERS = self.sld.value()

    def without_approximation(self):
        self.figure.clear()
        num_methods = numericals.Numerical_methods(self.x0, self.y0, self.X, self.NUMBERS)
        graphic = graph.Graph(self.x0, self.y0, self.X, self.NUMBERS)
        if self.radio2.isChecked():
            self.ax1 = self.figure.add_subplot(311)
            self.ax2 = self.figure.add_subplot(312)
            self.ax3 = self.figure.add_subplot(313)
        else:
            self.ax1 = self.figure.add_subplot(411)
            self.ax2 = self.figure.add_subplot(412)
            self.ax3 = self.figure.add_subplot(413)
            self.ax4 = self.figure.add_subplot(414)
        self.ax1.set_title("Numerical methods", fontweight="bold", size=13)
        self.ax2.set_title("Exact solution", fontweight="bold", size=13)
        self.ax3.set_title("Local errors", fontweight="bold", size=13)

        self.ax1.grid(True)
        self.ax2.grid(True)
        self.ax3.grid(True)

        # x_locator = mplt.ticker.MultipleLocator(base=self.X_STEP)
        # y_locator = mplt.ticker.MultipleLocator(base=self.Y_STEP)

        x, y_graph = graphic.solve()

        self.ax2.plot(x, y_graph, "purple", label="y'=sin(x)+y")
        self.ax2.legend(loc='upper left')
        # self.ax2.xaxis.set_major_locator(x_locator)
        # self.ax2.yaxis.set_major_locator(y_locator)

        x, y_euler = num_methods.euler()
        self.ax1.plot(x, y_euler, "red", label="Euler")
        self.ax1.legend(loc='upper left')

        x, y_improved_euler = num_methods.improved_euler()
        self.ax1.plot(x, y_improved_euler, "blue", label="Improved Euler")
        self.ax1.legend(loc='upper left')

        x, y_runge_kutta = num_methods.runge_kutta()
        self.ax1.plot(x, y_runge_kutta, "green", label="Runge Kutta")
        self.ax1.legend(loc='upper left')

        # self.ax1.xaxis.set_major_locator(x_locator)
        # self.ax1.yaxis.set_major_locator(y_locator)
        local_errors = errors.Errors(self.NUMBERS)

        y_local_euler = local_errors.local_error(y_graph, y_euler)
        self.ax3.plot(x, y_local_euler, "red", label="local euler error")
        self.ax3.legend(loc="upper left")

        y_local_improved = local_errors.local_error(y_graph, y_improved_euler)
        self.ax3.plot(x, y_local_improved, "blue", label="local improved euler error")
        self.ax3.legend(loc="upper left")

        y_local_runge_kutta = local_errors.local_error(y_graph, y_runge_kutta)
        self.ax3.plot(x, y_local_runge_kutta, "green", label="local runge-kutta error")
        self.ax3.legend(loc="upper left")

        """needed the second one because common locator for
        3 graphs takes minimum y grid (what is too small
        because of graph of approximation)
        """
        # y_error_locator = mplt.ticker.MultipleLocator(base=self.Y_STEP)
        # self.ax3.xaxis.set_major_locator(x_locator)
        # self.ax3.yaxis.set_major_locator(y_error_locator)

        hand, label = self.ax3.get_legend_handles_labels()
        handout = []
        lblout = []
        for h, l in zip(hand, label):
            if l not in lblout:
                lblout.append(l)
                handout.append(h)
        self.ax3.legend(handout, lblout, loc='best')

        self.figure.tight_layout()
        self.canvas.draw()

    def with_approximation(self):
        self.figure.clear()
        self.without_approximation()
        self.ax4.set_title("Total approximation errors", fontweight="bold", size=13)
        self.ax4.grid(True)
        # x_locator = mplt.ticker.MultipleLocator(base=1)
        # self.ax4.xaxis.set_major_locator(x_locator)

        euler_max_errors = []
        improved_euler_max_errors = []
        runge_kutta_max_errors = []
        nums = [k for k in range(self.N0, self.NF + 1)]
        for k in range(self.N0, self.NF + 1):
            num_methods = numericals.Numerical_methods(self.x0, self.y0, self.X, k)
            x, y_graph = graph.Graph(self.x0, self.y0, self.X, k).solve()
            local_errors = errors.Errors(k)

            x, y_euler = num_methods.euler()
            y_local_euler = local_errors.local_error(y_graph, y_euler)
            euler_max_errors.append(max(y_local_euler))

            x, y_improved_euler = num_methods.improved_euler()
            y_local_improved_euler = local_errors.local_error(y_graph, y_improved_euler)
            improved_euler_max_errors.append(max(y_local_improved_euler))

            x, y_runge_kutta = num_methods.runge_kutta()
            y_local_runge_kutta = local_errors.local_error(y_graph, y_runge_kutta)
            runge_kutta_max_errors.append(max(y_local_runge_kutta))
        self.ax4.plot(nums, euler_max_errors, "red", label='total approximation euler error')
        self.ax4.plot(nums, improved_euler_max_errors, "blue", label='total approximation improved euler error')
        self.ax4.plot(nums, runge_kutta_max_errors, "green", label='total approximation runge-kutta error')

        if (self.mradio1.isChecked()):
            self.ax4.plot(nums, euler_max_errors, 'ro', markersize=4)
            self.ax4.plot(nums, improved_euler_max_errors, 'bo', markersize=4)
            self.ax4.plot(nums, runge_kutta_max_errors, 'go', markersize=4)
            for i, j in zip(nums, euler_max_errors):
                self.ax4.annotate(str(i) + ";" + str(round(j, 3)), xy=(i, j), color='red')
            for i, j in zip(nums, improved_euler_max_errors):
                self.ax4.annotate(str(i) + ";" + str(round(j, 3)), xy=(i, j), color='blue')
            for i, j in zip(nums, runge_kutta_max_errors):
                self.ax4.annotate(str(i) + ";" + str(round(j, 3)), xy=(i, j), color='green')
        self.ax4.set_ylabel("Error value")
        self.ax4.set_xlabel("Number of points on each step")
        self.ax4.legend(loc='best')
        self.figure.tight_layout()
        self.canvas.draw()

    def plot(self):
        try:
            self.x0 = self.x0_le.toPlainText().replace(",", ".")
            self.y0 = self.y0_le.toPlainText().replace(",", ".")
            self.X = self.X_le.toPlainText().replace(",", ".")
            self.N0 = self.N0_le.toPlainText()
            self.NF = self.NF_le.toPlainText()
            if (graph.is_float(self.x0) and graph.is_float(self.X) and graph.is_float(self.y0)
                    and int(self.N0) and int(self.NF)):
                self.x0 = float(Fraction(self.x0))
                self.y0 = float(Fraction(self.y0))
                self.X = float(Fraction(self.X))
                self.N0 = int(self.N0)
                self.NF = int(self.NF)

                if self.x0 <= self.X and self.radio2.isChecked():
                    self.without_approximation()
                elif self.x0 <= self.X and self.N0 <= self.NF and self.N0 > 1 and self.NF > 1 and self.radio1.isChecked():
                    self.with_approximation()
                elif self.x0 > self.X:
                    self.msg = MsgBox("x0 is greater than X")
                elif self.N0 > self.NF:
                    self.msg = MsgBox("N0 is greater than Nf")
                elif (self.N0 <= 1 or self.NF <= 1) and self.radio1.isChecked():
                    self.msg = MsgBox("N0 and Nf must be > 1")
            elif (graph.is_float(self.x0) == False):
                self.msg = MsgBox("x0 is not double")
            elif (graph.is_float(self.X) == False):
                self.msg = MsgBox("X is not double")
            elif (graph.is_float(self.y0) == False):
                self.msg = MsgBox("y0 is not double")
        except ValueError:
            if (represents_int(self.N0) == False or represents_int(self.NF) == False):
                self.msg = MsgBox("N0 or NF is not an integer")


class MsgBox(QDialog):
    def __init__(self, message):
        super().__init__()
        layout = QVBoxLayout(self)
        self.label = QLabel(message)
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.close)
        self.setWindowTitle("Error")
        layout.addWidget(self.label)
        layout.addWidget(close_btn)
        self.q = QDesktopWidget().availableGeometry()
        self.setGeometry(self.q.width() / 3, self.q.height() / 2,
                         self.q.width() / 9.6, self.q.height() / 12.8)
        self.show()


if __name__ == '__main__':
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        app = QApplication(sys.argv)
        main = Window()
        main.show()
        sys.exit(app.exec_())
