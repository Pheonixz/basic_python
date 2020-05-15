# Two variants of a simple log parser, which parses a file of log lines
# and then writes out to console how many events with "NOK" marker occurred
# in each of logged minute.


def generator(file):
    current_time_period = None
    occasions_counter = 0
    for line in file:
        if line.endswith("NOK\n"):
            if current_time_period == line[1:17]:
                occasions_counter += 1
            else:
                yield current_time_period, occasions_counter
                current_time_period = line[1:17]
                occasions_counter = 1


with open("events.txt", "r", encoding="utf8") as f:
    gen = generator(f)
    NOK = (line for line in gen if None not in line)
    for time, event in NOK:
        print(f" [{time}] {event}")


class Iterator:

    def __init__(self, file):
        self.i = 0
        self.file = file
        self.line = None
        self.occasions_counter = 0
        self.current_time_period = None

    def __iter__(self):
        self.i = 0

        return self

    def __next__(self):
        self.i += 1
        self.line = self.file.readline()

        if self.line.endswith("NOK\n"):
            if self.current_time_period == self.line[1:17]:
                self.occasions_counter += 1
            else:
                x, y = self.current_time_period, self.occasions_counter
                self.current_time_period = self.line[1:17]
                self.occasions_counter = 1
                return x, y

        if not self.line:
            raise StopIteration


with open("events.txt", "r", encoding="utf8") as f:
    iterator = Iterator(f)
    NOK = (line for line in iterator if line is not None and not line[0] is None)
    for i in NOK:
        print(f"{i[0]} {i[1]}")