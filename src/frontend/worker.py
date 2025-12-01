from PyQt5.QtCore import QObject, QRunnable, pyqtSignal

class WorkerSignals(QObject):
    finished = pyqtSignal(object)
    error = pyqtSignal(object)


class Worker(QRunnable):

    def __init__(self, func, *args, **kwargs):
        super().__init__()
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

    def run(self):
        try:
            result = self.func(*self.args, **self.kwargs)
            self.signals.finished.emit(result)
        except Exception as e:
            self.signals.error.emit(str(e))
