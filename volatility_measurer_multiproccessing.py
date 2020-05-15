# Multiprocessing version of volatility measurer.

import multiprocessing

from vol_measure_additions import to_prepare, to_result


class Ticker(multiprocessing.Process):

    def __init__(self, file_in, data_storage, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.file_in = file_in
        self.minimum_price = 10000
        self.maximum_price = 0
        self.average_price = 0
        self.volatility = 0
        self.security_ticker = None
        self.data_storage = data_storage

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
        self.data_storage.put([self.security_ticker, self.volatility])


def main():
    processes_data_bank = multiprocessing.Queue()
    tickers_data = []
    files = to_prepare("vol_measure_trades")
    tickers = [Ticker(data_storage=processes_data_bank, file_in=file_in) for file_in in files]

    for ticker in tickers:
        ticker.start()

    for ticker in tickers:
        ticker.join()

    while not processes_data_bank.empty():
        tickers_data.append(processes_data_bank.get())

    to_result(tickers_data)


if __name__ == "__main__":
    main()
