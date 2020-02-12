#GUI_200212

#initialize part
from initialize import menu_excel, Menu, americano, latte, iceamericano, icelatte
#menu_list
menu_list = [americano, latte, iceamericano, icelatte]

#GUI part
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QGroupBox, QInputDialog, \
    QHBoxLayout, QVBoxLayout, QGridLayout

class MyApp(QWidget):
    def __init__(self):
        super().__init__() #기반 class의 __init__ call
        self.initUI()

    def initUI(self):
        grid = QGridLayout()
        grid.addWidget(self.createGB0(),0,0) #groupbox
        grid.addWidget(self.createGB1(),0,1) #groupbox

        self.setLayout(grid) #gridlayout

        self.setWindowTitle('POS by brilliantOh')
        self.setGeometry(600,300,480,320)
        self.show()

    def createGB0(self): #주문현황 #grid:(0,0)
        gbox = QGroupBox('주문현황')
        grid = QGridLayout() #gridlayout

        self.lbls_menu = [] #메뉴명 label list
        self.lbls_qt = [] #수량 label list
        self.btns_minus = [] #수량- pushbutton list
        self.btns_add = [] #수량+ pushbutton list
        self.btns_cancel = [] #취소 pushbutton list
        self.btns_input = [] #직접입력 pushbutton list
        self.lbls_tot = []

        for i in range(len(menu_excel)): #label widget 정의 및 추가 for문
            self.lbls_menu.append(QLabel(menu_excel['메뉴명'][i], self)) #메뉴명 label
            self.lbls_qt.append(QLabel('0', self)) #수량 label
            self.btns_minus.append(QPushButton('-', self))
            self.btns_add.append(QPushButton('+', self))
            self.btns_cancel.append(QPushButton('x', self))
            self.btns_input.append(QPushButton('수량입력', self))
            self.lbls_tot.append(QLabel('0', self)) #금액 label
            grid.addWidget(self.lbls_menu[i], i, 0)
            grid.addWidget(self.lbls_qt[i], i, 1)
            grid.addWidget(self.btns_minus[i], i, 2)
            grid.addWidget(self.btns_add[i], i, 3)
            grid.addWidget(self.btns_cancel[i], i, 4)
            grid.addWidget(self.btns_input[i], i, 5)
            grid.addWidget(self.lbls_tot[i], i, 6)

        self.lbl_totsum = QLabel('0', self) #총액 label
        grid.addWidget(self.lbl_totsum, 4, 6)

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

    def createGB1(self): #메뉴선택 #grid:(0,1)
        gbox = QGroupBox('메뉴선택')
        vbox = QVBoxLayout()

        self.btns_menu = [] #메뉴 pushbutton list

        for i in range(len(menu_excel)): #pushbutton widget 정의 및 추가 for문
            self.btns_menu.append(QPushButton(menu_excel['메뉴명'][i], self)) #메뉴 pushbutton
            vbox.addWidget(self.btns_menu[i])

        self.btns_menu[0].clicked.connect(lambda: self.menuClicked(0)) #click signal->menuClicked
        self.btns_menu[1].clicked.connect(lambda: self.menuClicked(1))
        self.btns_menu[2].clicked.connect(lambda: self.menuClicked(2))
        self.btns_menu[3].clicked.connect(lambda: self.menuClicked(3))

        gbox.setLayout(vbox) #verticalbox layout

        return gbox

    def menuClicked(self, i): #pushbutton clicked signal call
        self.lbls_qt[i].setText(str(menu_list[i].qt_changed(1))) #수량 label 변경
        self.menuTot(i) #메뉴금액 계산 함수 call

    def menuMinus(self, i):
        self.lbls_qt[i].setText(str(menu_list[i].qt_changed(-1)))
        self.menuTot(i)

    def menuAdd(self, i):
        self.lbls_qt[i].setText(str(menu_list[i].qt_changed(1)))
        self.menuTot(i)

    def menuCancel(self, i):
        self.lbls_qt[i].setText(str(menu_list[i].qt_canceled()))
        self.menuTot(i)

    def menuInputDialog(self, i): #수량변경
        num, ok = QInputDialog.getInt(self, '수량 직접입력', '수량을 입력하세요.', min=0)

        if ok:
            menu_list[i].qt = num
            self.lbls_qt[i].setText(str(menu_list[i].qt))
            self.menuTot(i)

    def menuTot(self, i): #메뉴금액 계산
        self.lbls_tot[i].setText(str(menu_list[i].menu_tot()))
        self.menuTotSum()

    def menuTotSum(self): #총액 계산
        self.lbl_totsum.setText((str(Menu.tot_sum())))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())