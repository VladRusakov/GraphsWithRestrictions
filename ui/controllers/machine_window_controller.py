from typing import List
from PyQt5.QtWidgets import QMessageBox

from ui.models.machine_window_model import MachineWindowModel
from ui.views.machine_window_view import MachineWindowView
from ui.utils.readwrite_dialogs import save_file_dialog, open_file_dialog


class MachineWindowController:

    def __init__(self, model: MachineWindowModel):
        self.model = model
        self.view = MachineWindowView(self, self.model)  # TODO derive parent window to MachineWindowController as param

    def load_machine(self):
        try:
            filename = open_file_dialog(self.view)
            if filename:
                self.model.read_machine(filename)
        except Exception as e:
            QMessageBox.about(self.view, 'Ошибка', f'Выбранный файл имеет некорректное содержимое ({str(e)})')

    def save_machine(self):
        try:
            filename = save_file_dialog(self.view)
            if filename:
                self.model.save_machine(filename)
        except Exception as e:
            QMessageBox.about(self.view, 'Ошибка', f'Не удалось сохранить файл. ({e})')

    def clear(self):
        self.model.clear_machine()

    def apply_states(self):
        new_states = get_list_srtings(self.view.statesInput.toPlainText())
        self.model.update_states(new_states)

    def apply_types(self):
        new_types = get_list_srtings(self.view.typesInput.toPlainText())
        self.model.update_types(new_types)

    def set_forbidden(self):
        new_forbidden = self.view.forbiddenInput.toPlainText().strip()
        if new_forbidden:
            self.model.update_forbidden(new_forbidden)
        else:
            QMessageBox.about(self.view, "Ошибка", "Имя нового запретного состояния пусто")
            self.view.forbiddenInput.setText(self.model.machine.forbidden)

    def rename_state(self):
        old_state = self.view.oldStateInput.toPlainText().strip()
        if old_state not in self.model.machine.states:
            QMessageBox.about(self.view, "Ошибка", "Заменяемое состояние отсутствует")
            return
        new_state = self.view.newStateInput.toPlainText().strip()
        if new_state:
            self.model.rename_state(old_state, new_state)

    def rename_type(self):
        old_type = self.view.oldTypeInput.toPlainText().strip()
        if old_type not in self.model.machine.types:
            QMessageBox.about(self.view, "Ошибка", "Заменяемый тип дуг отсутствует")
            return
        new_type = self.view.newTypeInput.toPlainText().strip()
        if new_type:
            self.model.rename_type(old_type, new_type)

    def set_rule(self):
        state = self.view.stateInput.toPlainText().strip()
        arc_type = self.view.typeInput.toPlainText().strip()
        result = self.view.resultInput.toPlainText().strip()
        machine = self.model.machine
        if ((result in machine.states or result == machine.forbidden) and
                state in machine.states and arc_type in machine.types):
            self.model.set_rule(state, arc_type, result)
        else:
            QMessageBox.about(self.view, "Ошибка", "Неверно заданы: состояние, тип дуг или результат")

    def cell_changed(self, row, column):
        item = self.view.tableWidget.item(row, column)
        result = item.text().strip()
        machine = self.model.machine
        if result in machine.states or result == machine.forbidden:
            state = machine.states[row]
            arc_type = machine.types[column]
            self.model.set_rule(state, arc_type, result)
        else:
            QMessageBox.about(self.view, "Ошибка", f"Неверный результат преобразования: {item.text()}")
            item.setText(machine.forbidden)


def get_list_srtings(string: str) -> List[str]:
    import re
    return list((re.sub('[\{\}\[\]:]', '', string.replace(' ', '')).split(',')))
