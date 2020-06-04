from typing import List
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow

from ui.utils.window_metaclasses import WrapperAndAbcMeta


class ObtainWindowView(QMainWindow, metaclass=WrapperAndAbcMeta):

    def __init__(self, controller, variants: List[str]):
        super(QMainWindow, self).__init__()
        self.controller = controller
        self.variants = variants
        self.setupUi()
        self.show()

    def setupUi(self):
        MainWindow = self
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        central_widget = QtWidgets.QWidget(MainWindow)
        MainWindow.setCentralWidget(central_widget)

        # vertical layout
        self.verticalLayoutMain = QtWidgets.QVBoxLayout()
        central_widget.setLayout(self.verticalLayoutMain)

        self.variants_combo_box = QtWidgets.QComboBox(parent=central_widget)
        self.variants_combo_box.addItems(self.variants)
        self.verticalLayoutMain.addWidget(self.variants_combo_box)

        self.obtainButton = QtWidgets.QPushButton(text='Выполнить', parent=central_widget)
        self.obtainButton.adjustSize()
        self.verticalLayoutMain.addWidget(self.obtainButton)

        self.variants_widget = QtWidgets.QWidget(self.centralWidget())
        self.change_view(self.variants[0])  # TODO unsafe when variants fool

        self.variants_combo_box.currentTextChanged.connect(self.change_view)
        self.obtainButton.clicked.connect(self.controller.gather_data_from_getters)

    def change_view(self, variant: str):
        # изменить содержимое Layer'а в ObtainView

        self.variants_widget.close()
        self.variants_widget = QtWidgets.QWidget(self.centralWidget())
        self.variants_layout = QtWidgets.QVBoxLayout()

        self.variants_widget.setLayout(self.variants_layout)
        self.verticalLayoutMain.addWidget(self.variants_widget)
        self.controller.set_variant_widgets(variant, self.variants_widget)
