# initialize_totsumqt

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

        total.tot_qt(self.qt)

        return self.qt

    # 메뉴 금액 계산
    def menu_tot(self):
        self.tot = self.qt * self.cost

        total.tot_sum(self.tot)

        return self.tot


# menu class instance 정의
americano = Menu(0)
latte = Menu(1)
iceamericano = Menu(2)
icelatte = Menu(3)


#전체 수량, 총액 class
class Total:
    def __init__(self):
        self.qt = 0
        self.sum = 0

    def tot_qt(self, qt):
        self.qt += qt

        return self.qt

    def tot_sum(self, tot):
        self.sum += tot

        return self.sum

total = Total()