from typing import Dict

from PyQt5.QtWidgets import QMessageBox
from networkx import MultiDiGraph

from graph_generators.functions_restrictions.non_decreasing_magnetism import non_decreasing_magnetism
from graph_generators.functions_restrictions.barrier_restricted import barrier_restricted
from graph_generators.layered_from_machine import generate_layered_graph
from graph_models.utils import read_graph, save_graph, read_layered_graph, save_layered_graph
from common_algorithms.bfs import breadth_first
from common_algorithms.dfs import depth_first_has_cycle
from common_algorithms.dijkstra import calculate_dijkstra
from common_algorithms.pascal import pascal_for_layered
from ui.controllers.machine_window_controller import MachineWindowController
from ui.controllers.obtain_layered_window_controller import ObtainWindowController
from ui.models.machine_window_model import MachineWindowModel
from ui.views.main_window_view import MainWindowView
from ui.utils.readwrite_dialogs import open_file_dialog, save_file_dialog
from ui.views.get_data_widgets import LabelAndTextEdit, MachineGetter, LabelAndTextEditListInt

obtain_variants = {
    'Неубывающая магнитность':
        [(LabelAndTextEdit, {'label_text': 'Уровень магнитности k', 'result_key': 'k', 'result_type': int})],
    'Барьерная достижимость':
        [(LabelAndTextEdit, {'label_text': 'Барьерный уровень k', 'result_key': 'k', 'result_type': int})],
    'Автоматное описание достижимости': [(MachineGetter, {'result_key': 'machine'})]
}
obtain_functions = {
    'Неубывающая магнитность': non_decreasing_magnetism,
    'Барьерная достижимость': barrier_restricted,
    'Автоматное описание достижимости': generate_layered_graph
}

perform_variants = {
    'Поиск в ширину':
        [(LabelAndTextEdit, {'label_text': 'Начальная вершина (на развёртке)', 'result_key': 'source',
                             'result_type': int})],
    'Поиск в глубину (проверка на ацикличность дерева поиска из вершины)':
        [(LabelAndTextEdit, {'label_text': 'Начальная вершина (на развёртке)', 'result_key': 'source',
                             'result_type': int})],
    'Алгоритм Дейкстры':
        [(LabelAndTextEdit, {'label_text': 'Начальная вершина (на развёртке)', 'result_key': 'source',
                             'result_type': int})],
    'Алгоритм Паскаля':
        [(LabelAndTextEditListInt, {'label_text': 'Начальные вершины (на развёртке)', 'result_key': 'sources'}),
         (LabelAndTextEdit, {'label_text': 'Глубина обхода (0, если неограниченно)', 'result_key': 'max_path',
                             'result_type': int})]
}


def breadth_first_result(tree: MultiDiGraph, not_truncated: MultiDiGraph) -> str:
    return f"Результат поиска в глубину.\n" \
        f"Усеченное дерево: узлы = {tree.nodes}, дуги = {tree.edges(keys=False)}\n" \
        f"Исходное дерево: узлы = {not_truncated.nodes}, дуги = {not_truncated.edges(keys=False)}"


def depth_first_has_cycle_result(has_cycle: bool, cycle_nodes) -> str:
    answer = "имеет циклы" if has_cycle else "не имеет циклов"
    return "Дерево обхода в глубину из заданной вершины " + answer


def calculate_dijkstra_result(tree: MultiDiGraph, not_truncated: MultiDiGraph) -> str:
    return f"Кратчайшие пути на развёртке из заданной вершины:\n" \
        f"Усеченное дерево: узлы = {tree.nodes}, дуги = {tree.edges(keys=False, data=True)}\n" \
        f"Исходное дерево: узлы = {not_truncated.nodes}, дуги = {not_truncated.edges(keys=False, data=True)}"


def pascal_for_layered_result(paths_on_origin: Dict[int, int], paths_on_layered: Dict[int, int]) -> str:
    return f"Число путей во все вершины из заданных:\n" \
        f"На исходном графе: {paths_on_origin}\n" \
        f"На вспомогательном: {paths_on_layered}"


perform_functions = {
    'Поиск в ширину': [breadth_first, breadth_first_result],
    'Поиск в глубину (проверка на ацикличность дерева поиска из вершины)': [depth_first_has_cycle,
                                                                            depth_first_has_cycle_result],
    'Алгоритм Дейкстры': [calculate_dijkstra, calculate_dijkstra_result],
    'Алгоритм Паскаля': [pascal_for_layered, pascal_for_layered_result]
}


class MainWindowController:
    def __init__(self, model):
        self.model = model
        self.view = MainWindowView(self, self.model)
        self.view.show()
        graph = read_graph('../data/image2.txt')  # TODO remove hardcode
        self.model.graph = graph
        layered_graph = read_layered_graph('../data/image2_layered.txt')  # TODO remove hardcode
        self.model.layered_graph = layered_graph

    def obtain_graph(self) -> bool:
        graph = self.model.graph
        if not graph:
            QMessageBox.about(self.view, "Ошибка", "Граф не загружен")
            return

        try:
            def obtain_layered_graph(variant, **kwargs):
                self.model.layered_graph = obtain_functions[variant](graph=graph, **kwargs)

            ObtainWindowController(obtain_variants, obtain_layered_graph)

        except Exception as e:
            print(str(e))

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

    def perform_task(self):
        graph = self.model.graph
        layered_graph = self.model.layered_graph
        if not graph:
            QMessageBox.about(self.view, "Ошибка", "Граф не загружен")
            return
        if not layered_graph:
            QMessageBox.about(self.view, "Ошибка", "Вспомогательный граф не загружен")
            return
        try:
            def perform_task(variant, **kwargs):
                kwargs.update({'layered_graph': layered_graph})
                function = perform_functions[variant][0]
                if 'graph' in function.__code__.co_varnames:
                    kwargs.update({'graph': graph})
                answer = function(**kwargs)
                self.view.set_answer_text(perform_functions[variant][1](*answer))

            ObtainWindowController(perform_variants, perform_task)

        except Exception as e:
            print(str(e))
