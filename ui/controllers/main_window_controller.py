from PyQt5.QtWidgets import QMessageBox
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

        if not graph:
            QMessageBox.about(self.view, "Ошибка", "Граф не загружен")
            return
        obtain_params = self.obtain_window()
        if not obtain_params:
            return
        method = obtain_params['method']
        self.model.layered_graph = method(obtain_params['args'])

    def open_graph(self):
        try:
            filename = open_file_dialog(self.view)
            if filename:
                graph = read_graph(filename)
                self.model.graph = graph
                self.view.update()
        except Exception:
            QMessageBox.about(self.view, 'Ошибка', 'Выбранный файл имеет некорректное содержимое или поврежден')

    def open_layered_graph(self):
        try:
            filename = open_file_dialog(self.view)
            if filename:
                layered_graph = read_layered_graph(filename)
                self.model.layered_graph = layered_graph
                self.view.update()
        except Exception:
            QMessageBox.about(self.view, 'Ошибка', f'Выбранный файл имеет некорректное содержимое или поврежден')

    def save_graph(self):
        if not self.model.graph:
            QMessageBox.about(self.view, 'Ошибка', f'Граф пуст. Нечего сохранять')
            return
        try:
            filename = save_file_dialog(self.view)
            if filename:
                save_graph(self.model.layered_graph, filename)
        except Exception:
            QMessageBox.about(self.view, 'Ошибка', f'Не удалось сохранить файл')

    def save_layered_graph(self):
        if not self.model.layered_graph:
            QMessageBox.about(self.view, 'Ошибка', f'Граф-развёртка пуст. Нечего сохранять')
            return
        try:
            filename = save_file_dialog(self.view)
            if filename:
                save_layered_graph(self.model.layered_graph, filename)
        except Exception:
            QMessageBox.about(self.view, 'Ошибка', f'Не удалось сохранить файл')

    def obtain_window(self):
        pass