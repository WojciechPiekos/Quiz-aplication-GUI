import sys
import requests
import random
import html
from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import QRunnable,QObject,QThreadPool,pyqtSignal,pyqtSlot,QTimer

from MainWindow import Ui_MainWindow

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
        finally:
            self.signals.finished.emit("done")

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.setStyleSheet(".MainWindow {background: #333333;}")
        self.actionExit.triggered.connect(QtWidgets.QApplication.quit)
        self.actionStart_New_Game.triggered.connect(self.new_game)
        self.parameters = {
            'amount' : '1',
            'category' : '18',
            'difficulty' : 'easy',
            'type' : 'boolean'
        }
        self.categories = {}
        self.data_dict = {}
        self.name = ''
        self.score = 0

        self.timer = QTimer(self)
        

        self.actionMedium.triggered.connect(lambda: self.difficult_level('medium'))
        self.actionEasy.triggered.connect(lambda: self.difficult_level('easy'))
        self.actionHard.triggered.connect(lambda: self.difficult_level('medium'))
        self.buttonOK.clicked.connect(lambda: self.game_logic("True"))
        self.buttonNO.clicked.connect(lambda: self.game_logic("False"))

        self.threadpool = QThreadPool()
        self.category_request()
        


    def difficult_level(self,level):
        
        if level == 'medium':
            self.parameters['difficulty'] = 'medium'
        if level == 'easy':
            self.parameters['difficulty'] = 'easy'
        

    def request_question(self):

        api_url = "https://opentdb.com/api.php"

        worker = Worker(api_url,self.parameters)
        worker.signals.result.connect(self.prepare_data)
        worker.signals.finished.connect(self.finished)
        self.threadpool.start(worker)

    
    def category_request(self):

        url = 'https://opentdb.com/api_category.php'

        worker = Worker(url)
        worker.signals.result.connect(self.set_category)
        self.threadpool.start(worker)


    def set_category(self,data):
        self.categories = data


    def prepare_data(self,data):

        if data['results']:
            self.data_dict['question'] = (data['results'][0]['category'],
                                          html.unescape(data['results'][0]['question']),
                                          data['results'][0]['correct_answer'])
            
            print(data['results'][0]['correct_answer'])
               

    def finished(self,str):

        self.questionText.setStyleSheet("background-color: rgb(90, 90, 90);\n"
                                        "color: rgb(255, 255, 255);")
        
        self.questionText.setPlainText(f"Category: {self.name}\n\n{self.data_dict['question'][1]}")

    def random_categorie(self):

        # Losowanie kategorii
        self.labelDifficultLevel.setText(f"Level: {self.parameters['difficulty'].capitalize()}")
        categorie = random.choice(self.categories["trivia_categories"])
        self.parameters['category'] = categorie['id']
        self.name = categorie['name']

        self.request_question()

    def new_game(self):

        if self.categories:
            self.start_game()
        

    def start_game(self):

        self.random_categorie()
        self.score = 0
        self.game_logic()


    def game_logic(self,data=None):

        self.scoreLabel.setText(f'Score: {str(self.score)}')
        if data:
            answer = self.data_dict['question'][2]
            print(data)
            if answer == data:
                self.score += 1
                self.scoreLabel.setText(f'Score: {str(self.score)}')
                self.questionText.setStyleSheet("background-color: green;")
                self.timer.singleShot(500,self.random_categorie)
                self.questionText.setPlainText("\n\n\n\n                Good Answer")
            else:
                self.questionText.setStyleSheet("background-color: red;")
                self.timer.singleShot(500,self.random_categorie)
                self.questionText.setPlainText("\n\n\n\n                Bad Answer")















app = QtWidgets.QApplication(sys.argv)

window = MainWindow()
window.show()
app.exec()