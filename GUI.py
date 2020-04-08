'''
GUI.py
=========================
GUI module of POS_packages
'''

# import packages
import sys

from PyQt5.QtCore import pyqtSlot, QDate
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QTabWidget, QTableWidget, QTableWidgetItem, \
    QPushButton, QGroupBox, QInputDialog, QMessageBox, QHBoxLayout, QVBoxLayout, QGridLayout, QAbstractItemView, \
    QDateEdit, QLabel
from PyQt5.QtGui import QIcon

import matplotlib.pyplot as plt
from matplotlib import font_manager, rc

from calculator import POS_calculator, cal, menu_excel
from receipt import POS_receipt, rec
from sales_stats import POS_statistics, stats


# matplotlib font management(Korean)
font_name = font_manager.FontProperties(fname='C:\Windows\Fonts\malgun.ttf').get_name()
rc('font', family=font_name)

# Main Window
class MyApp(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.title = 'POS by brilliantOh'
        self.initUI()

    def initUI(self):
        # 기본 설정(프로그램 이름, 창 크기, 프로그램 아이콘)
        self.setWindowTitle(self.title)
        self.setGeometry(600, 300, 1024, 300)
        self.setWindowIcon(QIcon(r'C:\Users\JH\POS_packages\image_icon.jpg'))
        # 중앙 위젯 설정
        widget = MyWidget(self)
        self.setCentralWidget(widget)

        self.show()

    def closeEvent(self, event):
        # 종료 시 발생할 이벤트 설정 (messagebox)
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
        # 기능별 탭 생성 (tab)
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
        # 기능별 그룹박스 생성 (groupbox)
        grid.addWidget(self.create_order_groupbox(), 0, 0)
        grid.addWidget(self.create_menu_groupbox(), 0, 1)

        self.setLayout(grid)

    # Groupbox: 주문현황
    def create_order_groupbox(self):
        gbox = QGroupBox()
        gbox.setTitle('주문현황')
        hbox = QHBoxLayout()
        vbox = QVBoxLayout()

        # 장바구니 테이블 생성 (tablewidget)
        self.cart_table = QTableWidget()
        self.create_cart_table()
        vbox.addWidget(self.cart_table)

        vbox.addLayout(hbox)

        # 버튼 생성 (pushbutton)
        btn_print_bill = QPushButton('영수증출력', self)
        btn_cancel_all = QPushButton('전체취소', self)
        btn_pay_in_cash = QPushButton('현금결제', self)
        btn_pay_in_card = QPushButton('카드결제', self)
        # Signal: 버튼 클릭시 연결문
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

        # 버튼 생성 (pushbutton)
        btns_menu = []
        for i in range(len(menu_excel['메뉴명'])):
            btns_menu.append(QPushButton())
            btns_menu[i].setText(menu_excel['메뉴명'][i] + '\n' + str(menu_excel['가격'][i]) + '원')
            vbox.addWidget(btns_menu[i])
            # Signal: 버튼 클릭시 연결문
            btns_menu[i].clicked.connect(lambda arg, idx=i: self.add_menu_in_cart(menu_excel['메뉴명'][idx]))

        gbox.setLayout(vbox)

        return gbox

    # Table Widget: 카트
    def create_cart_table(self):
        # 장바구니 테이블의 column이 될 list 생성
        header_list = ['메뉴', '수량', '감소', '증가', '직접입력', '단가', '금액', '취소']
        # 장바구니 테이블 기본 설정 (tablewidget): row 길이, col 길이, header label
        self.cart_table.setColumnCount(len(header_list))
        self.cart_table.setRowCount(len(menu_excel['메뉴명']) + 1)
        self.cart_table.setHorizontalHeaderLabels(header_list)

        # 장바구니 테이블 최하단에 총 금액, 총 수량 세팅
        self.cart_table.setItem(len(menu_excel['메뉴명']), 0, QTableWidgetItem('Total'))
        self.cart_table.setItem(len(menu_excel['메뉴명']), 1, QTableWidgetItem(str(cal.return_total_qty())))
        self.cart_table.setItem(len(menu_excel['메뉴명']), 6, QTableWidgetItem(str(cal.return_total_amount())))

        # 테이블에서 직접 수정 불가능하게 설정
        self.cart_table.setEditTriggers(QAbstractItemView.NoEditTriggers)

    # Slot
    @pyqtSlot()
    def set_item_in_cart_table(self):
        # 장바구니 테이블 내용 지우기
        self.cart_table.clearContents()
        # 장바구니 테이블 최하단에 총 금액, 총 수량 세팅
        self.cart_table.setItem(len(menu_excel['메뉴명']), 0, QTableWidgetItem('Total'))
        self.cart_table.setItem(len(menu_excel['메뉴명']), 1, QTableWidgetItem(str(cal.return_total_qty())))
        self.cart_table.setItem(len(menu_excel['메뉴명']), 6, QTableWidgetItem(str(cal.return_total_amount())))

        btns_minus = []
        btns_add = []
        btns_input = []
        btns_cancel = []
        # 장바구니 테이블 row 세팅
        row_int = 0

        # 장바구니(cart_list)를 장바구니 테이블로 불러오기
        if len(cal.cart_list) != 0:
            for i in range(len(cal.cart_list)):
                if cal.cart_list[i] not in cal.cart_list[:i]: # 중복 제거
                    # 버튼 생성 (pushbutton)
                    btns_minus.append(QPushButton('-', self))
                    btns_add.append(QPushButton('+', self))
                    btns_input.append(QPushButton('수량입력', self))
                    btns_cancel.append(QPushButton('x', self))

                    self.cart_table.setCellWidget(row_int, 2, btns_minus[row_int])
                    self.cart_table.setCellWidget(row_int, 3, btns_add[row_int])
                    self.cart_table.setCellWidget(row_int, 4, btns_input[row_int])
                    self.cart_table.setCellWidget(row_int, 7, btns_cancel[row_int])

                    # Signal: 버튼 클릭시 연결문
                    btns_minus[row_int].clicked.connect(lambda: self.minus_menu_in_cart(cal.cart_list[i]))
                    btns_add[row_int].clicked.connect(lambda: self.add_menu_in_cart(cal.cart_list[i]))
                    btns_input[row_int].clicked.connect(lambda: self.input_menu_in_cart(cal.cart_list[i]))
                    btns_cancel[row_int].clicked.connect(lambda: self.cancel_menu_in_cart(cal.cart_list[i]))

                    # 메뉴 정보 불러오기 (메뉴명, 수량, 단가, 금액)
                    self.cart_table.setItem(row_int, 0, QTableWidgetItem(cal.cart_list[i]))
                    self.cart_table.setItem(row_int, 1, QTableWidgetItem(str(cal.return_menu_qty(cal.cart_list[i]))))
                    self.cart_table.setItem(row_int, 5, QTableWidgetItem(str(cal.return_menu_cost(cal.cart_list[i]))))
                    self.cart_table.setItem(row_int, 6, QTableWidgetItem(str(cal.return_menu_amount(cal.cart_list[i]))))

                    # 장바구니 테이블 row 세팅
                    row_int += 1

    @pyqtSlot(str)
    def add_menu_in_cart(self, menu_str): # 메뉴 추가 & 테이블 그리기
        cal.add_qty(menu_str)
        self.set_item_in_cart_table()

    @pyqtSlot(str)
    def minus_menu_in_cart(self, menu_str): # 메뉴 감소 & 테이블 그리기
        cal.minus_qty(menu_str)
        self.set_item_in_cart_table()

    @pyqtSlot(str)
    def input_menu_in_cart(self, menu_str): # 메뉴 직접입력 (inputdialog) & 테이블 그리기
        input_int, ok = QInputDialog.getInt(self, '수량 직접입력', menu_str + '의 수량을 입력하세요.', min=0)
        if ok:
            cal.input_qty(menu_str, input_int)
            self.set_item_in_cart_table()

    @pyqtSlot(str)
    def cancel_menu_in_cart(self, menu_str): # 메뉴 취소 & 테이블 그리기
        cal.cancel_qty(menu_str)
        self.set_item_in_cart_table()

    @pyqtSlot()
    def cancel_all_in_cart(self): # 전체 취소 & 테이블 그리기
        cal.cancel_all_qty()
        self.set_item_in_cart_table()

    @pyqtSlot()
    def print_bill_of_recent_order(self): # 영수증출력 (messagebox)
        msg = QMessageBox.information(self, '영수증출력', str(rec.receipt_df), QMessageBox.Ok, QMessageBox.Ok)

    @pyqtSlot()
    def pay_in_cash(self): # 현금 결제 (inputdialog, messagebox)
        if len(cal.cart_list) == 0:
            # 장바구니에 아무것도 없을 시 warning
            self.warn_pay_zero()
        else:
            # 고객에게 받은 금액을 입력
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
                    # 결제 완료 함수 호출
                    self.complete_payment('현금')

    @pyqtSlot()
    def pay_in_credit_card(self): # 카드 결제 (messagebox)
        if len(cal.cart_list) == 0:
            # 장바구니에 아무것도 없을 시 warning
            self.warn_pay_zero()
        else:
            reply = QMessageBox.question(self, '카드결제',
                                         '결제할 금액: ' + str(cal.return_total_amount()) + '원' + '\n' + '카드로 결제합니까?',
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if reply == QMessageBox.Yes:
                # 결제 완료 함수 호출
                self.complete_payment('카드')

    @pyqtSlot()
    def warn_pay_zero(self): # 장바구니에 아무것도 없을 시 warning (messagebox)
        msg = QMessageBox.information(self, '결제금액 경고', '결제금액은 0원일 수 없습니다.',
                                      QMessageBox.Ok, QMessageBox.Ok)

    @pyqtSlot(str)
    def complete_payment(self, payment_method_str): # 결제 완료 (messagebox) & 테이블 그리기
        # 주문접수 모듈 연결
        rec.receive_order(payment_method_str)
        # 결제완료 messagebox 팝업
        msg = QMessageBox.information(self, '결제완료', '결제수단: ' + payment_method_str + '\n' + '결제가 완료되었습니다.',
                                      QMessageBox.Ok, QMessageBox.Ok)
        # 장바구니 테이블 그리기
        self.set_item_in_cart_table()


# Tab Widget: 내역조회
class SecondTab(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        grid = QGridLayout()
        # 기능별 그룹박스 생성 (groupbox)
        grid.addWidget(self.create_choice_groupbox(), 0, 0)
        grid.addWidget(self.create_view_groupbox(), 0, 1)

        self.setLayout(grid)

    # Groupbox: 주문결제내역
    def create_choice_groupbox(self):
        gbox = QGroupBox()
        gbox.setTitle('주문결제내역')
        vbox = QVBoxLayout()

        # 버튼 생성 (pushbutton)
        btn_update = QPushButton('새로고침', self)
        vbox.addWidget(btn_update)
        # Signal: 버튼 클릭시 연결문
        btn_update.clicked.connect(self.set_item_in_order_history_table)

        # 주문내역 테이블 생성 (tablewidget)
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

        # 세부내역 테이블 생성 (tablewidget)
        self.order_details_table = QTableWidget()
        self.create_order_details_table()
        vbox.addWidget(self.order_details_table)

        gbox.setLayout(vbox)

        return gbox

    # Table Widget: 조회할 주문 선택
    def create_order_history_table(self):
        # 주문내역 테이블 기본 설정 (tablewidget): col 길이, header label
        self.order_history_table.setColumnCount(len(rec.summary_cols_list))
        self.order_history_table.setHorizontalHeaderLabels(rec.summary_cols_list)
        # 테이블에서 직접 수정 불가/cell 선택시 해당 row 선택/다중선택 불가 설정
        self.order_history_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.order_history_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.order_history_table.setSelectionMode(QAbstractItemView.SingleSelection)

    # Table Widget: 상세조회
    def create_order_details_table(self):
        # 세부내역 테이블 기본 설정 (tablewidget): row 길이, col 길이, header label
        self.order_details_table.setColumnCount(len(rec.details_cols_list))
        self.order_details_table.setHorizontalHeaderLabels(rec.details_cols_list)
        self.order_details_table.setRowCount(len(menu_excel['메뉴명']))
        # 테이블에서 직접 수정 불가능하게 설정
        self.order_details_table.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def set_item_in_order_history_table(self):
        # 주문내역 테이블 내용 지우기
        self.order_history_table.clearContents()
        # 주문내역 테이블 row 길이 세팅
        self.order_history_table.setRowCount(rec.summary_ws.max_row - 1)

        # 주문내역 worksheet(summary_ws)를 주문내역 테이블로 불러오기
        order_history_list = []
        for row in rec.summary_ws.iter_rows(min_row=2, values_only=True):
            order_history_list.append(row)

        for i in range(rec.summary_ws.max_row - 1):
            self.order_history_table.setItem(i, 0, QTableWidgetItem(order_history_list[i][0]))
            self.order_history_table.setItem(i, 1, QTableWidgetItem(str(order_history_list[i][1])))
        # Signal: 셀 클릭 시 연결 (세부내역 테이블 그리기)
        self.order_history_table.cellClicked.connect(self.set_item_in_order_details_table)

    @pyqtSlot(int, int)
    def set_item_in_order_details_table(self, row_int, col):
        # 세부내역 테이블 내용 지우기
        self.order_details_table.clearContents()

        # 세부내역 worksheet(detail_ws) 불러오기
        order_datetime_list = []
        order_details_list = []
        for row in rec.details_ws.iter_rows(min_row=2, values_only=True):
            order_datetime_list.append(row[0])
            order_details_list.append(row)

        # 세부내역 worksheet(detail_ws)에서 원하는 주문정보만 불러오기
        order_datetime = rec.summary_ws['A'][row_int + 1].value # 주문일시
        order_index = order_datetime_list.index(order_datetime) # 주문일시 index
        order_count = order_datetime_list.count(order_datetime) # 주문일시 count
        order_details_2_list = order_details_list[order_index: order_index + order_count]
        # 세부내역 테이블 row 길이 세팅
        self.order_details_table.setRowCount(order_count)

        # 해당 주문정보를 세부내역 테이블에 불러오기
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
        # 기능별 그룹박스 생성 (groupbox)
        grid.addWidget(self.create_choice_groupbox(), 0, 0)
        grid.addWidget(self.create_view_groupbox(), 0, 1)

        self.setLayout(grid)

    # Groupbox : 기간 선택
    def create_choice_groupbox(self):
        gbox = QGroupBox()
        hbox = QHBoxLayout()
        vbox = QVBoxLayout()
        hbox2 = QHBoxLayout()

        # 위젯 생성 (pushbutton, label, dateedit)
        lbl_period = QLabel('조회기간')
        self.dateed_start = QDateEdit() # 시작일
        lbl_mark = QLabel('~')
        self.dateed_end = QDateEdit() # 종료일
        self.dateed_start.setDate(QDate.currentDate()) # default: 오늘
        self.dateed_end.setDate(QDate.currentDate()) # default: 오늘
        self.dateed_start.setCalendarPopup(True) # 달력 팝업
        self.dateed_end.setCalendarPopup(True) # 달력 팝업
        btn_week = QPushButton('1주')
        btn_view = QPushButton('조회')
        # Signal: 버튼 클릭시 연결
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
        gbox.setTitle('조회')
        vbox = QVBoxLayout()
        # 매출집계 테이블 생성 (tablewidget)
        self.sales_stats_table = QTableWidget()
        self.create_sales_stats_table()
        vbox.addWidget(self.sales_stats_table)
        gbox.setLayout(vbox)

        return gbox


    @pyqtSlot()
    def change_week_period(self):
        # 조회기간 1주일 설정 (시작일 = 종료일-6)
        self.dateed_start.setDate(self.dateed_end.date().addDays(-6))

    @pyqtSlot()
    def lookup_period_sales(self):
        # 기간별 매출집계 조회
        if self.dateed_end.date() < self.dateed_start.date():
            # 시작일이 종료일보다 늦을 경우 warning
            self.warn_period()
        else:
            # 입력된 시작일/종료일(QDate)을 datetime.date type으로 변환 후 모듈 연결
            stats.stats_period_sales(self.dateed_start.date().toPyDate(), self.dateed_end.date().toPyDate())
            # 매출집계 테이블 그리기
            self.set_item_in_sales_stats_table()
            # 매출집계 그래프 그리기 (barplot)
            ax = stats.stats_df.plot(kind='bar', title='기간별 매출액 비교', rot=0,
                                     x='매출일시', y=['매출총액', '현금매출', '카드매출'],
                                     color=['royalblue', 'darkslateblue', 'slateblue'])
            plt.show()

    @pyqtSlot()
    def warn_period(self): # 시작일이 종료일보다 늦을 경우 warning (messagebox)
        msg = QMessageBox.information(self, '조회기간 경고', '시작일은 종료일보다 나중일 수 없습니다.',
                                      QMessageBox.Ok, QMessageBox.Ok)

    def create_sales_stats_table(self):
        # 매출집계 테이블 기본 설정 (tablewidget): col 길이, header label
        self.sales_stats_table.setColumnCount(len(stats.stats_cols_list))
        self.sales_stats_table.setHorizontalHeaderLabels(stats.stats_cols_list)
        # 테이블에서 직접 수정 불가능하게 설정
        self.sales_stats_table.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def set_item_in_sales_stats_table(self):
        # 매출집계 테이블 내용 지우기
        self.sales_stats_table.clearContents()
        # 매출집계 테이블 row 길이 세팅
        self.sales_stats_table.setRowCount(self.dateed_start.date().daysTo(self.dateed_end.date()) + 1)
        # 기간별 매출집계 dataframe 불러오기
        for i in range(self.sales_stats_table.rowCount()):
            self.sales_stats_table.setItem(i, 0, QTableWidgetItem(stats.stats_df['매출일시'][i]))
            self.sales_stats_table.setItem(i, 1, QTableWidgetItem(str(stats.stats_df['매출건수'][i])))
            self.sales_stats_table.setItem(i, 2, QTableWidgetItem(str(stats.stats_df['매출수량'][i])))
            self.sales_stats_table.setItem(i, 3, QTableWidgetItem(str(stats.stats_df['매출총액'][i])))
            self.sales_stats_table.setItem(i, 4, QTableWidgetItem(str(stats.stats_df['현금매출'][i])))
            self.sales_stats_table.setItem(i, 5, QTableWidgetItem(str(stats.stats_df['카드매출'][i])))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())