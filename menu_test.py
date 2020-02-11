#menu_test

#menu_excel load
import pandas as pd
filepath = './menu_excel.xlsx'
menu_excel = pd.read_excel(filepath)

#menu class
class Menu:
    def __init__(self, idx):
        self.menu_name = menu_excel['메뉴명'][idx]
        self.menu_cost = menu_excel['가격'][idx]
        self.menu_qt = 0

    def qt_changed(self, num):
        if self.menu_qt + num < 0:
            self.menu_qt = 0
        else:
            self.menu_qt += num
        return self.menu_qt

    def total_amount(self):
        self.menu_tot = self.menu_qt * self.menu_cost
        return self.menu_tot

#menu instance
americano = Menu(0)
latte = Menu(1)

#GUI part
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QHBoxLayout, QVBoxLayout

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.btn0 = QPushButton(menu_excel['메뉴명'][0], self)  # pushbutton #메뉴
        self.btn1 = QPushButton(menu_excel['메뉴명'][1], self)  # pushbutton #메뉴

        self.lbl0 = QLabel('0', self) #label #수량
        self.lbl1 = QLabel('0', self) #label #수량
        self.lbl_menu0 = QLabel(menu_excel['메뉴명'][0], self)  # 주문현황의 메뉴
        self.lbl_menu1 = QLabel(menu_excel['메뉴명'][1], self)  # 주문현황의 메뉴

        self.btn0.clicked.connect(self.menuClicked(0))  # clicked signal -> call menuClicked
        self.btn1.clicked.connect(self.menuClicked(1))  # clicked signal -> call menuClicked

        hbox = QHBoxLayout()  #주문현황 part #HorizentalBox 수평 레이아웃
        hbox.addWidget(self.lbl_menu0)
        hbox.addWidget(self.lbl0)
        hbox.addWidget(self.lbl_menu1)
        hbox.addWidget(self.lbl1)

        hbox2 = QHBoxLayout() #메뉴 part #HorizentalBox 수평 레이아웃
        hbox2.addWidget(self.btn0)
        hbox2.addWidget(self.btn1)

        vbox = QVBoxLayout()  #VerticalBox 수직 레이아웃
        vbox.addLayout(hbox)
        vbox.addStretch(1)
        vbox.addLayout(hbox2)

        self.setLayout(vbox)  #Layout

        self.setWindowTitle('POS by brilliantOh')
        self.setGeometry(300, 300, 300, 200)
        self.show()

    def menuClicked(self, idx):
        if idx == 0:
            self.lbl0.setText(str(americano.qt_changed(1)))
        elif idx == 1:
            self.lbl1.setText(str(latte.qt_changed(1)))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())