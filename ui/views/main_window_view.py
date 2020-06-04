import networkx as nx
import matplotlib.pyplot as plt

from ui.models.main_window_model import MainWindowModel
from ui.utils.observer import Observer
from ui.views.main_window import Ui_MainWindow
from PyQt5.QtWidgets import QMainWindow
from ui.utils.window_metaclasses import WrapperAndAbcMeta


class MainWindowView(QMainWindow, Observer, metaclass=WrapperAndAbcMeta):

    def __init__(self, controller, model: MainWindowModel, parent=None):
        super(QMainWindow, self).__init__(parent)
        self.controller = controller
        self.model = model

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.model.add_observer(self)

        # регистрация событий/слотов-сигналов
        self.ui.pushButtonToLayered.clicked.connect(self.controller.obtain_graph)
        self.ui.open_graph.triggered.connect(self.controller.open_graph)
        self.ui.open_layered_graph.triggered.connect(self.controller.open_layered_graph)
        self.ui.open_machine.triggered.connect(self.controller.open_machine_window)
        self.ui.save_graph.triggered.connect(self.controller.save_graph)
        self.ui.save_layered_graph.triggered.connect(self.controller.save_layered_graph)
        self.ui.menu_task.triggered.connect(self.controller.perform_task)
        self.model_is_changed()

    def set_answer_text(self, text):
        self.ui.answerTextEdit.setPlainText(text)

    def model_is_changed(self) -> None:

        def get_labels(graph: nx.MultiDiGraph):
            labels = {}
            for data in graph.edges.data():
                labels[data[0], data[1]] = str(list(data[2].values()))
            return labels

        if self.model.graph:
            plt.figure('Graph', clear=True)  # также работает доступ через plt.figure(1)
            graph = self.model.graph
            pos = nx.spring_layout(graph)
            graph.graph['edge'] = {'splines': 'curved'}
            nx.draw(self.model.graph, pos=pos, with_labels=True, node_color='r', connectionstyle='arc3,rad=0.2')
            labels = get_labels(graph)
            nx.draw_networkx_edge_labels(graph, pos=pos, edge_labels=labels)
            plt.draw()

        if self.model.layered_graph:
            plt.figure('Layered graph', clear=True)  # аналог - plt.figure(2).clear()
            offset = 0.3
            pos = []
            graph = self.model.layered_graph
            for y in range(graph.layers):
                for x in range(len(graph.origin_nodes)):
                    pos.append((x*offset, y*offset))
            nx.draw(graph, pos=pos, with_labels=True, connectionstyle='arc3,rad=0.2')
            #labels = get_labels(graph)
            #nx.draw_networkx_edge_labels(graph, pos=pos, edge_labels=labels, label_pos=0.8)
            plt.draw()
