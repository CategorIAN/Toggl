import os
import pandas as pd
from functools import reduce
import math
from bokeh.plotting import figure, output_file, show
from bokeh.palettes import magma
import matplotlib.pyplot as plt
from itertools import product


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
        df = df.fillna("")
        f = lambda x, t: x + int(t[0]) * math.pow(1 / 60, int(t[1]))
        g = lambda s: reduce(f, zip(s.split(':'), range(3)), 0)
        df['Duration'] = df['Duration'].map(g)
        df['Billable duration'] = df['Billable duration'].map(g)
        sum_cols = {'Duration': 'sum', 'Billable duration': 'sum'}
        if 'Amount USD' in df.columns: sum_cols['Amount USD'] = 'sum'
        df = df.groupby(by=['Month', 'Project', 'Client'], dropna=False).agg(sum_cols).reset_index(drop=False)
        for (month, project, client) in product(self.months, set(df['Project']), set(df['Client'])):
            if len(df[(df["Month"] == month) & (df["Project"] == project) & (df["Client"] == client)]) == 0:
                df.loc[len(df)] = [month, project, client, 0, 0, 0]
        df = df.sort_values(by = ["Month", "Project", "Client"], axis=0).reset_index(drop=True)
        df.to_csv(self.file + '20' + year + '\\' + "{}.csv".format(year))
        return df

    def show(self, year):
        df = pd.read_csv(self.file + '20' + year + '\\' + "{}.csv".format(year), index_col=0)
        df = df.fillna("")
        projects = ['Exercise', 'Church', 'Work', 'Work']
        clients = ['', '', 'Tutor.com', 'Montana State University']
        colors = ['blue', 'red', 'green', 'yellow']
        for (project, client, color) in zip(projects, clients, colors):
            print(df[(df['Project'] == project) & (df['Client'] == client)]['Duration'])
            plt.plot(self.months, df[(df['Project'] == project) & (df['Client'] == client)]['Duration'],
                     **{'color': color}, label="{}, {}".format(project, client))

        plt.legend()
        plt.xlabel("Month")
        plt.ylabel("Duration (Hours)")
        plt.title("20{} Hours".format(year))
        plt.show()


    """
    for (i, c) in zip([1, 2, 3], [0, 100, 1000000000]):
        ax = plt.subplot(3, 1, i)
        ax.title.set_text('Cost = {}'.format(c))
        plt.plot(P.df['x'], P.df['y'], **{'color': 'blue', 'marker': 'o'}, label='raw data')
        plt.legend()
        ptpartition = P.segmentedLeastSquares(c)
        print(ptpartition)
        fittedPts = ptpartition.fitPoints()
        plt.plot(fittedPts['x'], fittedPts['y'], **{'color': 'red'}, label='fitted')
        plt.legend()
    plt.show()
    """



