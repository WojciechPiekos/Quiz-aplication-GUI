
from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(390, 490)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setStyleSheet("background-color: rgb(170, 170, 255);")
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.scoreLabel = QtWidgets.QLabel(parent=self.centralwidget)
        self.scoreLabel.setGeometry(QtCore.QRect(230, 20, 121, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        self.scoreLabel.setFont(font)
        self.scoreLabel.setStyleSheet("color: rgb(255, 255, 255);")
        self.scoreLabel.setObjectName("scoreLabel")
        self.questionText = QtWidgets.QPlainTextEdit(parent=self.centralwidget)
        self.questionText.setGeometry(QtCore.QRect(30, 70, 331, 221))
        self.questionText.setStyleSheet("background-color: rgb(90, 90, 90);\n"
"color: rgb(255, 255, 255);")
        self.questionText.setReadOnly(True)
        self.questionText.setObjectName("questionText")
        self.buttonOK = QtWidgets.QPushButton(parent=self.centralwidget)
        self.buttonOK.setGeometry(QtCore.QRect(50, 340, 101, 81))
        self.buttonOK.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("images/true.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.buttonOK.setIcon(icon)
        self.buttonOK.setIconSize(QtCore.QSize(100, 100))
        self.buttonOK.setObjectName("buttonOK")
        self.buttonNO = QtWidgets.QPushButton(parent=self.centralwidget)
        self.buttonNO.setGeometry(QtCore.QRect(240, 340, 101, 81))
        self.buttonNO.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("images/false.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.buttonNO.setIcon(icon1)
        self.buttonNO.setIconSize(QtCore.QSize(100, 100))
        self.buttonNO.setObjectName("buttonNO")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 390, 26))
        self.menubar.setObjectName("menubar")
        self.menuGame = QtWidgets.QMenu(parent=self.menubar)
        self.menuGame.setObjectName("menuGame")
        self.menuDifficulty_Level = QtWidgets.QMenu(parent=self.menubar)
        self.menuDifficulty_Level.setObjectName("menuDifficulty_Level")
        self.menuBest_Scores = QtWidgets.QMenu(parent=self.menubar)
        self.menuBest_Scores.setObjectName("menuBest_Scores")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionStart_New_Game = QtGui.QAction(parent=MainWindow)
        self.actionStart_New_Game.setObjectName("actionStart_New_Game")
        self.actionExit = QtGui.QAction(parent=MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionEasy = QtGui.QAction(parent=MainWindow)
        self.actionEasy.setObjectName("actionEasy")
        self.actionMedium = QtGui.QAction(parent=MainWindow)
        self.actionMedium.setObjectName("actionMedium")
        self.actionHard = QtGui.QAction(parent=MainWindow)
        self.actionHard.setObjectName("actionHard")
        self.actionList = QtGui.QAction(parent=MainWindow)
        self.actionList.setObjectName("actionList")
        self.menuGame.addAction(self.actionStart_New_Game)
        self.menuGame.addSeparator()
        self.menuGame.addAction(self.actionExit)
        self.menuDifficulty_Level.addAction(self.actionEasy)
        self.menuDifficulty_Level.addAction(self.actionMedium)
        self.menuDifficulty_Level.addAction(self.actionHard)
        self.menuBest_Scores.addAction(self.actionList)
        self.menubar.addAction(self.menuGame.menuAction())
        self.menubar.addAction(self.menuDifficulty_Level.menuAction())
        self.menubar.addAction(self.menuBest_Scores.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Trivia Quiz"))
        self.scoreLabel.setText(_translate("MainWindow", "Score: "))
        self.menuGame.setTitle(_translate("MainWindow", "Game"))
        self.menuDifficulty_Level.setTitle(_translate("MainWindow", "Difficulty Level"))
        self.menuBest_Scores.setTitle(_translate("MainWindow", "Best Scores"))
        self.actionStart_New_Game.setText(_translate("MainWindow", "Start New Game"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionEasy.setText(_translate("MainWindow", "Easy"))
        self.actionMedium.setText(_translate("MainWindow", "Medium"))
        self.actionHard.setText(_translate("MainWindow", "Hard"))
        self.actionList.setText(_translate("MainWindow", "List"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
