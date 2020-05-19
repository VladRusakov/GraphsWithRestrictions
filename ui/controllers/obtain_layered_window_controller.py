from typing import List, Dict, Any
from PyQt5.QtWidgets import QWidget, QMessageBox
from ui.views.obtain_layered_view import ObtainWindowView


class ObtainWindowController:
    def __init__(self, variants: Dict[str, List[Any]]):
        self.variants = variants
        self.current_variant = None
        self.view = ObtainWindowView(self, list(self.variants.keys()))

    def set_variant_widgets(self, variant: str, parent: QWidget):
        for data_getter in self.variants[variant]:
            data_getter[0](parent=parent, **data_getter[1])

    def get_obtain_params(self):
        try:
            pass
        # считать и вернуть словарь с параметрами преобразования
        except Exception as e:
            QMessageBox.about("Ошибка", str(e))
