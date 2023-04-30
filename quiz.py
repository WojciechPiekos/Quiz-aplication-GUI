import sys
import requests
from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import QRunnable,QObject,QThreadPool,pyqtSignal,pyqtSlot

from MainWindow import Ui_MainWindow

class WorkerSignals(QObject):

    finished = pyqtSignal(str)
    result = pyqtSignal(dict)
    error = pyqtSignal(str)

class Worker(QRunnable):
    def __init__(self,params):
        super().__init__()
        self.parameters = params
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        # Pobranie pytania
        print(self.parameters)
        api_url = "https://opentdb.com/api.php"
        try:
            response = requests.get(api_url,params=self.parameters)
            data = response.json()

        except Exception as e:
            self.signals.error.emit(str(e))
        else:
            self.signals.result.emit(data)
        finally:
            self.signals.finished.emit("done")

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.actionExit.triggered.connect(QtWidgets.QApplication.quit)
        self.actionStart_New_Game.triggered.connect(self.new_game)
        self.parameters = {
            'amount' : '10',
            'category' : '18',
            'difficulty' : 'easy',
            'type' : 'boolean'
        }
        self.actionMedium.triggered.connect(self.difficult_medium)
        self.actionEasy.triggered.connect(self.difficult_easy)
        self.actionHard.triggered.connect(self.difficult_hard)

        self.threadpool = QThreadPool()


    def difficult_medium(self):
        self.parameters['difficulty'] = 'medium'

    
    def difficult_easy(self):
        self.parameters['difficulty'] = 'easy'
        
    
    def difficult_hard(self):
        self.parameters['difficulty'] = 'medium'

    def print_data(self,data):
        print(data)


    def new_game(self):
        worker = Worker(self.parameters)
        worker.signals.result.connect(self.print_data)
        self.threadpool.start(worker)




app = QtWidgets.QApplication(sys.argv)

window = MainWindow()
window.show()
app.exec()