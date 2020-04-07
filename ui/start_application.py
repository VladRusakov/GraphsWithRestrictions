from PyQt5 import QtWidgets, QtCore

from ui.main_window import Ui_MainWindow
from ui.canvas import MplCanvas

import random


class StartWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.setupUi(self)

        # canvas copypaste experiment
        self.canvas = MplCanvas(self, width=4, height=4, dpi=100)
        self.canvas2 = MplCanvas(self, width=4, height=4, dpi=100)

        #self.horizontalLayoutGraphics.addChildWidget(self.canvas)
        self.horizontalLayoutGraphics.addWidget(self.canvas)
        self.horizontalLayoutGraphics.addWidget(self.canvas2)
        #self.horizontalLayoutGraphics.addChildWidget(self.canvas2)
        #self.setCentralWidget(self.canvas)

        n_data = 50
        self.xdata = list(range(n_data))
        self.ydata = [random.randint(0, 10) for i in range(n_data)]
        self.update_plot()

        self.show()

        # Setup a timer to trigger the redraw by calling update_plot.
        self.timer = QtCore.QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.update_plot)
        self.timer.start()

        # endof canvas experiment

    def update_plot(self):
        # Drop off the first y element, append a new one.
        self.ydata = self.ydata[1:] + [random.randint(0, 10)]
        self.canvas.axes.cla()  # Clear the canvas.
        self.canvas.axes.plot(self.xdata, self.ydata, 'r')
        # Trigger the canvas to update and redraw.
        self.canvas.draw()

        #self.pushButtonToLayered.clicked.connect(QtWidgets.qApp.quit)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = StartWindow()
    window.show()
    sys.exit(app.exec())
