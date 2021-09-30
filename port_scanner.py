import multiprocessing
import socket
import requests


class ToConnect(multiprocessing.Process):

    def __init__(self, storage, pair, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.storage = storage
        self.pair = pair

    def get_server_engine(self):
        response = requests.get(f"http://{self.pair[0]}:{self.pair[1]}/")
        return response.headers.get("Server")

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(0.5)

            try:
                sock.connect(self.pair)
                if self.pair[1] == 80 or self.pair[1] == 443:
                    server_engine = self.get_server_engine()

                    if len(server_engine) < 1:
                        server_engine = "empty_string"

                    self.storage.put((self.pair[0], self.pair[1], "OPEN", f"SERVER: {server_engine}"))
                else:
                    self.storage.put((self.pair[0], self.pair[1], "OPEN"))
            except Exception:
                pass


class PortScanner:
    def __init__(self):
        self.some_ip_addresses = []
        self.some_ports = []
        self.ip_n_port_pairs = []
        self.results = []
        self.data_storage = multiprocessing.Queue()

    def get_ip_addresses(self):
        while True:
            ip_address = input("Введите ip-адрес. Если все ip-адреса введены, введите Y/y. >>>: ")

            if "Y" in ip_address or "y" in ip_address:
                break

            self.some_ip_addresses.append(ip_address)

    def get_ports(self):
        while True:
            port = input("Введите порт. Если все порты введены, введите Y/y. >>>: ")

            if "Y" in port or "y" in port:
                break

            self.some_ports.append(int(port))

    def get_ip_port_pairs(self):
        for ip in self.some_ip_addresses:
            for port in self.some_ports:
                self.ip_n_port_pairs.append((ip, port))

    def prepare_threads(self):
        return [ToConnect(self.data_storage, pair) for pair in self.ip_n_port_pairs]

    def get_results(self):
        while not self.data_storage.empty():
            self.results.append(self.data_storage.get())

    def print_out_results(self):
        for result in self.results:
            print(str(result).translate({ord(some_char): None for some_char in "(),'"}))

    def run(self):
        self.get_ip_addresses()
        self.get_ports()
        self.get_ip_port_pairs()

        threads = self.prepare_threads()

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        self.get_results()
        self.print_out_results()


if __name__ == "__main__":
    try:
        PortScanner().run()
    except ValueError:
        print("Ошибка при вводе номера порта.")
