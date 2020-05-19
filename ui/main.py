import sys

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication
from ui.controllers.main_window_controller import MainWindowController
from ui.models.main_window_model import MainWindowModel


def main():
    application = QApplication(sys.argv)
    model = MainWindowModel()
    controller = MainWindowController(model)
    font = QFont("Consolas", 16, QFont.StyleItalic)
    application.setFont(font)
    application.exec()


if __name__ == "__main__":
        sys.exit(main())
