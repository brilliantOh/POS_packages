#pyqt_tab2

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QFont

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        tabs = QTabWidget() #tab 위젯 생성
        tabs.addTab(FirstTab(), 'HOT음료')

        vbox = QVBoxLayout()
        vbox.addWidget(tabs)

        self.setLayout(vbox) #box layout

        self.setWindowTitle('POS by brilliantOh')
        self.setWindowIcon(QIcon('image_icon.jpg'))  # icon 불러오기
        self.setGeometry(300,300,400,300)
        self.show()

class FirstTab(QWidget): #HOT음료 tab 정의
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        btn1 = QPushButton('아메리카노(HOT)', self) #pushbutton #메뉴
        btn2 = QPushButton('카페라떼(HOT)', self)

        label1 = QLabel('아메리카노(HOT) 수량') #label(수량)
        label1.setFont(QFont('SansSerif', 10)) #label-font

        vbox = QVBoxLayout()
        vbox.addWidget(btn1)
        vbox.addWidget(btn2)
        vbox.addWidget(label1)
        vbox.addStretch() #창 크기가 변화해도 stretch 유지

        self.setLayout(vbox) #수직vertical


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())