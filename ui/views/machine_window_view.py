from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QSizePolicy, QTableWidgetItem

from ui.models.machine_window_model import MachineWindowModel
from ui.utils.observer import Observer
from ui.utils.window_metaclasses import WrapperAndAbcMeta


class MachineWindowView(QMainWindow, Observer, metaclass=WrapperAndAbcMeta):

    def __init__(self, controller, model: MachineWindowModel, parent=None):
        super(QMainWindow, self).__init__(parent)
        self.controller = controller
        self.model = model
        self.model.add_observer(self)
        self.setupUi()
        self.register_events()
        self.model_is_changed()
        self.show()

    def setupUi(self):
        MainWindow = self
        MainWindow.setObjectName("MachineWindow")
        MainWindow.setWindowTitle('Автомат преобразования графа')
        MainWindow.resize(800, 600)

        self.centralWidget = QtWidgets.QWidget()
        self.setCentralWidget(self.centralWidget)

        self.menubar = self.menuBar()
        self.open_machine = QtWidgets.QAction('Открыть')
        self.menubar.addAction(self.open_machine)
        self.save_machine = QtWidgets.QAction('Сохранить')
        self.menubar.addAction(self.save_machine)
        self.clear_machine = QtWidgets.QAction('Очистить')
        self.menubar.addAction(self.clear_machine)

        self.horizontalLayoutMain = QtWidgets.QHBoxLayout()
        self.centralWidget.setLayout(self.horizontalLayoutMain)

        self.tableWidget = QtWidgets.QTableWidget()
        self.tableWidget.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.tableWidget.setMinimumSize(300, 500)
        self.tableWidget.resizeColumnsToContents()
        self.horizontalLayoutMain.addWidget(self.tableWidget)

        verticalLayoutButtons = QtWidgets.QVBoxLayout()
        verticalLayoutWidget = QtWidgets.QWidget()
        verticalLayoutWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        verticalLayoutWidget.setLayout(verticalLayoutButtons)
        self.horizontalLayoutMain.addWidget(verticalLayoutWidget)

        horizontalLayoutStates = QtWidgets.QHBoxLayout()
        verticalLayoutButtons.addLayout(horizontalLayoutStates)
        self.statesInput = QtWidgets.QTextEdit()
        self.statesInput.setFixedWidth(330)
        self.statesButton = QtWidgets.QPushButton(text='Задать состояния')

        horizontalLayoutStates.addWidget(self.statesInput)
        horizontalLayoutStates.addWidget(self.statesButton)

        horizontalLayoutTypes = QtWidgets.QHBoxLayout()
        verticalLayoutButtons.addLayout(horizontalLayoutTypes)
        self.typesInput = QtWidgets.QTextEdit()
        self.typesInput.setFixedWidth(330)
        self.typesButton = QtWidgets.QPushButton(text='Задать типы дуг')
        horizontalLayoutTypes.addWidget(self.typesInput)
        horizontalLayoutTypes.addWidget(self.typesButton)

        horizontalLayoutForbidden = QtWidgets.QHBoxLayout()
        verticalLayoutButtons.addLayout(horizontalLayoutForbidden)
        self.forbiddenInput = QtWidgets.QTextEdit()
        self.forbiddenInput.setFixedWidth(330)
        self.forbiddenButton = QtWidgets.QPushButton(text='Задать запретное состояние')
        horizontalLayoutForbidden.addWidget(self.forbiddenInput)
        horizontalLayoutForbidden.addWidget(self.forbiddenButton)

        horizontalLayoutRenameState = QtWidgets.QHBoxLayout()
        verticalLayoutButtons.addLayout(horizontalLayoutRenameState)
        self.oldStateInput = QtWidgets.QTextEdit()
        self.oldStateInput.setFixedWidth(161)
        self.newStateInput = QtWidgets.QTextEdit()
        self.newStateInput.setFixedWidth(161)
        self.renameStateButton = QtWidgets.QPushButton(text='Переименовать состояние')
        horizontalLayoutRenameState.addWidget(self.oldStateInput)
        horizontalLayoutRenameState.addWidget(self.newStateInput)
        horizontalLayoutRenameState.addWidget(self.renameStateButton)

        horizontalLayoutRenameType = QtWidgets.QHBoxLayout()
        verticalLayoutButtons.addLayout(horizontalLayoutRenameType)
        self.oldTypeInput = QtWidgets.QTextEdit()
        self.oldTypeInput.setFixedWidth(161)
        self.newTypeInput = QtWidgets.QTextEdit()
        self.newTypeInput.setFixedWidth(161)
        self.renameTypeButton = QtWidgets.QPushButton(text='Переименовать тип дуг')
        horizontalLayoutRenameType.addWidget(self.oldTypeInput)
        horizontalLayoutRenameType.addWidget(self.newTypeInput)
        horizontalLayoutRenameType.addWidget(self.renameTypeButton)

        horizontalLayoutSetRule = QtWidgets.QHBoxLayout()
        verticalLayoutButtons.addLayout(horizontalLayoutSetRule)
        self.stateInput = QtWidgets.QTextEdit()
        self.stateInput.setFixedWidth(105)
        self.typeInput = QtWidgets.QTextEdit()
        self.typeInput.setFixedWidth(105)
        self.resultInput = QtWidgets.QTextEdit()
        self.resultInput.setFixedWidth(105)
        self.setRuleButton = QtWidgets.QPushButton(text='Задать правило')
        horizontalLayoutSetRule.addWidget(self.stateInput)
        horizontalLayoutSetRule.addWidget(self.typeInput)
        horizontalLayoutSetRule.addWidget(self.resultInput)
        horizontalLayoutSetRule.addWidget(self.setRuleButton)

    def register_events(self):
        self.open_machine.triggered.connect(self.controller.load_machine)
        self.save_machine.triggered.connect(self.controller.save_machine)
        self.clear_machine.triggered.connect(self.controller.clear)

        self.statesButton.clicked.connect(self.controller.apply_states)
        self.typesButton.clicked.connect(self.controller.apply_types)
        self.forbiddenButton.clicked.connect(self.controller.set_forbidden)
        self.renameStateButton.clicked.connect(self.controller.rename_state)
        self.renameTypeButton.clicked.connect(self.controller.rename_type)
        self.setRuleButton.clicked.connect(self.controller.set_rule)

        self.tableWidget.cellChanged.connect(self.controller.cell_changed)

    def set_table_data(self):
        machine = self.model.machine
        self.tableWidget.cellChanged.disconnect(self.controller.cell_changed)
        for state, rules in machine.rules.items():
            if rules:
                for arc_type, result in rules.items():
                    if result:
                        row = machine.states.index(state)
                        column = machine.types.index(arc_type)
                        self.tableWidget.setItem(row, column, QTableWidgetItem(result))
        self.tableWidget.cellChanged.connect(self.controller.cell_changed)

    def model_is_changed(self):
        # if True:
        try:
            machine = self.model.machine
            self.statesInput.setText(str.join(',', machine.states))
            self.typesInput.setText(str.join(',', machine.types))
            self.forbiddenInput.setText(machine.forbidden)

            self.tableWidget.setRowCount(len(machine.states))
            self.tableWidget.setColumnCount(len(machine.types))
            self.tableWidget.setVerticalHeaderLabels(machine.states)
            self.tableWidget.setHorizontalHeaderLabels(machine.types)

            self.set_table_data()
            self.tableWidget.resizeColumnsToContents()
            self.tableWidget.viewport().update()
            self.update()
        except Exception as e:
            print(e)
