# practice.py

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

import random
from sales_stats import Sales_statistics, stats


class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

    def plot(self):
        self.fig.clear()

        #data = [random.random() for i in range(25)]
        data = stats.stats_df['매출총액'].tolist()
        ax = self.figure.add_subplot(111)
        ax.plot(data, 'r-')
        ax.set_title('practice')
        self.draw()
