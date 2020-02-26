# initialize_dev

import pandas as pd
from datetime import datetime
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows

# menu_excel load
filepath = './menu_excel.xlsx'
menu_excel = pd.read_excel(filepath)


# menu class
class Menu:
    def __init__(self, idx):
        # instance attribute 정의(이름, 가격, 수량, 메뉴 금액)
        self.name = menu_excel['메뉴명'][idx]
        self.cost = menu_excel['가격'][idx]
        self.qt = 0
        self.tot = 0


    # 메뉴 하나의 수량을 변경/취소
    def menu_qt(self, num):
        # 음수 처리
        if self.qt + num < 0:
            self.qt = 0
        # 취소
        elif num == 0:
            self.qt = 0
        else:
            self.qt += num

        self.menu_qt_changed()

        return self.qt

    # 메뉴 하나의 수량 직접입력
    def menu_qt_input(self, num):
        self.qt = num

        self.menu_qt_changed()

        return self.qt

    # 메뉴 하나의 금액 계산
    def menu_tot(self):
        for i in range(len(menu_list)):
            menu_list[i].tot = menu_list[i].qt * menu_list[i].cost

        return self.tot

    # 전체 취소
    def tot_cancel(self):
        for i in range(len(menu_list)):
            menu_list[i].qt = 0

        self.menu_qt_changed()

    # 수량 변동시 call
    def menu_qt_changed(self):
        total.tot_qt()
        cart.cart()
        self.menu_tot()
        total.tot_sum()


#전체 수량, 총액 class
class Total:
    def __init__(self):
        # 메뉴별 수량/금액 리스트, 전체 수량, 총액 변수 정의
        self.qt = 0
        self.sum = 0
        self.qt_list = []
        self.tot_list = []
        for i in range(len(menu_list)):
            self.qt_list.append(0)
            self.tot_list.append(0)

    # 전체 수량 변경
    def tot_qt(self):
        for i in range(len(menu_list)):
            self.qt_list[i] = menu_list[i].qt

        self.qt = sum(self.qt_list)

        return self.qt

    # 총액 계산
    def tot_sum(self):
        for i in range(len(menu_list)):
            self.tot_list[i] = menu_list[i].tot

        self.sum = sum(self.tot_list)

        return self.sum


# 장바구니 class
class Cart:
    def __init__(self):
        self.cart_dic = {}
        self.cart_keys = list(self.cart_dic.keys())

    # 장바구니 관리: dic
    def cart(self):
        if total.qt == 0:
            # 전체 수량이 0
            self.cart_dic = {}
        else:
            for i in range(len(menu_list)):
                if menu_list[i].qt != 0:
                    # 메뉴의 수량이 0이 아닐 때 # dic이라 key 중복 없이 덮어쓰기
                    self.cart_dic[menu_list[i]] = menu_list[i].qt
                else:
                    if menu_list[i] in self.cart_dic:
                        # 메뉴의 수량이 0이고 장바구니에 있을 때
                        del self.cart_dic[menu_list[i]]

        self.cart_keys = list(self.cart_dic.keys())

        return self.cart_dic


# 주문 class
class Order:
    def __init__(self):
        # reset order_idx, dataframe, xlsx
        self.order_idx = 0
        self.order_idx_list = []

        self.cols_list = ['주문번호', '주문일시', '메뉴명', '수량', '단가', '금액']
        self.order_df = pd.DataFrame(columns=self.cols_list)
        self.history_df = pd.DataFrame(columns=self.cols_list)

        self.wb = Workbook()
        self.wb_filename = 'order_history.xlsx'
        self.ws1 = self.wb.active
        self.ws1.title = 'order'
        self.ws1.append(self.cols_list)
        self.wb.save(filename=self.wb_filename)

    # 주문접수
    def orderOccur(self):
        # set order_idx, dataframe
        self.order_idx += 1
        self.order_idx_list.append(self.order_idx)
        self.now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.order_df = pd.DataFrame(columns=self.cols_list)

        for i in range(len(cart.cart_keys)):
            temp_list = [self.order_idx, self.now_str,
                         cart.cart_keys[i].name, cart.cart_keys[i].qt, cart.cart_keys[i].cost, cart.cart_keys[i].tot]
            self.order_df = self.order_df.append(pd.DataFrame([temp_list], columns=self.cols_list), ignore_index=True)

        # concatenate dataframe
        self.history_df = pd.concat([self.history_df, self.order_df], ignore_index=True)

        # 전체취소 call
        americano.tot_cancel()

        # 저장 call
        self.orderSave()

        return self.order_df

    # 주문정보 save(xlsx)
    def orderSave(self):
        for row in dataframe_to_rows(self.order_df, index=False, header=False):
            self.ws1.append(row)
            self.wb.save(filename=self.wb_filename)


# instance 정의
americano = Menu(0)
latte = Menu(1)
iceamericano = Menu(2)
icelatte = Menu(3)

menu_list = [americano, latte, iceamericano, icelatte]

total = Total()
cart = Cart()
order = Order()