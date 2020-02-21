# initialize_dev

import pandas as pd
from datetime import datetime

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
        self.order_now_list = []

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
        self.menu_tot()
        total.order_now()
        total.tot_qt()
        total.tot_sum()



#전체 수량, 총액 class
class Total:
    def __init__(self):
        # 메뉴별 수량/금액 리스트, 전체 수량, 총액 변수 정의
        self.qt = 0
        self.sum = 0
        self.qt_list = []
        self.tot_list = []
        self.order_now_list = []

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

    # 현재 주문 상황
    def order_now(self):
        if self.qt == 0:
            self.order_now_list = []
        else:
            for i in range(len(menu_list)):
                if menu_list[i].qt != 0 and menu_list[i].name not in self.order_now_list:
                    self.order_now_list.append(menu_list[i].name)
                elif menu_list[i].qt == 0 and menu_list[i].name in self.order_now_list:
                    self.order_now_list.remove(menu_list[i].name)

        return self.order_now_list

# 주문 class
class Order:
    def __init__(self):
        # 주문번호 변수/리스트, df columns, 전체 주문내역 정의
        self.order_idx = 0
        self.order_idx_list = []

        self.cols_list = ['주문번호', '주문일시', '메뉴명', '수량', '단가', '금액']
        self.order_df = pd.DataFrame(columns=self.cols_list)
        self.history_df = pd.DataFrame(columns=self.cols_list)

    # 주문접수
    def orderOccur(self):
        self.order_idx += 1
        self.order_idx_list.append(self.order_idx)
        self.now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.order_df = pd.DataFrame(columns=self.cols_list)

        # 메뉴 수량이 0이 아닐 때 주문정보를 현재 주문내역에 append
        for i in range(len(menu_list)):
            if menu_list[i].qt != 0:
                temp_list = [self.order_idx, self.now_str,
                             menu_list[i].name, menu_list[i].qt, menu_list[i].cost, menu_list[i].tot]
                self.order_df = self.order_df.append(pd.DataFrame([temp_list],
                                 columns=self.cols_list), ignore_index=True)

        # 현재 주문내역을 전체 주문내역과 concatenate
        self.history_df = pd.concat([self.history_df, self.order_df], ignore_index=True)

        # 전체취소 call
        americano.tot_cancel()

        return self.order_df


# instance 정의
americano = Menu(0)
latte = Menu(1)
iceamericano = Menu(2)
icelatte = Menu(3)

menu_list = [americano, latte, iceamericano, icelatte]

total = Total()

order = Order()