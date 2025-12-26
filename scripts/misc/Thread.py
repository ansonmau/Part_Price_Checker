import threading 
from PySide6.QtCore import QObject, QThread, Signal, Slot
from scripts.misc.Log import MyLogger

logger = MyLogger(__name__)

class Worker(QObject):
    started = Signal()
    finished = Signal()

    def __init__(self):
        super().__init__()

    def set_exec_fnc(self, fnc):
        self.exec = fnc

    def run(self):
        assert self.exec
        self.exec()
        self.finished.emit()

class Thread():
    def __init__(self):
        self.thread = QThread()
        self.thread.finished.connect(self.thread.deleteLater)

    def attach_worker(self, worker: Worker):
        self.worker = worker
        self.worker.moveToThread(self.thread)
        self.worker.finished.connect(self.worker.deleteLater)
        self.worker.finished.connect(self.thread.quit)
        self.thread.started.connect(self.worker.run)

    def start(self):
        self.thread.start()
        


