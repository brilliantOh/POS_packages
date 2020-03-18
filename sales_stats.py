# sales_stats.py

from datetime import date
from receipt import Receipt, rec
import openpyxl as xl


class Sales_statistics:
    def __init__(self):
        self.date_start = date.today()
        self.date_end = date.today()

    def stats_period_sales(self, start_date, end_date):
        order_count_list = []
        total_quantity_list = []
        total_amount_list = []

        for day in range(end_date - start_date):
            pass


stats = Sales_statistics()