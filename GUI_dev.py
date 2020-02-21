# GUI_dev

# initialize part
from initialize_dev import *

menu_list = [americano, latte, iceamericano, icelatte]

# GUI part
import sys
from PyQt5.QtCore import pyqtSlot, Qt, QDateTime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QTabWidget, QTableWidget, QTableWidgetItem,
                             QPushButton, QLabel, QGroupBox, QInputDialog, QMessageBox,
                             QHBoxLayout, QVBoxLayout, QGridLayout)

# Main Window
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


# Tab Widget: 주문/계산
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
        self.table = QTableWidget()
        self.createTable()
        vbox.addWidget(self.table)

        btn_totcancel = QPushButton('전체취소', self)
        btn_printbill = QPushButton('영수증출력', self)
        btn_paycash = QPushButton('현금결제', self)
        btn_paycard = QPushButton('카드결제', self)
        hbox.addWidget(btn_printbill)
        hbox.addWidget(btn_totcancel)
        hbox.addWidget(btn_paycash)
        hbox.addWidget(btn_paycard)

        vbox.addLayout(hbox)
        gbox.setLayout(vbox)

        # Signal
        btn_totcancel.clicked.connect(self.totalCancel)
        btn_printbill.clicked.connect(self.printBill)
        btn_paycash.clicked.connect(self.payCash)
        btn_paycard.clicked.connect(self.payCard)

        return gbox


    # Table Widget: 주문 테이블
    def createTable(self):
        # row, column 정의
        self.table.setColumnCount(6)
        self.table.setRowCount(4)
        self.table.setHorizontalHeaderLabels(['메뉴', '수량', '증가', '감소', '직접입력', '취소'])

    @pyqtSlot()
    def tableSetItem(self):
        # 전체 수량이 0일 경우
        if total.qt == 0:
            self.table.clearContents()
        else:
            for i in range(len(total.order_now_list)):
                self.table.setItem(i, 0, QTableWidgetItem(total.order_now_list[i]))
                #self.table.setItem(i, 1, QTableWidgetItem())


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
    # 수량 변경/취소
    @pyqtSlot(int)
    def menuClicked(self, i):
        menu_list[i].menu_qt(1)
        self.tableSetItem()

    # 전체취소
    @pyqtSlot()
    def totalCancel(self):
        americano.tot_cancel()
        self.tableSetItem()

    # 영수증출력
    @pyqtSlot()
    def printBill(self):
        msg = QMessageBox.information(self, '영수증출력',
                                      str(order.order_df),
                                      QMessageBox.Ok, QMessageBox.Ok)

    # 현금결제
    @pyqtSlot()
    def payCash(self):
        if total.sum == 0:
            self.payZeroWarning()
        else:
            money, ok = QInputDialog.getInt(self, '현금결제',
                                            '결제할 금액: '+ str(total.sum) + '원' + '\n' + \
                                            '받은 금액을 입력하세요.', min=total.sum)
            if ok:
                reply = QMessageBox.question(self, '현금결제: 거스름돈',
                                             '결제할 금액: '+ str(total.sum) + '원' + '\n' + \
                                             '받은 금액: '+ str(money) + '원' + '\n' + \
                                             '거스름돈: ' + str(money-total.sum) + '원' + '\n' + \
                                             '이대로 결제합니까?',
                                             QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
                if reply == QMessageBox.Yes:
                    self.payComplete('현금')

    # 카드결제
    @pyqtSlot()
    def payCard(self):
        if total.sum == 0:
            self.payZeroWarning()
        else:
            reply = QMessageBox.question(self, '카드결제',
                                         '결제할 금액: '+ str(total.sum) + '원' + '\n' + \
                                         '카드로 결제합니까?',
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if reply == QMessageBox.Yes:
                self.payComplete('카드')

    # 결제완료
    @pyqtSlot(str)
    def payComplete(self, method):
        order.orderOccur()

        msg = QMessageBox.information(self, '결제완료',
                                      '결제수단: '+ method + '\n' + \
                                      '결제가 완료되었습니다.',
                                      QMessageBox.Ok, QMessageBox.Ok)
        self.tableSetItem()

    # 결제금액 0원 경고
    @pyqtSlot()
    def payZeroWarning(self):
        msg = QMessageBox.information(self, '결제금액 경고',
                                      '결제금액은 0원일 수 없습니다.',
                                      QMessageBox.Ok, QMessageBox.Ok)


# Tab Widget: 내역조회
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
