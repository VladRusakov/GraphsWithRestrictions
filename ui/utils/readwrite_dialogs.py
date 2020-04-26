from PyQt5.QtWidgets import QFileDialog, QWidget


def open_file_dialog(dialog_parent: QWidget):
    options = QFileDialog.Options()
    filename, _ = QFileDialog.getOpenFileName(dialog_parent, "Открыть файл", options=options)
    return filename


def save_file_dialog(dialog_parent: QWidget):
    options = QFileDialog.Options()
    filename, _ = QFileDialog.getSaveFileName(dialog_parent, "Сохранить в файл", options=options)
    return filename
