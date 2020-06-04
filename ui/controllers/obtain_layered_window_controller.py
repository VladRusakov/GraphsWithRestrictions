from typing import List, Dict, Any, Callable
from PyQt5.QtWidgets import QWidget, QMessageBox

from ui.views.get_data_widgets import DataGetter
from ui.views.obtain_layered_view import ObtainWindowView


class ObtainWindowController:
    def __init__(self, variants: Dict[str, List[Any]], obtain_callback: Callable = None):
        self.variants = variants
        self.current_data_getters: List[DataGetter] = None
        self.current_variant: str = None
        self.view = ObtainWindowView(self, list(self.variants.keys()))
        self.obtain_callback = obtain_callback

    def set_variant_widgets(self, variant: str, parent: QWidget):
        self.current_variant = variant
        self.current_data_getters = []
        for data_getter in self.variants[variant]:
            self.current_data_getters.append(data_getter[0](parent=parent, **data_getter[1]))

    def gather_data_from_getters(self):
        params = {}
        try:
            for data_getter in self.current_data_getters:
                key, value = data_getter.get_data()
                params[key] = value
        except Exception as e:  # TODO specify exception
            QMessageBox.about(self.view, "Неправильный ввод данных:", str(e))
        else:
            self.obtain_callback(self.current_variant, **params)
            self.view.close()
