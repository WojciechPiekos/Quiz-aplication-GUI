import sys
import random
import html
from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import QThreadPool,QTimer
from database_service import BestScore
from popups import Messages, Dialog
from thread_handling import Worker
from MainWindow import Ui_MainWindow


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.setStyleSheet(".MainWindow {background: #333333;}")
        self.actionExit.triggered.connect(QtWidgets.QApplication.quit)
        self.actionStart_New_Game.triggered.connect(self.new_game)
        self.actionHelp.triggered.connect(self.help_window)
        self.actionAbout.triggered.connect(self.about_window)

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
        self.heart = 3
        self.error_flag = False

        self.timer = QTimer(self)
        
        self.actionMedium.triggered.connect(lambda: self.difficult_level('medium'))
        self.actionEasy.triggered.connect(lambda: self.difficult_level('easy'))
        self.actionHard.triggered.connect(lambda: self.difficult_level('medium'))
        self.buttonOK.clicked.connect(lambda: self.game_logic("True"))
        self.buttonNO.clicked.connect(lambda: self.game_logic("False"))

        self.labelDifficultLevel.setText(f"Level: {self.parameters['difficulty'].capitalize()}")

        self.threadpool = QThreadPool()
        self.category_request()
        

    def help_window(self):

        title = "Help"
        url = "images/otje2.jpg"
        body = """
    1. Quiz requires an active internet
        connection.

    2. To start the game, 
        select Game - New Game.

    3. Changing the difficulty 
        level is possible only 
        before starting the game. 
        This can be done in the 
        Difficulty Level menu.

    4. The player starts with 
        three lives, after each 
        wrong answer the player 
        loses one life.

    5. The game ends when the player 
        loses last life
    
        """

        dialog = Dialog(title,url,body)
        dialog.add_widgets_to_layout()
        dialog.exec()

    def about_window(self):
        title = "About"
        url = "images/otje2.jpg"
        body = """
    Author: WojciechP

    Date: 01.05.2023
    
        """

        dialog = Dialog(title,url,body)
        dialog.add_widgets_to_layout()
        dialog.exec()


    def difficult_level(self,level):

        if level == 'medium':
            self.parameters['difficulty'] = 'medium'
            self.labelDifficultLevel.setText(f"Level: {self.parameters['difficulty'].capitalize()}")
        if level == 'easy':
            self.parameters['difficulty'] = 'easy'
            self.labelDifficultLevel.setText(f"Level: {self.parameters['difficulty'].capitalize()}")
        

    def request_question(self):

        api_url = "https://opentdb.com/api.php"

        worker = Worker(api_url,self.parameters)
        worker.signals.result.connect(self.prepare_data)
        worker.signals.finished.connect(self.finished)
        worker.signals.error.connect(self.errors_function)
        self.threadpool.start(worker)

    
    def errors_function(self,err):
        self.error_flag = True
        error = Messages("Opss...Something goes wrong",err,QtWidgets.QMessageBox.Icon.Critical)
        error.exec()
        

    def category_request(self):

        url = 'https://opentdb.com/api_category.php'

        worker = Worker(url)
        worker.signals.result.connect(self.set_category)
        worker.signals.error.connect(self.errors_function)
        self.threadpool.start(worker)


    def set_category(self,data):
        self.categories = data


    def prepare_data(self,data):

        if data['results']:
            self.data_dict['question'] = (data['results'][0]['category'],
                                          html.unescape(data['results'][0]['question']),
                                          data['results'][0]['correct_answer'])
               

    def finished(self,str):

        self.questionText.setStyleSheet("background-color: rgb(90, 90, 90);\n"
                                        "color: rgb(255, 255, 255);")
        
        self.questionText.setPlainText(f"Category: {self.name}\n\n{self.data_dict['question'][1]}")

    def random_categorie(self):

        # Losowanie kategorii
        categorie = random.choice(self.categories["trivia_categories"])
        self.parameters['category'] = categorie['id']
        self.name = categorie['name']

        self.request_question()


    def new_game(self):

        if self.error_flag:
           self.category_request()
           self.error_flag = False
        else: 
            if self.categories:
                self.start_game()
                self.buttonOK.setDisabled(False)
                self.buttonNO.setDisabled(False)
        

    def start_game(self):

        self.random_categorie()
        self.score = 0
        self.heart = 3
        self.actionHard.setDisabled(True)
        self.actionMedium.setDisabled(True)
        self.actionEasy.setDisabled(True)
        self.heart1.setVisible(True)
        self.heart2.setVisible(True)
        self.heart3.setVisible(True)
        self.game_logic()


    def heart_update(self):
        
        if self.heart == 3:
            self.heart -= 1
            self.heart3.setVisible(False)
            parameter = "Continue"
        elif self.heart == 2:
            self.heart -= 1
            self.heart2.setVisible(False)
            parameter = "Continue"
        elif self.heart == 1:
            self.heart -= 1
            self.heart1.setVisible(False)
            parameter = "End of game"
        else:
            parameter = "End of game"
        
        return parameter
        

    def game_logic(self,data=None):

        self.scoreLabel.setText(f'Score: {str(self.score)}')
        if data:
            answer = self.data_dict['question'][2]
            if answer == data:
                self.score += 1
                self.scoreLabel.setText(f'Score: {str(self.score)}')
                self.questionText.setStyleSheet("background-color: green;")
                self.timer.singleShot(500,self.random_categorie)
                self.questionText.setPlainText("\n\n\n\n                Good Answer")
            else:
                self.questionText.setStyleSheet("background-color: red;")
                chances = self.heart_update()
                if chances == "Continue":
                    self.timer.singleShot(500,self.random_categorie)
                    self.questionText.setPlainText("\n\n\n\n                Bad Answer")
                elif chances == "End of game":
                    self.questionText.setPlainText("\n\n\n\n                Game Over")
                    self.actionHard.setDisabled(False)
                    self.actionMedium.setDisabled(False)
                    self.actionEasy.setDisabled(False)
                    self.buttonOK.setDisabled(True)
                    self.buttonNO.setDisabled(True)

                    # Save to database
                    if self.score > 0:
                        save_to_db = self.end_game_messages(title="Save Your Score",
                                                            msg=f"Congrats!!!\nYou Have {self.score} Points\nDo You Want Save Your Score?")
                        
                        if save_to_db:
                            body = "                    Save Your Score "
                            dialog = Dialog("Save To Database","images/otje2.jpg",body=body)
                            frame = QtWidgets.QFrame()
                            layout = QtWidgets.QFormLayout()
                            name = QtWidgets.QLineEdit()
                            layout.addRow("Enter Your Name:",name)
                            frame.setLayout(layout)
                            button = QtWidgets.QDialogButtonBox.StandardButton.Save
                            dialog.add_widgets_to_layout(frame,button)
                            
                            if dialog.exec():
                                connection = BestScore("best_scores.db")
                                connection.add_record(name.text(),self.score)
        
                    # Asking about next game
                    play_agin = self.end_game_messages(title="Play again",
                                                       msg="Do You Want Play Again?")
                    if play_agin:
                        self.new_game()
                    else:
                        return
                    

    def end_game_messages(self,title,msg):

        question = Messages(title,msg,
                            QtWidgets.QMessageBox.Icon.Question)
                    
        question.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes\
                                    | QtWidgets.QMessageBox.StandardButton.No)
                    
        button = question.exec()

        if button == QtWidgets.QMessageBox.StandardButton.Yes:
            return True
        elif button == QtWidgets.QMessageBox.StandardButton.No:
            return False





app = QtWidgets.QApplication(sys.argv)

window = MainWindow()
window.show()
app.exec()