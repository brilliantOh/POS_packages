# GUI_dev

# initialize part
from initialize_dev import *

menu_list = [americano, latte, iceamericano, icelatte]

# GUI part
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QGroupBox, QInputDialog, \
    QMessageBox, QVBoxLayout, QGridLayout

class MyApp(QWidget):
    def __init__(self):
        super().__init__()  # 기반 class의 __init__ call
        self.title = 'POS by brilliantOh'
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)  # 창 이름
        self.setGeometry(600, 300, 480, 320)  # 창 size

        grid = QGridLayout()
        grid.addWidget(self.createGB0(), 0, 0)  # groupbox # 주문현황
        grid.addWidget(self.createGB1(), 0, 1)  # groupbox # 메뉴선택

        self.setLayout(grid)  # gridlayout

        self.show()  # 그리기

    # 종료 이벤트
    def closeEvent(self, event):
        reply = QMessageBox.question(self, '종료', 'POS를 종료합니까?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def createGB0(self):  # 주문현황 #grid:(0,0)
        gbox = QGroupBox('주문현황')
        grid = QGridLayout()  # gridlayout

        # widget list 정의
        self.lbls_menu = []
        self.lbls_qt = []
        self.btns_minus = []
        self.btns_add = []
        self.btns_cancel = []
        self.btns_input = []
        self.lbls_tot = []

        # widget 정의 및 추가 for문
        for i in range(len(menu_list)):
            self.lbls_menu.append(QLabel(menu_list[i].name, self))
            self.lbls_qt.append(QLabel(str(menu_list[i].qt), self))
            self.btns_minus.append(QPushButton('-', self))
            self.btns_add.append(QPushButton('+', self))
            self.btns_cancel.append(QPushButton('x', self))
            self.btns_input.append(QPushButton('수량입력', self))
            self.lbls_tot.append(QLabel(str(menu_list[i].tot), self))

            grid.addWidget(self.lbls_menu[i], i, 0)
            grid.addWidget(self.lbls_qt[i], i, 1)
            grid.addWidget(self.btns_minus[i], i, 2)
            grid.addWidget(self.btns_add[i], i, 3)
            grid.addWidget(self.btns_cancel[i], i, 4)
            grid.addWidget(self.btns_input[i], i, 5)
            grid.addWidget(self.lbls_tot[i], i, 6)

        self.lbl_totqt = QLabel(str(total.qt), self)
        self.lbl_totsum = QLabel(str(total.sum), self)
        self.btn_totcancel = QPushButton('전체취소', self)
        self.btn_paycash = QPushButton('현금결제', self)
        self.btn_paycard = QPushButton('카드결제', self)

        grid.addWidget(self.lbl_totqt, 4, 1)
        grid.addWidget(self.lbl_totsum, 4, 6)
        grid.addWidget(self.btn_totcancel, 5, 1)
        grid.addWidget(self.btn_paycash, 5, 5)
        grid.addWidget(self.btn_paycard, 5, 6)

        gbox.setLayout(grid)

        # pushbutton clicked signal call #보다 간략하게 수정 필요
        self.btns_minus[0].clicked.connect(lambda: self.menuMinus(0))
        self.btns_minus[1].clicked.connect(lambda: self.menuMinus(1))
        self.btns_minus[2].clicked.connect(lambda: self.menuMinus(2))
        self.btns_minus[3].clicked.connect(lambda: self.menuMinus(3))

        self.btns_add[0].clicked.connect(lambda: self.menuAdd(0))
        self.btns_add[1].clicked.connect(lambda: self.menuAdd(1))
        self.btns_add[2].clicked.connect(lambda: self.menuAdd(2))
        self.btns_add[3].clicked.connect(lambda: self.menuAdd(3))

        self.btns_cancel[0].clicked.connect(lambda: self.menuCancel(0))
        self.btns_cancel[1].clicked.connect(lambda: self.menuCancel(1))
        self.btns_cancel[2].clicked.connect(lambda: self.menuCancel(2))
        self.btns_cancel[3].clicked.connect(lambda: self.menuCancel(3))

        self.btns_input[0].clicked.connect(lambda: self.menuInputDialog(0))
        self.btns_input[1].clicked.connect(lambda: self.menuInputDialog(1))
        self.btns_input[2].clicked.connect(lambda: self.menuInputDialog(2))
        self.btns_input[3].clicked.connect(lambda: self.menuInputDialog(3))

        self.btn_totcancel.clicked.connect(self.totalCancel)
        self.btn_paycash.clicked.connect(self.payCash)
        self.btn_paycard.clicked.connect(self.payCard)


        return gbox

    def createGB1(self):  # 메뉴선택 #grid:(0,1)
        gbox = QGroupBox('메뉴선택')
        vbox = QVBoxLayout()

        # widget list 정의
        self.btns_menu = []

        # widget 정의 및 추가 for문
        for i in range(len(menu_list)):
            self.btns_menu.append(QPushButton(menu_list[i].name + '\n'
                                              + str(menu_list[i].cost)+ '원', self))
            vbox.addWidget(self.btns_menu[i])

        gbox.setLayout(vbox)  # verticalbox layout

        # pushbutton clicked signal call #보다 간략하게 수정 필요
        self.btns_menu[0].clicked.connect(lambda: self.menuClicked(0))
        self.btns_menu[1].clicked.connect(lambda: self.menuClicked(1))
        self.btns_menu[2].clicked.connect(lambda: self.menuClicked(2))
        self.btns_menu[3].clicked.connect(lambda: self.menuClicked(3))

        return gbox


    # 수량, 금액 label setText
    def lbltxt_changed(self):
        for i in range(len(menu_list)):
            self.lbls_qt[i].setText(str(menu_list[i].qt))
            self.lbls_tot[i].setText(str(menu_list[i].tot))
        self.lbl_totqt.setText(str(total.qt))
        self.lbl_totsum.setText(str(total.sum))

    # 수량 변경/취소
    def menuClicked(self, i):
        menu_list[i].menu_qt(1)
        self.lbltxt_changed()

    def menuMinus(self, i):
        menu_list[i].menu_qt(-1)
        self.lbltxt_changed()

    def menuAdd(self, i):
        self.menuClicked(i)

    def menuCancel(self, i):
        menu_list[i].menu_qt(0)
        self.lbltxt_changed()

    def menuInputDialog(self, i):
        num, ok = QInputDialog.getInt(self, '수량 직접입력',
                                      menu_list[i].name + '의 수량을 입력하세요.', min=0)
        if ok:
            menu_list[i].menu_qt_input(num)
            self.lbltxt_changed()

    # 전체 취소
    def totalCancel(self):
        americano.tot_cancel()
        self.lbltxt_changed()

    # 현금결제
    def payCash(self):
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
    def payCard(self):
        reply = QMessageBox.question(self, '카드결제',
                                     '결제할 금액: '+ str(total.sum) + '원' + '\n' + \
                                     '카드로 결제합니까?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if reply == QMessageBox.Yes:
            self.payComplete('카드')

    # 결제완료
    def payComplete(self, method):
        msg = QMessageBox.information(self, '결제완료',
                                      '결제금액: '+ str(total.sum) + '원' + '\n' + \
                                      '결제수단: '+ method + '\n' + \
                                      '결제가 완료되었습니다.',
                                      QMessageBox.Ok, QMessageBox.Ok)

        sales.orderOccur()

        self.lbltxt_changed()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
