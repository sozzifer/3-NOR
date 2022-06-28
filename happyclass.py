import numpy as np
from matplotlib import pyplot as plt


class Happy():
    def __init__(self, df, column1, column2, value):
        self.data = df[column1][df[column2] == value].reset_index(drop=True)
        self.column1 = column1
        self.column2 = column2
        self.value = value
        self.mean = round(self.data.describe()["mean"], 3)
        self.min = self.data.describe()["min"]
        self.q1 = self.data.describe()["25%"]
        self.median = self.data.describe()["50%"]
        self.q3 = self.data.describe()["75%"]
        self.max = self.data.describe()["max"]
        self.count = int(self.data.describe()["count"])
        self.iqr = self.data.describe()["75%"] - self.data.describe()["25%"]
        self.std = round(self.data.describe()["std"], 3)
        self.skew = round(self.data.skew(), 3)
        self.sem = round(self.data.sem(), 3)

    def __repr__(self):
        return f"Dataset:\n{self.data}\n\
                 \nColumn 1: {self.column1}\
                 \nColumn 2: {self.column2}\
                 \nValue: {self.value}\
                 \nCount: {self.count}\
                 \nMean: {self.mean}\
                 \nStandard deviation: {self.std}\
                 \nMinimum: {self.min}\
                 \nQ1: {self.q1}\
                 \nMedian: {self.median}\
                 \nQ3: {self.q3}\
                 \nMaximum: {self.max}\
                 \nInterquartile range{self.iqr}\
                 \nSkewness: {self.skew}\
                 \nSE Mean: {self.sem}\
                 \n\n"

    def graphical(data1, data2):
        # To add: code to adjust bins, x-ticks, x-tick labels, y-ticks, boxplot labels; toggle lines on/off; key for mean/median/IQR/SD colours
        fig, axs = plt.subplots(nrows=2, ncols=2, figsize=(6, 6))
        x_ticks = range(0, 31, 10)
        x_labels = ["0", "10", "20", "30"]
        y_ticks = np.arange(0, 0.14, 0.02)
        fig.suptitle(f"Is {data1.column1} dependent on {data1.column2}?")

        axs[0, 0].hist(data1.data, density=True, linewidth=0.8,
                       color="white", edgecolor="black", bins=12, zorder=1, alpha=0.5)
        axs[0, 0].set_title(f"\nCount = {data1.count}\n{data1.value}")
        axs[0, 0].set_ylabel("Frequency")
        axs[0, 0].axvline(data1.q1, color="green", linewidth=1.5, zorder=0)
        axs[0, 0].axvline(data1.median, color="red", linewidth=1.5, zorder=0)
        axs[0, 0].axvline(data1.mean, color="orange", linewidth=1.5, zorder=0)
        axs[0, 0].axvline(data1.q3, color="green", linewidth=1.5, zorder=0)
        axs[0, 0].axvline(data1.mean +
                          data1.std, color="blue", linewidth=1.5, zorder=0)
        axs[0, 0].axvline(data1.mean -
                          data1.std, color="blue", linewidth=1.5, zorder=0)
        axs[0, 0].set_xticks(x_ticks)
        axs[0, 0].set_xticklabels(x_labels)
        axs[0, 0].set_yticks(y_ticks)

        axs[0, 1].hist(data2.data, density=True, linewidth=0.8,
                       color="white", edgecolor="grey", bins=12)
        axs[0, 1].set_title(f"\nCount = {data2.count}\n{data2.value}")
        axs[0, 1].set_ylabel("Frequency")
        axs[0, 1].axvline(data2.q1, color="green", linewidth=1.5)
        axs[0, 1].axvline(data2.median, color="red", linewidth=1.5)
        axs[0, 1].axvline(data2.mean, color="orange", linewidth=1.5)
        axs[0, 1].axvline(data2.q3, color="green", linewidth=1.5)
        axs[0, 1].axvline(data2.mean +
                          data2.std, color="blue", linewidth=1.5)
        axs[0, 1].axvline(data2.mean -
                          data2.std, color="blue", linewidth=1.5)
        axs[0, 1].set_xticks(x_ticks)
        axs[0, 1].set_xticklabels(x_labels)
        axs[0, 1].set_yticks(y_ticks)

        axs[1, 0].boxplot(data1.data, labels=data1.value, vert=False, boxprops=dict(color="green", linewidth=1.5), medianprops=dict(
            color='red', linewidth=1.5), meanprops=dict(color="orange", linestyle="-", linewidth=1.5), showmeans=True, meanline=True)
        axs[1, 0].axvline(data1.mean +
                          data1.std, color="blue", linewidth=1.5, ymin=0.425, ymax=0.575)
        axs[1, 0].axvline(data1.mean -
                          data1.std, color="blue", linewidth=1.5, ymin=0.425, ymax=0.575)
        axs[1, 0].set_xticks(x_ticks)

        axs[1, 1].boxplot(data2.data, labels=data2.value, vert=False, boxprops=dict(color="green", linewidth=1.5), medianprops=dict(
            color='red', linewidth=1.5), meanprops=dict(color="orange", linestyle="-", linewidth=1.5), showmeans=True, meanline=True)
        axs[1, 1].axvline(data2.mean +
                          data2.std, color="blue", linewidth=1.5, ymin=0.425, ymax=0.575)
        axs[1, 1].axvline(data2.mean -
                          data2.std, color="blue", linewidth=1.5, ymin=0.425, ymax=0.575)
        axs[1, 1].set_xticks(x_ticks)
        plt.subplots_adjust(wspace=0.5)
        plt.show()
