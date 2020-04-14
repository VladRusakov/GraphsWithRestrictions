import networkx as nx

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
        self.ui.pushButtonToLayered.clicked.connect(self.controller.perform_graph)
        self.ui.open_graph.triggered.connect(self.controller.open_graph)
        self.ui.open_layered_graph.triggered.connect(self.controller.open_layered_graph)
        self.ui.save_graph.triggered.connect(self.controller.save_graph)
        self.ui.save_layered_graph.triggered.connect(self.controller.save_graph)
        self.update()


    def model_is_changed(self):
        self.update()

    def update(self) -> None:
        nx.draw(nx.cycle_graph(4))
        nx.draw(nx.cycle_graph(5))
