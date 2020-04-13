from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMessageBox

from ui.Views.main_window_view import MainWindowView


class MainWindowController:
    def __init__(self, model):
        self.model = model
        self.view = MainWindowView(self, self.model)
        self.view.show()

    # def setModelProperty(self):
    #    var x = self.view.ui.textBox1.text()
    #    self.model.x = double(x)
    # и так далее на все изменяемые во view элементы

    def perform_graph(self) -> bool:
        graph = self.model.graph
        method = self.model.method

        if not graph:
            QMessageBox.about(self.view, "Ошибка", "Граф не загружен")
            return
        if not method:
            QMessageBox.about(self.view, "Ошибка", "Не выбран метод преобразования")
            return
        pass

    def open_graph(self):
        import networkx as nx
        #G = nx.dodecahedral_graph()
        import matplotlib.pyplot as plt
        #nx.draw(G)
        #plt.draw()
        #plt.
        #plt.show()

        H = nx.path_graph(4)
        plt.figure(2)
        nx.draw(H)

        G = nx.cycle_graph(4)
        plt.figure(1)
        nx.draw(G)

        plt.show()

        print("OPEN GRAPH")

    def open_layered_graph(self):
        print("OPEN LAYERED GRAPH")

    def save_graph(self):
        print("Save GRAPH")

    def save_layered_graph(self):
        print("save layered")
