from ui.utils.model import AbstractModel


class ObtainWindowModel(AbstractModel):

    methods_forms = {
        ''
    }

    def __init__(self):
        super().__init__()
        self.methods = {}
        self.current_method = None

    @property
    def current_method(self):
        return self._current_method

    @current_method.setter
    def current_method(self, name):
        if self.methods[name]:
            self._current_method = name
            self.notify_observers()
