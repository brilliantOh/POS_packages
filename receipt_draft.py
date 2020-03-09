# receipt_draft.py

import os
import pandas as pd
import openpyxl as xl
from initialize_reform import POS_calculator, cal
from datetime import datetime
from openpyxl.utils.dataframe import dataframe_to_rows

# receive order and save data(excel)
class Receipt:
    def __init__(self):
        datetime_now_ymd = datetime.now().strftime('%Y%m%d')
        self.header_list = ['주문일시', '메뉴', '수량', '단가', '금액', '지불수단']
        self.receipt_df = pd.DataFrame(columns=self.header_list)

        self.order_history_wb = xl.Workbook()
        self.wb_filename = 'order_history_' + datetime_now_ymd + '.xlsx'
        self.order_history_ws = self.order_history_wb.active
        self.order_history_ws.title = 'receipt'
        self.order_history_ws.append(self.header_list)
        self.order_history_wb.save(filename=self.wb_filename)

    def receive_order(self, payment_method_str):
        self.receipt_df = pd.DataFrame(columns=self.header_list)

        datetime_now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        for i in range(len(set(cal.cart_list))):
            if cal.cart_list[i] not in cal.cart_list[:i]:
                details_list = [datetime_now_str, cal.cart_list[i], cal.return_menu_qty(cal.cart_list[i]),
                                cal.return_menu_cost(cal.cart_list[i]), cal.return_menu_amount(cal.cart_list[i]),
                                payment_method_str]
                self.receipt_df = self.receipt_df.append(pd.DataFrame([details_list], columns=self.header_list),
                                                         ignore_index=True)
        cal.cancel_all_qty()
        self.save_receipt_df_to_excel()

        return self.receipt_df

    def save_receipt_df_to_excel(self):
        for row in dataframe_to_rows(self.receipt_df, index=False, header=False):
            self.order_history_ws.append(row)
            self.order_history_wb.save(filename=self.wb_filename)


rec = Receipt()