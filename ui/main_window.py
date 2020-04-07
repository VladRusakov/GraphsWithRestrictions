# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_window.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1090, 810)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 1091, 751))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayoutWindow = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayoutWindow.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.verticalLayoutWindow.setContentsMargins(0, 0, 0, 0)
        self.verticalLayoutWindow.setObjectName("verticalLayoutWindow")
        self.horizontalLayoutGraphics = QtWidgets.QHBoxLayout()
        self.horizontalLayoutGraphics.setObjectName("horizontalLayoutGraphics")
        self.verticalLayoutWindow.addLayout(self.horizontalLayoutGraphics)
        self.pushButtonToLayered = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButtonToLayered.setMaximumSize(QtCore.QSize(200, 35))
        self.pushButtonToLayered.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.pushButtonToLayered.setObjectName("pushButtonToLayered")
        self.verticalLayoutWindow.addWidget(self.pushButtonToLayered, 0, QtCore.Qt.AlignHCenter)
        MainWindow.setCentralWidget(self.centralwidget)
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
        self.open_layeredgraph = QtWidgets.QAction(MainWindow)
        self.open_layeredgraph.setObjectName("open_layeredgraph")
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
        self.action_12 = QtWidgets.QAction(MainWindow)
        self.action_12.setObjectName("action_12")
        self.menu_open.addAction(self.open_graph)
        self.menu_open.addAction(self.open_layeredgraph)
        self.menu_save.addAction(self.save_graph)
        self.menu_save.addAction(self.save_layered_graph)
        self.menu_tasks.addAction(self.task_dijkstra)
        self.menu_tasks.addAction(self.task_pascal)
        self.menu_tasks.addAction(self.task_random_walk)
        self.menubar.addAction(self.menu_open.menuAction())
        self.menubar.addAction(self.menu_save.menuAction())
        self.menubar.addAction(self.menu_tasks.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButtonToLayered.setText(_translate("MainWindow", "Получить &развёртку графа"))
        self.menu_open.setTitle(_translate("MainWindow", "Открыть"))
        self.menu_save.setTitle(_translate("MainWindow", "Сохранить"))
        self.menu_tasks.setTitle(_translate("MainWindow", "Задача"))
        self.open_graph.setText(_translate("MainWindow", "Граф"))
        self.open_layeredgraph.setText(_translate("MainWindow", "Граф-развёртка"))
        self.save_graph.setText(_translate("MainWindow", "Граф"))
        self.save_layered_graph.setText(_translate("MainWindow", "Граф-развёртку"))
        self.task_dijkstra.setText(_translate("MainWindow", "Алгоритм Дейкстры"))
        self.task_pascal.setText(_translate("MainWindow", "Алгоритм Паскаля"))
        self.task_random_walk.setText(_translate("MainWindow", "Случайные блуждания"))
        self.action_12.setText(_translate("MainWindow", "Потоковая задача"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
