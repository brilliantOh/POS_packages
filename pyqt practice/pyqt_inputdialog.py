#pyqt_dialog

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QInputDialog

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.btn = QPushButton('근무자 log-in', self) #pushbutton
        self.btn.move(30,30)
        self.btn.clicked.connect(self.showDialog) #clicked signal->showDialog call

        self.le = QLineEdit(self) #lineedit
        self.le.move(120,30)

        self.setWindowTitle('근무자관리')
        self.setGeometry(300,300,300,200)
        self.show()

    def showDialog(self): #pushbutton click->dialog
        text, ok = QInputDialog.getText(self, 'log-in dialog', '근무자ID:') #title, text 표시

        if ok:
            self.le.setText(str(text)) #입력시 입력한 text line에 표시

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())