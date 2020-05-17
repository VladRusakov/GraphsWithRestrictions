from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow
from ui.utils.observer import Observer
from ui.utils.window_metaclasses import WrapperAndAbcMeta


class MachineWindowView(QMainWindow, Observer, metaclass=WrapperAndAbcMeta):

    def __init__(self, controller, model, parent=None):
        super(QMainWindow, self).__init__(parent)
        self.controller = controller
        self.model = model
        self.setupUi()
        self.show()

    def setupUi(self):
        MainWindow = self
        MainWindow.setObjectName("MachineWindow")
        MainWindow.setWindowTitle('Автомат преобразования графа')
        MainWindow.resize(800, 600)

        self.centralWidget = QtWidgets.QWidget()
        self.setCentralWidget(self.centralWidget)

        self.menubar = self.menuBar()
        self.open_machine = self.menubar.addMenu('Открыть')
        self.save_machine = self.menubar.addMenu('Сохранить')
        self.clear_machine = self.menubar.addMenu('Очистить')

        self.horizontalLayoutMain = QtWidgets.QHBoxLayout()
        self.centralWidget.setLayout(self.horizontalLayoutMain)

        self.tableWidget = QtWidgets.QTableWidget()
        self.horizontalLayoutMain.addWidget(self.tableWidget)

        verticalLayoutButtons = QtWidgets.QVBoxLayout()
        verticalLayoutWidget = QtWidgets.QWidget()
        verticalLayoutWidget.setLayout(verticalLayoutButtons)
        self.horizontalLayoutMain.addWidget(verticalLayoutWidget)

        horizontalLayoutStates = QtWidgets.QHBoxLayout()
        verticalLayoutButtons.addChildLayout(horizontalLayoutStates)
        self.statesInput = QtWidgets.QTextEdit()
        self.statesButton = QtWidgets.QPushButton(text='Задать состояния')
        horizontalLayoutStates.addWidget(self.statesInput)
        horizontalLayoutStates.addWidget(self.statesButton)

        #self.tableWidget.clicked.connect(self.on_click)
        #self.button = QtWidgets.QPushButton(text='KKKKK')
        #self.horizontalLayoutMain.addWidget(self.button)
        #self.centralWidget.addWidget(self.button)

    @pyqtSlot()
    def on_click(self):
        print("kek")

    def model_is_changed(self):
        pass
