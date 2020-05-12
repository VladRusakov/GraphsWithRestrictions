from ui.utils.model import Observable


class OperateTable(Observable):

    def __init__(self):
        super.__init__()
        self.cayley_table = CayeleyTable()

    @property
    def cayley_table(self):
        return self._cayley_table

    def read_from_file(self):
        self.cayley_table

    def write_to_file(self):
        self.cayley_table
