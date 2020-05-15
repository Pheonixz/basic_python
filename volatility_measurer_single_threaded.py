# Single-threaded code which calculates volatility of securities using a simple formula
# "(max_price + min_price) / average_price" and then printing out top 3 tickers with the
# lowest and the highest volatility. Also prints out a list of tickers with zero volatility.

from vol_measure_additions import to_prepare, to_result


class Ticker:

    def __init__(self, file_in):
        self.file_in = file_in
        self.minimum_price = 10000
        self.maximum_price = 0
        self.average_price = 0
        self.volatility = 0
        self.security_ticker = None

    def run(self):
        for line in self.file_in:
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

    for file in files:
        with open(file, "r") as in_file:
            ticker = Ticker(in_file)
            ticker.run()
            if ticker.volatility == 0:
                tickers_data_zero.append(ticker.security_ticker)
            else:
                tickers_data_non_zero.append([ticker.security_ticker, ticker.volatility])

    to_result(tickers_data_non_zero, tickers_data_zero)


if __name__ == "main":
    main()
