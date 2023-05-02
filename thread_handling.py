from PyQt6.QtCore import QRunnable,QObject,pyqtSignal,pyqtSlot
import requests

class WorkerSignals(QObject):

    finished = pyqtSignal(str)
    result = pyqtSignal(dict)
    error = pyqtSignal(str)

class Worker(QRunnable):
    def __init__(self,url,params=None):
        super().__init__()
        self.url = url
        self.parameters = params
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        # Pobranie pytania

        try:
            response = requests.get(url=self.url,params=self.parameters)
            data = response.json()

        except Exception as e:
            self.signals.error.emit(str(e))
        else:
            self.signals.result.emit(data)
            self.signals.finished.emit("done")
