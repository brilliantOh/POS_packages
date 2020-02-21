# GUI_main

# initialize part
from initialize_dev import *

menu_list = [americano, latte, iceamericano, icelatte]

# GUI part
import sys
from PyQt5.QtCore import pyqtSlot, QDateTime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QTabWidget, QListWidget, QListWidgetItem,
                             QPushButton, QLabel, QGroupBox, QInputDialog, QMessageBox,
                             QHBoxLayout, QVBoxLayout, QGridLayout)

# Main
class MyApp(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.title = 'POS_dev'
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(600, 300, 480, 320)

        widget = MyWidget(self)
        self.setCentralWidget(widget)

        self.show()

    # 종료 이벤트
    def closeEvent(self, event):
        reply = QMessageBox.question(self, '종료', 'POS를 종료합니까?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


# Central Widget
class MyWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        # TabWidget call
        tabs = QTabWidget()
        tabs.addTab(FirstTab(), '주문/계산')
        tabs.addTab(SecondTab(), '내역조회')

        vbox = QVBoxLayout()
        vbox.addWidget(tabs)

        self.setLayout(vbox)


# Tab Qwidget: 주문/계산
class FirstTab(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Groupbox call
        grid = QGridLayout()
        grid.addWidget(self.createGB0(), 0, 0)
        grid.addWidget(self.createGB1(), 0, 1)

        self.setLayout(grid)

    # Groupbox: 주문현황
    def createGB0(self):
        gbox = QGroupBox('주문현황')
        hbox = QHBoxLayout()
        vbox = QVBoxLayout()

        # widget 정의
        self.orderlist = []

        self.listwidget = QListWidget()
        self.listwidget.addItems(self.orderlist)
        vbox.addWidget(self.listwidget)

        btn_totcancel = QPushButton('전체취소', self)
        btn_printbill = QPushButton('영수증출력', self)
        hbox.addWidget(btn_printbill)
        hbox.addWidget(btn_totcancel)

        vbox.addLayout(hbox)
        gbox.setLayout(vbox)

        # Signal
        btn_totcancel.clicked.connect(self.totalCancel)

        return gbox


    # Groupbox: 메뉴선택
    def createGB1(self):
        gbox = QGroupBox('메뉴선택')
        vbox = QVBoxLayout()

        # widget list 정의
        btns_menu = []

        # widget 정의 및 추가 for문
        for i in range(len(menu_list)):
            btns_menu.append(QPushButton(menu_list[i].name + '\n'
                                         + str(menu_list[i].cost) + '원', self))
            vbox.addWidget(btns_menu[i])

        # Signal
        btns_menu[0].clicked.connect(lambda: self.menuClicked(0))
        btns_menu[1].clicked.connect(lambda: self.menuClicked(1))
        btns_menu[2].clicked.connect(lambda: self.menuClicked(2))
        btns_menu[3].clicked.connect(lambda: self.menuClicked(3))

        gbox.setLayout(vbox)

        return gbox

    # Slot
    # 주문현황 list에 주문한 메뉴만 있도록
    @pyqtSlot()
    def orderChanged(self):
        # 전체 수량이 0일 경우
        if total.qt == 0:
            self.orderlist = []
            self.listwidget.clear()

        else:
            for i in range(len(menu_list)):
                if menu_list[i].qt != 0:
                    if menu_list[i].name in self.orderlist:
                        pass
                    else:
                        self.orderlist.append(menu_list[i].name)
                        self.listwidget.addItem(self.orderlist[-1])


    # 수량 변경/취소
    @pyqtSlot(int)
    def menuClicked(self, i):
        menu_list[i].menu_qt(1)
        self.orderChanged()

    # 전체취소
    @pyqtSlot()
    def totalCancel(self):
        americano.tot_cancel()
        self.orderChanged()


# Tab Qwidget: 내역조회
class SecondTab(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Groupbox call
        grid = QGridLayout()
        grid.addWidget(self.createGB0(), 0, 0)
        grid.addWidget(self.createGB1(), 0, 1)

        self.setLayout(grid)

    # Groupbox: 주문결제내역
    def createGB0(self):
        gbox = QGroupBox('주문결제내역')


        return gbox

    # Groupbox: 조회
    def createGB1(self):
        gbox = QGroupBox('조회')

        return gbox

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
