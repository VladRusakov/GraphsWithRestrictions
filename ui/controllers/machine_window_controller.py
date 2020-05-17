from ui.views.machine_window_view import MachineWindowView


class MachineWindowController:

    def __init__(self, model):
        self.model = model
        self.view = MachineWindowView(self, self.model)  # TODO derive parent window to MachineWindowController as param
        self.view.show()
