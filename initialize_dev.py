# initialize_dev

# menu_excel load
import pandas as pd

filepath = './menu_excel.xlsx'
menu_excel = pd.read_excel(filepath)


# menu class
class Menu:
    def __init__(self, idx):
        # instance attribute 정의
        self.name = menu_excel['메뉴명'][idx]
        self.cost = menu_excel['가격'][idx]
        self.qt = 0
        self.tot = 0

    # 수량 변경/취소
    def menu_qt(self, num):
        # 음수 처리
        if self.qt + num < 0:
            self.qt = 0
        # 수량 취소
        elif num == 0:
            self.qt = 0
        else:
            self.qt += num

        # 메뉴 금액, 전체 수량, 총 금액 변경 함수 call
        self.menu_tot()
        total.tot_qt()
        total.tot_sum()

        return self.qt

    # 메뉴 금액 계산
    def menu_tot(self):
        self.tot = self.qt * self.cost

        return self.tot


#전체 수량, 총액 class
class Total:
    def __init__(self):
        self.qt = 0
        self.sum = 0
        self.menu_list = [americano, latte, iceamericano, icelatte]
        self.qt_list = []
        self.tot_list = []

        for i in range(len(self.menu_list)):
            self.qt_list.append(0)
            self.tot_list.append(0)

    def tot_qt(self):
        for i in range(len(self.menu_list)):
            self.qt_list[i] = self.menu_list[i].qt

        self.qt = sum(self.qt_list)

        return self.qt

    def tot_sum(self):
        for i in range(len(self.menu_list)):
            self.tot_list[i] = self.menu_list[i].tot

        self.sum = sum(self.tot_list)

        return self.sum

# instance 정의
americano = Menu(0)
latte = Menu(1)
iceamericano = Menu(2)
icelatte = Menu(3)

total = Total()