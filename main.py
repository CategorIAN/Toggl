from TogglTime import TogglTime
from itertools import product

def f(i):
    if i == 1:
        T = TogglTime()
        for (year, month) in product(T.years, T.months):
            print("----------------------------------")
            print("The year is 20{}.".format(year))
            print("The month is {}.".format(month))
            print(T.dataFrame(year, month))
            print(T.yearResults('19'))

    if i == 2:
        T = TogglTime()
        T.yearResults('22')

    if i == 3:
        T = TogglTime()
        T.show('22')

if __name__ == '__main__':
    f(3)
