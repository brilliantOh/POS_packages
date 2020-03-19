# sales_stats.py
from datetime import date, timedelta
import pandas as pd


class Sales_statistics:
    def __init__(self):
        self.order_count_list = []
        self.total_quantity_list = []
        self.total_amount_list = []

    def stats_period_sales(self, start_date, end_date):
        self.order_count_list = []
        self.total_quantity_list = []
        self.total_amount_list = []

        details_df = pd.read_excel('order_history.xlsx', sheet_name='receipt')
        summary_df = pd.read_excel('order_history.xlsx', sheet_name='summary')
        period_int = (end_date - start_date).days

        for i in range(period_int + 1):
            order_date_str = (start_date + timedelta(days=i)).strftime('%Y-%m-%d')
            date_summary_df = summary_df.loc[(summary_df['주문일시'].str.contains(order_date_str)), :]
            date_details_df = details_df.loc[(details_df['주문일시'].str.contains(order_date_str)), :]
            self.order_count_list.append(len(date_summary_df))
            self.total_quantity_list.append(sum(date_details_df['수량']))
            self.total_amount_list.append(sum(date_summary_df['금액']))


stats = Sales_statistics()