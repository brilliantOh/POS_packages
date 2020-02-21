#GUI_draft

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QInputDialog,\
    QHBoxLayout, QVBoxLayout


class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.menu1_count = 0
        self.btn1 = QPushButton('아메리카노(HOT)', self) #pushbutton #메뉴
        self.btn1.clicked.connect(self.menuClicked)  #clicked signal -> call menuClicked

        self.btn2 = QPushButton('-', self) #수량-
        self.btn2.clicked.connect(self.menuMinus)
        self.btn3 = QPushButton('+', self) #수량+
        self.btn3.clicked.connect(self.menuAdd)

        self.btn4 = QPushButton('직접입력', self) #수량변경
        self.btn4.clicked.connect(self.menuInputDialog)

        self.btn5 = QPushButton('제거', self) #제거
        self.btn5.clicked.connect(self.menuCancel)

        self.lbl1 = QLabel('0', self) #label #수량count #default 0
        self.lbl2 = QLabel('아메리카노(HOT)', self) #주문현황의 메뉴

        hbox = QHBoxLayout() #주문현황 part #HorizentalBox 수평 레이아웃
        hbox.addWidget(self.lbl2)
        hbox.addWidget(self.btn2)
        hbox.addWidget(self.lbl1)
        hbox.addWidget(self.btn3)
        hbox.addWidget(self.btn4)
        hbox.addWidget(self.btn5)

        vbox = QVBoxLayout() #VerticalBox 수직 레이아웃
        vbox.addLayout(hbox)
        vbox.addStretch(1)
        vbox.addWidget(self.btn1) #메뉴 part

        self.setLayout(vbox) #Layout

        self.setWindowTitle('POS by brilliantOh')
        self.setGeometry(300,300,300,200)
        self.show()

    def menuClicked(self):
        self.menu1_count += 1
        self.lbl1.setText(str(self.menu1_count))

    def menuMinus(self):
        self.menu1_count -= 1
        if self.menu1_count < 0:
            self.menu1_count = 0
        self.lbl1.setText(str(self.menu1_count))

    def menuAdd(self): #수량+
        self.menu1_count += 1
        self.lbl1.setText(str(self.menu1_count))

    def menuInputDialog(self): #수량변경
        number, ok = QInputDialog.getInt(self, '수량 직접입력', '수량을 입력하세요.', min=0)

        if ok:
            self.menu1_count = number
            self.lbl1.setText(str(self.menu1_count))

    def menuCancel(self):
        self.menu1_count = 0
        self.lbl1.setText(str(self.menu1_count))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())