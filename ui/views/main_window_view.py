import networkx as nx
import matplotlib.pyplot as plt

from ui.utils.observer import Observer
from ui.views.main_window import Ui_MainWindow
from PyQt5.QtWidgets import QMainWindow
from ui.utils.window_metaclasses import WrapperAndAbcMeta


class MainWindowView(QMainWindow, Observer, metaclass=WrapperAndAbcMeta):

    def __init__(self, controller, model, parent=None):
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
        self.model_is_changed()

    def model_is_changed(self) -> None:

        if self.model.graph:
            plt.figure('Graph', clear=True)  # также работает доступ через plt.figure(1)
            nx.draw(nx.MultiDiGraph(self.model.graph))
            plt.draw()

        if self.model.layered_graph:
            plt.figure('Layered graph', clear=True)  # аналог - plt.figure(2).clear()
            nx.draw(self.model.layered_graph)
            plt.draw()
