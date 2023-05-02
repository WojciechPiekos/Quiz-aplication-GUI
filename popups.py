from PyQt6.QtWidgets import QDialog, QDialogButtonBox, QMessageBox, QVBoxLayout,QLabel
from PyQt6.QtGui import QPixmap

class Dialog(QDialog):
    def __init__(self,title,url=None,body=None):
        super().__init__()
        self.title = title
        self.url = url
        self.body = body

        self.setWindowTitle(self.title)
        self.resize(250,300)
        self.setStyleSheet("background: #333333; color: white; ")
        
        self.layout = QVBoxLayout()
        if url:
            self.image = QLabel()
            self.image.setPixmap(QPixmap(self.url))
        if body:
            self.message = QLabel(self.body)


    def add_widgets_to_layout(self, widget = None, button = None):

        if button:
            buttons = (button | QDialogButtonBox.StandardButton.Close)
            self.buttonBox = QDialogButtonBox(buttons)
            self.buttonBox.accepted.connect(self.accept)
            self.buttonBox.rejected.connect(self.reject)
        else:
            buttons = (QDialogButtonBox.StandardButton.Close)
            self.buttonBox = QDialogButtonBox(buttons)
            self.buttonBox.rejected.connect(self.reject)
        
        if self.url:
            self.layout.addWidget(self.image)
        
        if self.body:
            self.layout.addWidget(self.message)
        
        if widget:
            self.layout.addWidget(widget)
        
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)
        

class Messages(QMessageBox):
    def __init__(self, title, text, icon):
        super().__init__()
        self.title = title
        self.text = text
        self.icon = icon
        self.setWindowTitle(title)
        self.setText(text)
        self.setIcon(icon)
        self.setStyleSheet("background: #333333; color: white")

