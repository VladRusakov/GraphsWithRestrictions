from abc import ABCMeta
from PyQt5 import QtCore


class WrapperAndAbcMeta(type(QtCore.QObject), ABCMeta):
    pass
