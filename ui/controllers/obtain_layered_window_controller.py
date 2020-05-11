from ui.models.obtain_layered_window_model import ObtainWindowModel
from ui.views.obtain_layered_view import ObtainWindowView


''' форма - наполнение слоя внутри ObtainWindowView
по одной форме на каждую функцию генерации


'''


class ObtainWindowController:
    def __init__(self):
        self.model = ObtainWindowModel()
        self.view = ObtainWindowView(self, self.model)
        self.view.show()

    def change_view(self, name: str) -> None:
        # изменить содержимое Layer'а в ObtainView
        pass

    def get_obtain_params(self):
        # считать и вернуть словарь с параметрами преобразования
        pass
