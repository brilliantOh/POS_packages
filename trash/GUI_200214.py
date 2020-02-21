# GUI_200214

# initialize part
from initialize_totsumqt import menu_excel, Menu, americano, latte, iceamericano, icelatte, \
    Total, total


# 편의를 위한 menu_list 정의
menu_list = [americano, latte, iceamericano, icelatte]

# GUI part
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QGroupBox, QInputDialog, \
    QMessageBox, QVBoxLayout, QGridLayout

class MyApp(QWidget):
    def __init__(self):
        super().__init__()  # 기반 class의 __init__ call
        self.initUI()

    def initUI(self):
        self.setWindowTitle('POS by brilliantOh')  # 창 이름
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
        for i in range(len(menu_excel)):
            self.lbls_menu.append(QLabel(menu_excel['메뉴명'][i], self))
            self.lbls_qt.append(QLabel('0', self))
            self.btns_minus.append(QPushButton('-', self))
            self.btns_add.append(QPushButton('+', self))
            self.btns_cancel.append(QPushButton('x', self))
            self.btns_input.append(QPushButton('수량입력', self))
            self.lbls_tot.append(QLabel('0', self))
            grid.addWidget(self.lbls_menu[i], i, 0)
            grid.addWidget(self.lbls_qt[i], i, 1)
            grid.addWidget(self.btns_minus[i], i, 2)
            grid.addWidget(self.btns_add[i], i, 3)
            grid.addWidget(self.btns_cancel[i], i, 4)
            grid.addWidget(self.btns_input[i], i, 5)
            grid.addWidget(self.lbls_tot[i], i, 6)

        self.lbl_totqt = QLabel('0', self)
        self.lbl_totsum = QLabel('0', self)
        grid.addWidget(self.lbl_totqt, 4, 1)
        grid.addWidget(self.lbl_totsum, 4, 6)

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

        gbox.setLayout(grid)

        return gbox

    def createGB1(self):  # 메뉴선택 #grid:(0,1)
        gbox = QGroupBox('메뉴선택')
        vbox = QVBoxLayout()

        # widget list 정의
        self.btns_menu = []

        # widget 정의 및 추가 for문
        for i in range(len(menu_excel)):
            self.btns_menu.append(QPushButton(menu_excel['메뉴명'][i] + '\n'
                                              + str(menu_excel['가격'][i])+ '원', self))
            vbox.addWidget(self.btns_menu[i])

        # pushbutton clicked signal call #보다 간략하게 수정 필요
        self.btns_menu[0].clicked.connect(lambda: self.menuClicked(0))
        self.btns_menu[1].clicked.connect(lambda: self.menuClicked(1))
        self.btns_menu[2].clicked.connect(lambda: self.menuClicked(2))
        self.btns_menu[3].clicked.connect(lambda: self.menuClicked(3))

        gbox.setLayout(vbox)  # verticalbox layout

        return gbox

    # 버튼 클릭시 call할 함수 정의 # 수량
    def menuClicked(self, i):
        self.lbls_qt[i].setText(str(menu_list[i].menu_qt(1)))
        self.menuTot(i)
        self.totqt_changed(i)

    def menuMinus(self, i):
        self.lbls_qt[i].setText(str(menu_list[i].menu_qt(-1)))
        self.menuTot(i)

    def menuAdd(self, i):
        self.lbls_qt[i].setText(str(menu_list[i].menu_qt(1)))
        self.menuTot(i)

    def menuCancel(self, i):
        self.lbls_qt[i].setText(str(menu_list[i].menu_qt(0)))
        self.menuTot(i)

    def menuInputDialog(self, i):
        num, ok = QInputDialog.getInt(self, '수량 직접입력', menu_excel['메뉴명'][i] \
                                      + '의 수량을 입력하세요.', min=0)
        if ok:
            self.lbls_qt[i].setText(str(menu_list[i].menu_qt(num)))
            self.menuTot(i)

    # 전체 수량
    def totqt_changed(self, i):
        self.lbl_totqt.setText(str(total.tot_qt(menu_list[i].qt)))


    # 버튼 클릭시 call할 함수 정의 # 금액
    def menuTot(self, i):
        self.lbls_tot[i].setText(str(menu_list[i].menu_tot()))
        self.totsum_changed(i)
    
    # 총액
    def totsum_changed(self, i):
        self.lbl_totsum.setText(str(total.tot_sum(menu_list[i].tot)))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
