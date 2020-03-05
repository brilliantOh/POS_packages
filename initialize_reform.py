# initialize_reform

import os
import pandas as pd

# load menu data by pandas
excel_path = r'D:\Documents\repository'
excel_name = 'menu_excel.xlsx'
menu_excel = pd.read_excel(excel_path + os.sep + excel_name, index_col=None, header=0)

# calculate menu quantity
class POS_calculator:
    def __init__(self):
        self.cart_list = []

    def add_qty(self, menu_str):
        self.cart_list.append(menu_str)
        return self.cart_list

    def minus_qty(self, menu_str):
        if self.cart_list.count(menu_str) != 0:
            self.cart_list.remove(menu_str)
            return self.cart_list

    def cancel_qty(self, menu_str):
        while self.cart_list.count(menu_str) != 0:
            self.cart_list.remove(menu_str)
        return self.cart_list

    def input_qty(self, menu_str, input_int):
        while self.cart_list.count(menu_str) != input_int:
            self.cart_list.append(menu_str)
        return self.cart_list

    def cancel_all_qty(self):
        self.cart_list.clear()
        return self.cart_list

    def return_menu_qty(self, menu_str):
        return self.cart_list.count(menu_str)

    def return_total_qty(self):
        return len(self.cart_list)

    def return_menu_amount(self, menu_str):
        for i in range(len(menu_excel['메뉴명'])):
            if menu_str == menu_excel['메뉴명'][i]:
                return self.cart_list.count(menu_str) * menu_excel['가격'][i]

    def return_total_amount(self):
        total_amount_int = 0

        for i in range(len(set(self.cart_list))):
            total_amount_int += self.return_menu_amount(list(set(self.cart_list))[i])

        return total_amount_int

    def return_menu_cost(self, menu_str):
        for i in range(len(menu_excel['메뉴명'])):
            if menu_str == menu_excel['메뉴명'][i]:
                return menu_excel['가격'][i]


cal = POS_calculator()


# create variable in convenience
menu_names_list = []
for cell in menu_excel['메뉴명']:
    menu_names_list.append(cell)

menu_cost_dic = {}
for i in range(len(menu_excel['메뉴명'])):
    menu_cost_dic[menu_excel['메뉴명'][i]] = menu_excel['가격'][i]
