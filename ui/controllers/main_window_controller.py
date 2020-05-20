from PyQt5.QtWidgets import QMessageBox

from ui.controllers.machine_window_controller import MachineWindowController
from ui.controllers.obtain_layered_window_controller import ObtainWindowController
from ui.models.machine_window_model import MachineWindowModel
from ui.views.main_window_view import MainWindowView
from graph_models.utils import read_graph, save_graph, read_layered_graph, save_layered_graph
from ui.utils.readwrite_dialogs import open_file_dialog, save_file_dialog


class MainWindowController:
    def __init__(self, model):
        self.model = model
        self.view = MainWindowView(self, self.model)
        self.view.show()

    def obtain_graph(self) -> bool:
        graph = self.model.graph
        # if not graph:
        #     QMessageBox.about(self.view, "Ошибка", "Граф не загружен")
        #     return

        try:
            from ui.views.get_data_widgets import LabelAndTextEdit, MachineGetter
            variants = {
                'One': [(LabelAndTextEdit, {'label_text': 'label1', 'result_key': '1', 'result_type': str}),
                        (LabelAndTextEdit, {'label_text': 'label2', 'result_key': '2', 'result_type': str})],
                'Two': [(LabelAndTextEdit, {'label_text': 'label33', 'result_key': '1', 'result_type': str}),
                        (MachineGetter, {'result_key': '2'})]
            }

            def print_callback(**kwargs):
                print(kwargs)

            ObtainWindowController(variants, print_callback)

        except Exception as e:
            print(str(e))

        # obtain_params = self.obtain_window()
        # if not obtain_params:
        #     return
        # method = obtain_params['method']
        # self.model.layered_graph = method(obtain_params['args'])

    def open_graph(self):
        try:
            filename = open_file_dialog(self.view)
            if filename:
                graph = read_graph(filename)
                self.model.graph = graph
        except Exception as e:
            QMessageBox.about(self.view, 'Ошибка', f'Выбранный файл имеет некорректное содержимое или поврежден({e})')

    def open_layered_graph(self):
        try:
            filename = open_file_dialog(self.view)
            if filename:
                layered_graph = read_layered_graph(filename)
                self.model.layered_graph = layered_graph
        except Exception as e:
            QMessageBox.about(self.view, 'Ошибка', f'Выбранный файл имеет некорректное содержимое или поврежден({e})')

    @staticmethod
    def open_machine_window():
        MachineWindowController(MachineWindowModel())

    def save_graph(self):
        if not self.model.graph:
            QMessageBox.about(self.view, 'Ошибка', f'Граф пуст. Нечего сохранять')
            return
        try:
            filename = save_file_dialog(self.view)
            if filename:
                save_graph(self.model.layered_graph, filename)
        except Exception as e:
            QMessageBox.about(self.view, 'Ошибка', f'Не удалось сохранить файл ({e})')

    def save_layered_graph(self):
        if not self.model.layered_graph:
            QMessageBox.about(self.view, 'Ошибка', f'Граф-развёртка пуст. Нечего сохранять')
            return
        try:
            filename = save_file_dialog(self.view)
            if filename:
                save_layered_graph(self.model.layered_graph, filename)
        except Exception as e:
            QMessageBox.about(self.view, 'Ошибка', f'Не удалось сохранить файл  ({e})')
