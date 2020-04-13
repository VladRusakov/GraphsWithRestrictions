from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QScrollArea

from ui.Views.canvas import MplCanvas
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as Toolbar

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # expanding area
        self.area = QScrollArea(self.centralwidget)
        self.area.setWidgetResizable(True)

        # vertical layout
        self.verticalLayoutWidget = QtWidgets.QVBoxLayout()
        self.centralwidget.setLayout(self.verticalLayoutWidget)
        self.verticalLayoutWidget.addWidget(self.area)

        # horizontal layout
        self.horizontalLayoutGraphics = QtWidgets.QHBoxLayout()
        self.horizontalLayoutGraphics.setObjectName("horizontalLayoutGraphics")
        self.verticalLayoutWidget.addLayout(self.horizontalLayoutGraphics)



        # canvases
        self.figure_graph = plt.figure(1)
        #nx.draw(G)
        self.graphCanvas = MplCanvas(self.figure_graph)
        self.graph_toolbar = Toolbar(self.graphCanvas, self.centralwidget)
        #G2 = nx.cycle_graph(5)
        self.figure_layred_graph = plt.figure(2)
        #nx.draw(G2)
        self.layeredGraphCanvas = MplCanvas(self.figure_layred_graph)
        self.layered_graph_toolbar = Toolbar(self.layeredGraphCanvas, self.centralwidget)
        self.horizontalLayoutGraphics.addWidget(self.graphCanvas)
        self.horizontalLayoutGraphics.addWidget(self.layeredGraphCanvas)
        self.verticalLayoutWidget.addWidget(self.graph_toolbar)
        self.verticalLayoutWidget.addWidget(self.layered_graph_toolbar)

        self.scrollAreaWidgetContents = self.layeredGraphCanvas
        self.area.setWidget(self.scrollAreaWidgetContents)

        # push button
        self.pushButtonToLayered = QtWidgets.QPushButton()
        self.pushButtonToLayered.setMaximumSize(QtCore.QSize(200, 35))
        self.pushButtonToLayered.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.pushButtonToLayered.setObjectName("pushButtonToLayered")
        self.verticalLayoutWidget.addWidget(self.pushButtonToLayered, 0, QtCore.Qt.AlignHCenter)
        MainWindow.setCentralWidget(self.centralwidget)

        # menus
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1090, 26))
        self.menubar.setObjectName("menubar")
        self.menu_open = QtWidgets.QMenu(self.menubar)
        self.menu_open.setObjectName("menu_open")
        self.menu_save = QtWidgets.QMenu(self.menubar)
        self.menu_save.setObjectName("menu_save")
        self.menu_tasks = QtWidgets.QMenu(self.menubar)
        self.menu_tasks.setObjectName("menu_tasks")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.open_graph = QtWidgets.QAction(MainWindow)
        self.open_graph.setObjectName("open_graph")
        self.open_layered_graph = QtWidgets.QAction(MainWindow)
        self.open_layered_graph.setObjectName("open_layered_graph")
        self.save_graph = QtWidgets.QAction(MainWindow)
        self.save_graph.setObjectName("save_graph")
        self.save_layered_graph = QtWidgets.QAction(MainWindow)
        self.save_layered_graph.setObjectName("save_layered_graph")
        self.task_dijkstra = QtWidgets.QAction(MainWindow)
        self.task_dijkstra.setObjectName("task_dijkstra")
        self.task_pascal = QtWidgets.QAction(MainWindow)
        self.task_pascal.setObjectName("task_pascal")
        self.task_random_walk = QtWidgets.QAction(MainWindow)
        self.task_random_walk.setObjectName("task_random_walk")
        self.task_max_flow = QtWidgets.QAction(MainWindow)
        self.task_max_flow.setObjectName("task_max_flow")
        self.menu_open.addAction(self.open_graph)
        self.menu_open.addAction(self.open_layered_graph)
        self.menu_save.addAction(self.save_graph)
        self.menu_save.addAction(self.save_layered_graph)
        self.menu_tasks.addAction(self.task_dijkstra)
        self.menu_tasks.addAction(self.task_pascal)
        self.menu_tasks.addAction(self.task_random_walk)
        self.menu_tasks.addAction(self.task_max_flow)
        self.menubar.addAction(self.menu_open.menuAction())
        self.menubar.addAction(self.menu_save.menuAction())
        self.menubar.addAction(self.menu_tasks.menuAction())


        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Графы с нестандартной достижимостью"))
        self.pushButtonToLayered.setText(_translate("MainWindow", "Получить &развёртку графа"))
        self.menu_open.setTitle(_translate("MainWindow", "Открыть"))
        self.menu_save.setTitle(_translate("MainWindow", "Сохранить"))
        self.menu_tasks.setTitle(_translate("MainWindow", "Задача"))
        self.open_graph.setText(_translate("MainWindow", "Граф"))
        self.open_layered_graph.setText(_translate("MainWindow", "Граф-развёртку"))
        self.save_graph.setText(_translate("MainWindow", "Граф"))
        self.save_layered_graph.setText(_translate("MainWindow", "Граф-развёртку"))
        self.task_dijkstra.setText(_translate("MainWindow", "Алгоритм Дейкстры"))
        self.task_pascal.setText(_translate("MainWindow", "Алгоритм Паскаля"))
        self.task_random_walk.setText(_translate("MainWindow", "Случайные блуждания"))
        self.task_max_flow.setText(_translate("MainWindow", "Потоковая задача"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
