#GUI_draft

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout


class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        btn1 = QPushButton('아메리카노(HOT)', self) #pushbutton #메뉴
        #btn1.clicked.connect(self.showDialog)  #clicked signal -> call

        lbl1 = QLabel('수량', self) #label #수량
        lbl2 = QLabel('0', self) #수량 count

        vbox = QVBoxLayout()
        vbox.addWidget(btn1)
        vbox.addWidget(lbl1)
        vbox.addWidget(lbl2)
        vbox.addStretch() #창 크기가 변화해도 stretch 유지

        self.setLayout(vbox) #수직vertical

        self.setWindowTitle('POS by brilliantOh')
        self.setGeometry(300,300,400,300)
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())