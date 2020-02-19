# initialize_dev

# menu_excel load
import pandas as pd

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

        # 메뉴 금액, 전체 수량, 총액 변경 함수 call
        self.menu_tot()
        total.tot_qt()
        total.tot_sum()

        return self.qt

    # 메뉴 하나의 수량 직접입력
    def menu_qt_input(self, num):
        self.qt = num

        # 메뉴 금액, 전체 수량, 총액 변경 함수 call
        self.menu_tot()
        total.tot_qt()
        total.tot_sum()

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

        self.menu_tot()
        total.tot_qt()
        total.tot_sum()



#전체 수량, 총액 class
class Total:
    def __init__(self):
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


# 주문내역 class
class Sales:
    def __init__(self):
        self.order_idx = 0
        self.order_list = []
        self.cols_list = ['주문번호', '메뉴명', '단가', '수량', '금액']
        self.history_df = pd.DataFrame(columns=self.cols_list)

    def orderOccur(self):
        self.order_idx += 1
        self.order_list.append(self.order_idx)

        self.order_df = pd.DataFrame(columns=self.cols_list)

        for i in range(len(menu_list)):
            if menu_list[i].qt != 0:
                temp_list = [self.order_idx, menu_list[i].name, menu_list[i].cost,
                             menu_list[i].qt, menu_list[i].tot]
                self.order_df = self.order_df.append(pd.DataFrame([temp_list],
                                 columns=self.cols_list), ignore_index=True)

        self.history_df = pd.concat([self.history_df, self.order_df], ignore_index=True)

        americano.tot_cancel()

        return self.order_df


# instance 정의
americano = Menu(0)
latte = Menu(1)
iceamericano = Menu(2)
icelatte = Menu(3)

menu_list = [americano, latte, iceamericano, icelatte]

total = Total()

sales = Sales()