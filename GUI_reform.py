#GUI_reform

from initialize_reform import POS_calculator, menu_excel, cal, menu_names_list, menu_cost_dic
import sys
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QTabWidget, QTableWidget, QTableWidgetItem, \
    QPushButton, QLabel, QGroupBox, QInputDialog, QMessageBox, QHBoxLayout, QVBoxLayout, QGridLayout


# Main Window
class MyApp(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.title = 'POS_reform'
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(600, 300, 480, 320)

        widget = MyWidget(self)
        self.setCentralWidget(widget)

        self.show()

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
        tabs = QTabWidget()
        vbox = QVBoxLayout()

        tabs.addTab(FirstTab(), '주문/계산')
        tabs.addTab(SecondTab(), '내역조회')

        vbox.addWidget(tabs)

        self.setLayout(vbox)


# Tab Widget: 주문/계산
class FirstTab(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        grid = QGridLayout()

        grid.addWidget(self.create_order_groupbox(), 0, 0)
        grid.addWidget(self.create_menu_groupbox(), 0, 1)

        self.setLayout(grid)

    # Groupbox: 주문현황
    def create_order_groupbox(self):
        gbox = QGroupBox()
        gbox.setTitle('주문현황')
        hbox = QHBoxLayout()
        vbox = QVBoxLayout()

        # widget
        self.cart_table = QTableWidget()
        self.create_cart_table()
        vbox.addWidget(self.cart_table)

        vbox.addLayout(hbox)
        btn_cancel_all = QPushButton('전체취소', self)
        btn_cancel_all.clicked.connect(self.cancel_all_in_cart)
        hbox.addWidget(btn_cancel_all)

        gbox.setLayout(vbox)

        return gbox


    # Groupbox: 메뉴선택
    def create_menu_groupbox(self):
        gbox = QGroupBox()
        gbox.setTitle('메뉴선택')
        vbox = QVBoxLayout()

        # widget
        btns_menu = []

        for i in range(len(menu_excel['메뉴명'])):
            btns_menu.append(QPushButton())
            btns_menu[i].setText(menu_excel['메뉴명'][i] + '\n' + str(menu_excel['가격'][i]) + '원')
            vbox.addWidget(btns_menu[i])
            # Signal
            btns_menu[i].clicked.connect(lambda arg, idx=i: self.add_menu_in_cart(menu_excel['메뉴명'][idx]))

        gbox.setLayout(vbox)

        return gbox

    # Table Widget: 카트
    def create_cart_table(self):
        header_list = ['메뉴', '수량', '감소', '증가', '직접입력', '단가', '금액', '취소']

        self.cart_table.setColumnCount(len(header_list))
        self.cart_table.setRowCount(len(menu_excel['메뉴명']))

        self.cart_table.setHorizontalHeaderLabels(header_list)

    # Slot
    @pyqtSlot()
    def set_item_in_cart_table(self):
        self.cart_table.clearContents()

        if len(cal.cart_list) != 0:
            skip_count = 0
            for i in range(len(cal.cart_list)):
                if i == 0:
                    self.cart_table.setItem(0, 0, QTableWidgetItem(cal.cart_list[i]))
                    self.cart_table.setItem(0, 1, QTableWidgetItem(str(cal.return_menu_qty(cal.cart_list[i]))))
                    self.cart_table.setItem(0, 5, QTableWidgetItem(str(cal.return_menu_cost(cal.cart_list[i]))))
                    self.cart_table.setItem(0, 6, QTableWidgetItem(str(cal.return_menu_amount(cal.cart_list[i]))))
                elif i >= 1 and cal.cart_list[i] in cal.cart_list[:i]:
                    skip_count += 1
                else:
                    self.cart_table.setItem(skip_count+1, 0, QTableWidgetItem(cal.cart_list[i]))
                    self.cart_table.setItem(skip_count+1, 1, QTableWidgetItem(str(cal.return_menu_qty(cal.cart_list[i]))))
                    self.cart_table.setItem(skip_count+1, 5, QTableWidgetItem(str(cal.return_menu_cost(cal.cart_list[i]))))
                    self.cart_table.setItem(skip_count+1, 6, QTableWidgetItem(str(cal.return_menu_amount(cal.cart_list[i]))))

    @pyqtSlot(str)
    def add_menu_in_cart(self, menu_str):
        cal.add_qty(menu_str)
        self.set_item_in_cart_table()

    @pyqtSlot(str)
    def minus_menu_in_cart(self, menu_str):
        cal.minus_qty(menu_str)
        self.set_item_in_cart_table()

    @pyqtSlot(str, int)
    def input_menu_in_cart(self, menu_str, input_int):
        cal.input_qty(menu_str, input_int)
        self.set_item_in_cart_table()

    @pyqtSlot(str)
    def cancel_menu_in_cart(self, menu_str):
        cal.cancel_qty(menu_str)
        self.set_item_in_cart_table()

    @pyqtSlot()
    def cancel_all_in_cart(self):
        cal.cancel_all_qty()
        self.set_item_in_cart_table()

    @pyqtSlot()
    def print_bill_of_recent_order(self):
        pass

    @pyqtSlot()
    def pay_in_cash(self):
        pass

    @pyqtSlot()
    def pay_in_credit_card(self):
        pass


# Tab Widget: 내역조회
class SecondTab(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        grid = QGridLayout()

        grid.addWidget(self.create_choice_groupbox(), 0, 0)
        grid.addWidget(self.create_view_groupbox(), 0, 1)

        self.setLayout(grid)

    # Groupbox: 주문결제내역
    def create_choice_groupbox(self):
        gbox = QGroupBox()
        gbox.setTitle('주문결제내역')

        return gbox

    # Groupbox: 조회
    def create_view_groupbox(self):
        gbox = QGroupBox()
        gbox.setTitle('조회')

        return gbox


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())