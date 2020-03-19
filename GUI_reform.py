# GUI_reform

import sys

from PyQt5.QtCore import pyqtSlot, QDate
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QTabWidget, QTableWidget, QTableWidgetItem, \
    QPushButton, QGroupBox, QInputDialog, QMessageBox, QHBoxLayout, QVBoxLayout, QGridLayout, QAbstractItemView, \
    QDateEdit, QLabel

from initialize_reform import menu_excel, cal
from receipt import rec
from sales_stats import stats


# Main Window
class MyApp(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.title = 'POS_reform'
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(600, 300, 1024, 300)

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
        tabs.addTab(ThirdTab(), '매출집계')

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

        btn_print_bill = QPushButton('영수증출력', self)
        btn_cancel_all = QPushButton('전체취소', self)
        btn_pay_in_cash = QPushButton('현금결제', self)
        btn_pay_in_card = QPushButton('카드결제', self)
        # Signal
        btn_print_bill.clicked.connect(self.print_bill_of_recent_order)
        btn_cancel_all.clicked.connect(self.cancel_all_in_cart)
        btn_pay_in_cash.clicked.connect(self.pay_in_cash)
        btn_pay_in_card.clicked.connect(self.pay_in_credit_card)

        hbox.addWidget(btn_print_bill)
        hbox.addWidget(btn_cancel_all)
        hbox.addWidget(btn_pay_in_cash)
        hbox.addWidget(btn_pay_in_card)

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
        self.cart_table.setRowCount(len(menu_excel['메뉴명']) + 1)

        self.cart_table.setHorizontalHeaderLabels(header_list)

        self.cart_table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.cart_table.setItem(4, 0, QTableWidgetItem('Total'))
        self.cart_table.setItem(4, 1, QTableWidgetItem(str(cal.return_total_qty())))
        self.cart_table.setItem(4, 6, QTableWidgetItem(str(cal.return_total_amount())))

    # Slot
    @pyqtSlot()
    def set_item_in_cart_table(self):
        self.cart_table.clearContents()

        self.cart_table.setItem(4, 0, QTableWidgetItem('Total'))
        self.cart_table.setItem(4, 1, QTableWidgetItem(str(cal.return_total_qty())))
        self.cart_table.setItem(4, 6, QTableWidgetItem(str(cal.return_total_amount())))

        btns_minus = []
        btns_add = []
        btns_input = []
        btns_cancel = []
        row_int = 0

        if len(cal.cart_list) != 0:
            for i in range(len(cal.cart_list)):
                if cal.cart_list[i] not in cal.cart_list[:i]:
                    btns_minus.append(QPushButton('-', self))
                    btns_add.append(QPushButton('+', self))
                    btns_input.append(QPushButton('수량입력', self))
                    btns_cancel.append(QPushButton('x', self))

                    self.cart_table.setItem(row_int, 0, QTableWidgetItem(cal.cart_list[i]))
                    self.cart_table.setItem(row_int, 1, QTableWidgetItem(str(cal.return_menu_qty(cal.cart_list[i]))))
                    self.cart_table.setItem(row_int, 5, QTableWidgetItem(str(cal.return_menu_cost(cal.cart_list[i]))))
                    self.cart_table.setItem(row_int, 6, QTableWidgetItem(str(cal.return_menu_amount(cal.cart_list[i]))))

                    self.cart_table.setCellWidget(row_int, 2, btns_minus[row_int])
                    self.cart_table.setCellWidget(row_int, 3, btns_add[row_int])
                    self.cart_table.setCellWidget(row_int, 4, btns_input[row_int])
                    self.cart_table.setCellWidget(row_int, 7, btns_cancel[row_int])

                    # Signal
                    btns_minus[row_int].clicked.connect(lambda: self.minus_menu_in_cart(cal.cart_list[i]))
                    btns_add[row_int].clicked.connect(lambda: self.add_menu_in_cart(cal.cart_list[i]))
                    btns_input[row_int].clicked.connect(lambda: self.input_menu_in_cart(cal.cart_list[i]))
                    btns_cancel[row_int].clicked.connect(lambda: self.cancel_menu_in_cart(cal.cart_list[i]))

                    row_int += 1

    @pyqtSlot(str)
    def add_menu_in_cart(self, menu_str):
        cal.add_qty(menu_str)
        self.set_item_in_cart_table()

    @pyqtSlot(str)
    def minus_menu_in_cart(self, menu_str):
        cal.minus_qty(menu_str)
        self.set_item_in_cart_table()

    @pyqtSlot(str)
    def input_menu_in_cart(self, menu_str):
        input_int, ok = QInputDialog.getInt(self, '수량 직접입력', menu_str + '의 수량을 입력하세요.', min=0)
        if ok:
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
        msg = QMessageBox.information(self, '영수증출력', str(rec.receipt_df), QMessageBox.Ok, QMessageBox.Ok)

    @pyqtSlot()
    def pay_in_cash(self):
        if len(cal.cart_list) == 0:
            self.warn_pay_zero()
        else:
            cash, ok = QInputDialog.getInt(self, '현금결제', '결제할 금액: ' + \
                                           str(cal.return_total_amount()) + '원' + '\n' + \
                                           '받은 금액을 입력하세요.', min=cal.return_total_amount())
            if ok:
                reply = QMessageBox.question(self, '현금결제: 거스름돈',
                                             '결제할 금액: ' + str(cal.return_total_amount()) + '원' + '\n' + \
                                             '받은 금액: ' + str(cash) + '원' + '\n' + \
                                             '거스름돈: ' + str(cash - cal.return_total_amount()) + '원' + '\n' + \
                                             '이대로 결제합니까?',
                                             QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
                if reply == QMessageBox.Yes:
                    self.complete_payment('현금')

    @pyqtSlot()
    def pay_in_credit_card(self):
        if len(cal.cart_list) == 0:
            self.warn_pay_zero()
        else:
            reply = QMessageBox.question(self, '카드결제',
                                         '결제할 금액: ' + str(cal.return_total_amount()) + '원' + '\n' + '카드로 결제합니까?',
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if reply == QMessageBox.Yes:
                self.complete_payment('카드')

    @pyqtSlot()
    def warn_pay_zero(self):
        msg = QMessageBox.information(self, '결제금액 경고', '결제금액은 0원일 수 없습니다.',
                                      QMessageBox.Ok, QMessageBox.Ok)

    @pyqtSlot(str)
    def complete_payment(self, payment_method_str):
        rec.receive_order(payment_method_str)
        msg = QMessageBox.information(self, '결제완료', '결제수단: ' + payment_method_str + '\n' + '결제가 완료되었습니다.',
                                      QMessageBox.Ok, QMessageBox.Ok)
        self.set_item_in_cart_table()


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
        vbox = QVBoxLayout()

        # widget
        btn_update = QPushButton('새로고침', self)
        btn_update.clicked.connect(self.set_item_in_order_history_table)
        vbox.addWidget(btn_update)
        self.order_history_table = QTableWidget()
        self.create_order_history_table()
        vbox.addWidget(self.order_history_table)

        gbox.setLayout(vbox)

        return gbox

    # Groupbox: 조회
    def create_view_groupbox(self):
        gbox = QGroupBox()
        gbox.setTitle('조회')
        vbox = QVBoxLayout()

        # widget
        self.order_details_table = QTableWidget()
        self.create_order_details_table()
        vbox.addWidget(self.order_details_table)

        gbox.setLayout(vbox)

        return gbox

    # Table Widget: 조회할 주문 선택
    def create_order_history_table(self):
        self.order_history_table.setColumnCount(len(rec.summary_cols_list))
        self.order_history_table.setHorizontalHeaderLabels(rec.summary_cols_list)

        self.order_history_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.order_history_table.setSelectionBehavior(QAbstractItemView.SelectRows)

    # Table Widget: 상세조회
    def create_order_details_table(self):
        self.order_details_table.setColumnCount(len(rec.details_cols_list))
        self.order_details_table.setHorizontalHeaderLabels(rec.details_cols_list)
        self.order_details_table.setRowCount(4)

        self.order_details_table.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def set_item_in_order_history_table(self):
        self.order_history_table.clearContents()
        self.order_history_table.setRowCount(rec.summary_ws.max_row - 1)

        order_history_list = []
        for row in rec.summary_ws.iter_rows(min_row=2, values_only=True):
            order_history_list.append(row)

        for i in range(rec.summary_ws.max_row - 1):
            self.order_history_table.setItem(i, 0, QTableWidgetItem(order_history_list[i][0]))
            self.order_history_table.setItem(i, 1, QTableWidgetItem(str(order_history_list[i][1])))
        # Signal
        self.order_history_table.cellClicked.connect(self.set_item_in_order_details_table)

    @pyqtSlot(int, int)
    def set_item_in_order_details_table(self, row_int, col):
        self.order_details_table.clearContents()

        order_datetime_list = []
        order_details_list = []
        for row in rec.details_ws.iter_rows(min_row=2, values_only=True):
            order_datetime_list.append(row[0])
            order_details_list.append(row)

        order_datetime = rec.summary_ws['A'][row_int + 1].value
        order_index = order_datetime_list.index(order_datetime)
        order_count = order_datetime_list.count(order_datetime)
        self.order_details_table.setRowCount(order_count)
        order_details_2_list = order_details_list[order_index: order_index + order_count]

        for i in range(order_count):
            self.order_details_table.setItem(i, 0, QTableWidgetItem(order_details_2_list[i][0]))
            self.order_details_table.setItem(i, 1, QTableWidgetItem(order_details_2_list[i][1]))
            self.order_details_table.setItem(i, 2, QTableWidgetItem(str(order_details_2_list[i][2])))
            self.order_details_table.setItem(i, 3, QTableWidgetItem(str(order_details_2_list[i][3])))
            self.order_details_table.setItem(i, 4, QTableWidgetItem(str(order_details_2_list[i][4])))
            self.order_details_table.setItem(i, 5, QTableWidgetItem(order_details_2_list[i][5]))


# Tab Widget : 매출집계
class ThirdTab(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        grid = QGridLayout()

        grid.addWidget(self.create_choice_groupbox(), 0, 0)
        grid.addWidget(self.create_view_groupbox(), 0, 1)

        self.setLayout(grid)

    # Groupbox : 기간 선택
    def create_choice_groupbox(self):
        gbox = QGroupBox()
        hbox = QHBoxLayout()
        vbox = QVBoxLayout()
        hbox2 = QHBoxLayout()

        # widget
        lbl_period = QLabel('조회기간')
        self.dateed_start = QDateEdit()
        lbl_mark = QLabel('~')
        self.dateed_end = QDateEdit()
        self.dateed_start.setDate(QDate.currentDate())
        self.dateed_end.setDate(QDate.currentDate())
        self.dateed_start.setCalendarPopup(True)
        self.dateed_end.setCalendarPopup(True)
        btn_week = QPushButton('1주')
        btn_view = QPushButton('조회')
        # Signal
        btn_week.clicked.connect(self.change_week_period)
        btn_view.clicked.connect(self.lookup_period_sales)

        hbox.addWidget(lbl_period)
        hbox.addWidget(self.dateed_start)
        hbox.addWidget(lbl_mark)
        hbox.addWidget(self.dateed_end)
        hbox2.addWidget(btn_week)
        hbox2.addWidget(btn_view)
        vbox.addLayout(hbox)
        vbox.addLayout(hbox2)
        gbox.setLayout(vbox)

        return gbox

    # Groupbox : 조회
    def create_view_groupbox(self):
        gbox = QGroupBox()
        return gbox


    @pyqtSlot()
    def change_week_period(self):
        self.dateed_start.setDate(self.dateed_end.date().addDays(-6))

    @pyqtSlot()
    def lookup_period_sales(self):
        if self.dateed_end.date() < self.dateed_start.date():
            self.warn_period()
        else:
            stats.stats_period_sales(self.dateed_start.date().toPyDate(), self.dateed_end.date().toPyDate())

    @pyqtSlot()
    def warn_period(self):
        msg = QMessageBox.information(self, '조회기간 경고', '시작일이 종료일보다 나중입니다.',
                                      QMessageBox.Ok, QMessageBox.Ok)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
