from PyQt5.QtWidgets import QMainWindow
from ui.utils.observer import Observer


class MachineWindowView(QMainWindow, Observer):

    def __init__(self, controller, model, parent):
        super(QMainWindow, self).__init__(parent)
        self.controller = controller
        self.model = model

    def model_is_changed(self):
        pass
