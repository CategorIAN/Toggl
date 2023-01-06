import os
import pandas as pd
from functools import reduce
import math
from bokeh.plotting import figure, output_file, show
from bokeh.palettes import magma
import matplotlib.pyplot as plt


class TogglTime:
    def __init__(self):
        self.file = os.getcwd() + '\\' + 'Toggl Time' + '\\' + 'Personal Workspace' + '\\'
        self.years = ['19', '20', '21']
        self.months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']

    def dataFrame(self, year, month):
        return pd.read_csv(self.file + '20' + year + '\\' + year + '.' + month + '.csv')

    def yearResults(self, year):
        fileExt = self.file + '20' + year + '\\'
        dfs = []
        for month in self.months:
            df = pd.read_csv(fileExt + "{}.{}.csv".format(year, month))
            df.insert(0, 'Month', month)
            dfs.append(df)
        df = pd.concat(dfs).reset_index(drop=True)
        f = lambda x, t: x + int(t[0]) * math.pow(1 / 60, int(t[1]))
        g = lambda s: reduce(f, zip(s.split(':'), range(3)), 0)
        df['Duration'] = df['Duration'].map(g)
        df['Billable duration'] = df['Billable duration'].map(g)
        sum_cols = {'Duration': 'sum', 'Billable duration': 'sum'}
        if 'Amount USD' in df.columns: sum_cols['Amount USD'] = 'sum'
        df = df.groupby(by=['Month', 'Project', 'Client'], dropna=False).agg(sum_cols).reset_index(drop=False)
        df.to_csv(self.file + '20' + year + '\\' + "{}.csv".format(year))
        return df

    def show(self, year):
        df = self.yearResults(year)
        plt.plot(self.months, df.loc[lambda df: df['Project'] == 'Exercise']['Duration'])
        plt.xlabel("Month")
        plt.ylabel("Duration (Hours)")
        plt.title("Exercise in 20{}".format(year))
        plt.show()



