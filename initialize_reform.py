# initialize_reform

import os
import pandas as pd

# load menu data by pandas
excel_path = r'D:\Documents\repository'
excel_name = 'menu_excel.xlsx'
menu_excel = pd.read_excel(excel_path + os.sep + excel_name, index_col=None, header=0)

# create menu names list
menu_names_list = []
for cell in menu_excel['메뉴명']:
    menu_names_list.append(cell)

# calculate menu quantity
class Quantity_calculator:
    def __init__(self):
        self.cart_list = []

    def add_qty(self, menu_str):
        self.cart_list.append(menu_str)

    def minus_qty(self, menu_str):
        if self.cart_list.count(menu_str) != 0:
            self.cart_list.remove(menu_str)

    def cancel_qty(self, menu_str):
        while self.cart_list.count(menu_str) != 0:
            self.cart_list.remove(menu_str)

    def input_qty(self, menu_str, qty_int):
        while self.cart_list.count(menu_str) != qty_int:
            self.cart_list.append(menu_str)

    def cancel_all_qty(self):
        self.cart_list.clear()

cal = Quantity_calculator()

menu_amount_list = []
total_amount_int = 0
menu_qty_list = []
for menu in menu_names_list:
    cal.cart_list.count(menu)

class Amount_calculator:
    def __init__(self):
        self.