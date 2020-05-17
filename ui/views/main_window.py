from PyQt5 import QtCore, QtWidgets

from ui.views.canvas import MplCanvas
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as Toolbar


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # vertical layout
        self.verticalLayoutMain = QtWidgets.QVBoxLayout()
        self.centralwidget.setLayout(self.verticalLayoutMain)

        # horizontal layout
        self.horizontalLayoutGraphics = QtWidgets.QHBoxLayout()
        self.verticalLayoutMain.addLayout(self.horizontalLayoutGraphics)

        self.frameGraph = QtWidgets.QFrame()
        self.frameGraph.setStyleSheet("background-color: red;")
        self.horizontalLayoutGraphics.addWidget(self.frameGraph)
        self.verticalLayoutGraph = QtWidgets.QVBoxLayout(self.frameGraph)

        self.frameLayeredGraph = QtWidgets.QFrame()
        self.frameLayeredGraph.setStyleSheet("background-color: blue;")
        self.horizontalLayoutGraphics.addWidget(self.frameLayeredGraph)
        self.verticalLayoutLayeredGraph = QtWidgets.QVBoxLayout(self.frameLayeredGraph)

        # canvases
        self.graphCanvas = MplCanvas(plt.figure('Graph'), self.frameGraph)
        self.graph_toolbar = Toolbar(self.graphCanvas, self.frameGraph)
        self.verticalLayoutGraph.addWidget(self.graph_toolbar)
        self.verticalLayoutGraph.addWidget(self.graphCanvas)

        self.layeredGraphCanvas = MplCanvas(plt.figure('Layered graph'), self.frameLayeredGraph)
        self.layered_graph_toolbar = Toolbar(self.layeredGraphCanvas, self.frameLayeredGraph)
        self.verticalLayoutLayeredGraph.addWidget(self.layered_graph_toolbar)
        self.verticalLayoutLayeredGraph.addWidget(self.layeredGraphCanvas)

        # push button
        self.pushButtonToLayered = QtWidgets.QPushButton()
        self.pushButtonToLayered.setMaximumSize(QtCore.QSize(200, 35))
        self.pushButtonToLayered.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.pushButtonToLayered.setObjectName("pushButtonToLayered")
        self.verticalLayoutMain.addWidget(self.pushButtonToLayered, 0, QtCore.Qt.AlignHCenter)
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
        self.open_machine = QtWidgets.QAction(MainWindow)
        self.open_machine.setObjectName("open_machine")
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
        self.menu_open.addAction(self.open_machine)
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
        self.open_machine.setText(_translate("MainWindow", "Автомат"))
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
