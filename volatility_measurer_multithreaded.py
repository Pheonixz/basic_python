# Мultithreaded version of volatility measurer.

import threading

from vol_measure_additions import to_prepare, to_result


class Ticker(threading.Thread):

    def __init__(self, file_in, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.file_in = file_in
        self.minimum_price = 10000
        self.maximum_price = 0
        self.average_price = 0
        self.volatility = 0
        self.security_ticker = None

    def run(self):
        with open(self.file_in, "r") as file_in:
            for line in file_in:
                line = line.strip().split(",")

                if line[3].isdigit():
                    potential_max_or_min = float(line[2])

                    if potential_max_or_min > self.maximum_price:
                        self.maximum_price = potential_max_or_min
                    if potential_max_or_min < self.minimum_price:
                        self.minimum_price = potential_max_or_min
                    if self.security_ticker is None:
                        self.security_ticker = line[0]

        self.average_price = (self.maximum_price + self.minimum_price) / 2
        self.volatility = round(((self.maximum_price - self.minimum_price) / self.average_price) * 100, 2)


def main():
    tickers_data_non_zero = []
    tickers_data_zero = []

    files = to_prepare("vol_measure_trades")

    tickers = [Ticker(file_in) for file_in in files]

    for ticker in tickers:
        ticker.start()

    for ticker in tickers:
        ticker.join()

    for ticker in tickers:
        if ticker.volatility == 0:
            tickers_data_zero.append(ticker.security_ticker)
        else:
            tickers_data_non_zero.append([ticker.security_ticker, ticker.volatility])

    to_result(tickers_data_non_zero, tickers_data_zero)


if __name__ == "__main__":
    main()
