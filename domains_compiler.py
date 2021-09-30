from copy import copy
import asyncio
import aiohttp


DOMAINS = (
    "com", "ru", "net", "org", "info",
    "cn", "es", "top", "au", "pl", "it",
    "uk", "tk", "ml", "ga", "cf", "us",
    "xyz", "top", "site", "win", "bid"
)

SYMBOLS_SET = (
    "a", "b", "c", "d", "e", "f", "g", "h", "i", "j",
    "k", "l", "m", "n", "o", "p", "q", "r", "s", "t",
    "u", "v", "w", "x", "y", "z", "A", "B", "C", "D",
    "E", "F", "G", "H", "I", "J", "K", "L", "M", "N",
    "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X",
    "Y", "Z", "0", "1", "2", "3", "4", "5", "6", "7",
    "8", "9", "-", "_", ".", "~", "!", "*", "'", "(",
    ")", ";", ":", "@", "&", "=", "+", "$", ",", "/",
    "?", "%", "#", "[", "]"
)

HOMOGLYPHS_DICT = {
    "a": "@",
    "i": "1",
    "I": "l",
    "S": "$",
    "s": "$",
    "O": "0",
}


class DomainsCompiler:

    def __init__(self, keywords_list):
        self.keywords_list = keywords_list
        self.modified_words_list = []
        self.domains_list = []
        self.domains_pairs = {}

    def _add_symbol_at_the_end(self, word):
        for symbol in SYMBOLS_SET:
            self.modified_words_list.append(word + symbol)

    def _change_symbol_for_homoglyph(self, word):
        letters_list = list(word)  # [w, o, r, d]
        for letter in letters_list:
            if letter in HOMOGLYPHS_DICT.keys():
                letters_list[letters_list.index(letter)] = HOMOGLYPHS_DICT[letter]
                self.modified_words_list.append("".join(letters_list))

    def _insert_subdomain(self, word):
        letters_list = list(word)

        for letter in letters_list:
            try:
                if letter.isalpha() and letters_list[letters_list.index(letter) + 1].isalpha():
                    modified_letters_list = copy(letters_list)
                    modified_letters_list.insert(letters_list.index(letter) + 1, ".")
                    modified_word = "".join(modified_letters_list)
                    if not modified_word[0] == ".":
                        self.modified_words_list.append(modified_word)
            except IndexError:
                continue

    def _delete_a_symbol(self, word):
        length = len(word)

        for index in range(length + 1):
            try:
                new_word = copy(word)
                new_word = new_word.replace(new_word[index], "")
                self.modified_words_list.append(new_word)
            except IndexError:
                continue

    def prepare_strategy_list(self):
        return [
            self._add_symbol_at_the_end,
            self._change_symbol_for_homoglyph,
            self._insert_subdomain,
            self._delete_a_symbol
        ]

    def get_domain(self, word):
        for domain in DOMAINS:
            self.domains_list.append(f"http://{word}.{domain}")

    async def get(self, domain, session):
        try:
            async with session.get(url=domain) as resp:
                self.domains_pairs[domain] = resp.request_info.headers.get("Host")
        except Exception:
            pass

    async def main(self):
        async with aiohttp.ClientSession(timeout=0.1) as session:
            await asyncio.gather(*[self.get(domain, session) for domain in self.domains_list])

    def run(self):
        for word in self.keywords_list:
            [strategy(word) for strategy in self.prepare_strategy_list()]
            [self.get_domain(word) for word in self.modified_words_list]

        asyncio.get_event_loop().run_until_complete(self.main())

        return self.domains_pairs


if __name__ == "__main__":
    domain_words = []

    while True:
        domain_word = input("Введите ключевое слово. Если все ключевые слова введены, введите Д/д. >>>: ")

        if "Д" in domain_word or "д" in domain_word:
            break

        domain_words.append(domain_word)

    print(DomainsCompiler(domain_words).run())
