#pyqt_groupbox

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGroupBox, QPushButton, QLabel, \
    QMenu, QGridLayout, QVBoxLayout, QHBoxLayout

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        grid = QGridLayout()
        grid.addWidget(self.create1Groupbox(),0,0)
        grid.addWidget(self.create2Groupbox(),0,1)
        grid.addWidget(self.create3Groupbox(),1,0)
        grid.addWidget(self.create4Groupbox(),1,1)

        self.setLayout(grid)

        self.setWindowTitle('POS by brilliantOh')
        self.setGeometry(300,300,480,320)
        self.show()

    def create1Groupbox(self):
        bx = QGroupBox('HOT음료')

        btn1 = QPushButton('아메리카노(HOT)')
        btn2 = QPushButton('카페라떼(HOT)')

        hbox = QHBoxLayout()
        hbox.addWidget(btn1)
        hbox.addWidget(btn2)
        bx.setLayout(hbox)

        return bx

    def create2Groupbox(self):
        bx = QGroupBox('주문현황')

        lbl1 = QLabel('아메리카노(HOT)')
        lbl2 = QLabel('카페라떼(HOT)')

        vbox = QVBoxLayout()
        vbox.addWidget(lbl1)
        vbox.addWidget(lbl2)
        bx.setLayout(vbox)

        return bx

    def create3Groupbox(self):
        bx = QGroupBox('Qmenu test')

        popupbtn = QPushButton('popup button')
        menu = QMenu(self)
        menu.addAction('act 1')
        menu.addAction('act 2')
        popupbtn.setMenu(menu)

        vbox = QVBoxLayout()
        vbox.addWidget(popupbtn)
        bx.setLayout(vbox)

        return bx

    def create4Groupbox(self):
        bx = QGroupBox('4th group')

        return bx


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())