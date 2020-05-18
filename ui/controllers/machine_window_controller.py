from ui.views.machine_window_view import MachineWindowView


class MachineWindowController:

    def __init__(self, model):
        self.model = model
        self.view = MachineWindowView(self, self.model)  # TODO derive parent window to MachineWindowController as param
        self.view.show()

    def load_machine(self):
        pass

    def save_machine(self):
        pass

    def clear(self):
        pass

    def apply_states(self):
        pass

    def apply_types(self):
        pass

    def set_forbidden(self):
        pass

    def rename_state(self):
        pass

    def rename_type(self):
        pass

    def set_rule(self):
        pass
