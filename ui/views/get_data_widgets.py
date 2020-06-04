from abc import ABC, abstractmethod
from typing import Tuple, Any, List

from PyQt5.QtWidgets import QLabel, QTextEdit, QWidget, QHBoxLayout, QLayout, QPushButton

from graph_models.state_machine import StateMachine


class DataGetter(ABC):
    @abstractmethod
    def get_data(self) -> Tuple[str, Any]:
        pass


class LabelAndTextEdit(DataGetter):

    def __init__(self, label_text: str, result_key: str, parent: QWidget, result_type: type = str):
        self.label = QLabel(text=label_text, parent=parent)
        self.text_edit = QTextEdit(parent=parent)
        self.text_edit.setMaximumHeight(40)
        horizontal_layer = QHBoxLayout()
        horizontal_layer.addWidget(self.label)
        horizontal_layer.addWidget(self.text_edit)
        parent.layout().addLayout(horizontal_layer)
        self.key = result_key
        self.result_type = result_type

    def get_data(self) -> Tuple[str, Any]:
        # TODO делать проверку валидности полей и бросать исключения
        return self.key, self.result_type(self.text_edit.toPlainText().strip())


class LabelAndTextEditListInt(LabelAndTextEdit):
    def get_data(self) -> Tuple[str, List[int]]:
        return self.key, [int(val) for val in self.text_edit.toPlainText().strip().split(',')]


class MachineGetter(DataGetter):

    def __init__(self, result_key: str, parent: QWidget):
        self.button = QPushButton(text='Открыть автомат', parent=parent)
        self.button.clicked.connect(self.set_machine_path)
        self.text_edit = QTextEdit(parent=parent)
        self.text_edit.setMaximumHeight(100)
        horizontal_layer = QHBoxLayout()
        horizontal_layer.addWidget(self.button)
        horizontal_layer.addWidget(self.text_edit)
        parent.layout().addLayout(horizontal_layer)
        self.key = result_key

    def get_data(self) -> Tuple[str, StateMachine]:
        file_path = self.text_edit.toPlainText().strip()
        from ui.models.machine_window_model import read_machine_from_file
        machine = read_machine_from_file(file_path)
        return self.key, machine

    def set_machine_path(self) -> None:
        from ui.utils.readwrite_dialogs import open_file_dialog
        filename = open_file_dialog(None)
        self.text_edit.setPlainText(filename)
