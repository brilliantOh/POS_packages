# test

class Tempclass:
    def __init__(self):
        self.att1 = 0
        self.att2 = self.att1 * 10

    def attplus(self):
        self.att1 += 1
        self.att2 = self.att1 * 10

    def attminus(self):
        self.att1 -= 1
        self.att2 = self.att1 * 10

temp = Tempclass()


#GUI

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout

class MyApp(QWidget):
    def __init__(self):
        super().__init__()  # 기반 class의 __init__ call
        self.initUI()

    def initUI(self):
        self.btn1 = QPushButton('btn1', self)
        self.lbl1 = QLabel(str(temp.att1), self)
        self.btn2 = QPushButton('btn2', self)
        self.lbl2 = QLabel(str(temp.att2), self)

        vbox = QVBoxLayout()
        vbox.addWidget(self.btn1)
        vbox.addWidget(self.lbl1)
        vbox.addWidget(self.btn2)
        vbox.addWidget(self.lbl2)
        self.setLayout(vbox)

        self.btn1.clicked.connect(lambda: self.btn1click())
        self.btn2.clicked.connect(lambda: self.btn2click())

        self.show()

    def btn1click(self):
        temp.attplus()
        self.lbltxtchanged()

    def btn2click(self):
        temp.attminus()
        self.lbltxtchanged()

    def lbltxtchanged(self):
        self.lbl1.setText(str(temp.att1))
        self.lbl2.setText(str(temp.att2))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())