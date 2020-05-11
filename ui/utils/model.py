from abc import ABC


class AbstractModel(ABC):
    def __init__(self):
        self._observers = []

    def add_observer(self, new_observer):
        if new_observer not in self._observers:
            self._observers.append(new_observer)

    def remove_observer(self, removable_observer):
        self._observers.remove(removable_observer)

    def notify_observers(self):
        for observer in self._observers:
            observer.model_is_changed()
