# Some util functions for volatility measurer which are moved to a separate module.

import os
import pathlib
from operator import itemgetter


def to_prepare(dirname):
    files_list = None

    for _, _, filez in os.walk(dirname):
        files_list = filez

    files_list = [os.path.normpath(pathlib.Path.cwd() / dirname / f) for f in files_list]

    return files_list


def to_result(data_list1, data_list2=None):

    if data_list2 is not None:
        tickers_non_zero, tickers_zero = data_list1, data_list2
    else:
        tickers_zero = []
        tickers_non_zero = []
        for tic in data_list1:
            if tic[1] == 0:
                tickers_zero.append(tic[0])
            else:
                tickers_non_zero.append(tic)

    tickers_non_zero = sorted(tickers_non_zero, key=itemgetter(1), reverse=True)
    tickers_zero = sorted(tickers_zero)

    print("Максимальная волотильность:")
    for x in range(3):
        ticker_id = tickers_non_zero[x][0]
        volatility = tickers_non_zero[x][1]
        print(f"{ticker_id} - {volatility} %")

    print("Минимальная волотильность:")
    for x in range(3, 0, -1):
        ticker_id = tickers_non_zero[-x][0]
        volatility = tickers_non_zero[-x][1]
        print(f"{ticker_id} - {volatility} %")

    print("Нулевая волотильность:")
    print(tickers_zero)
