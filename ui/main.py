import sys
from PyQt5.QtWidgets import QApplication
from ui.controllers.main_window_controller import MainWindowController
from ui.models.main_window_model import MainWindowModel


def main():
    application = QApplication(sys.argv)
    model = MainWindowModel()
    controller = MainWindowController(model)
    application.exec()


if __name__ == "__main__":
    sys.exit(main())
