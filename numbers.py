# Some functional style code. There are prime numbers iterator and generator,
# time function decorator and some filtering functions which are applied to decorators.

import time
from math import sqrt


class PrimeNumbers:

    def __init__(self, limit_number):
        self.end_number = limit_number
        self.prime_numbers = []
        self.iterator = 1
        self.start = 2

    def __iter__(self):
        self.iterator = 1

        return self

    def __next__(self):
        self.iterator += 1

        for num in range(self.start, self.end_number+1):
            self.start = num+1
            for prime in self.prime_numbers:
                if num % prime == 0:
                    break
            else:
                self.prime_numbers.append(num)
                return num

            if num >= self.end_number:
                print(len(self.prime_numbers))
                raise StopIteration


def time_tracker(some_function):
    def derivative(*args, **kwargs):
        start = time.time()
        result = list(some_function(*args, **kwargs))
        time_taken = round(time.time() - start, 5)
        print(f"{time_taken} секунд")
        return result
    return derivative


@time_tracker
def prime_numbers_generator(n):
    yield 2
    prime_numbers = [2]
    sqrt_num = sqrt(n)
    for num in range(3, n+1, 2):
        for prime in prime_numbers:
            if num % prime == 0:
                break
        else:
            yield num
            if sqrt_num > num:
                prime_numbers.append(num)


def lucky_numbers(n):
    lucky_nmb = str(n)
    lucky_nmb_len = len(lucky_nmb)
    cntr = (lucky_nmb_len - lucky_nmb_len % 2) // 2

    left_path, right_path = lucky_nmb[:cntr], lucky_nmb[-cntr:]

    left_nmb_sum = sum([int(n) for n in left_path])
    right_nmb_sum = sum([int(n) for n in right_path])

    if left_nmb_sum == right_nmb_sum:
        return True
    else:
        return False


def palindrome_numbers(n):
    palindrome_nmb = str(n)
    palindrome_len = len(palindrome_nmb)
    cntr = (palindrome_len - palindrome_len % 2) // 2

    if palindrome_nmb[:cntr] == palindrome_nmb[-cntr:]:
        return True
    else:
        return False


def armstrong_numbers(n):
    armstrong_nmb = str(n)
    result = 0
    for digit in armstrong_nmb:
        result += int(digit) ** len(armstrong_nmb)
    if result == n:
        return True
    else:
        return False


def lucky_prime_numbers_generator(n):
    for num in prime_numbers_generator(n):
        lucky_nmb = str(num)
        lucky_nmb_len = len(lucky_nmb)
        cntr = (lucky_nmb_len - lucky_nmb_len % 2) // 2
        left_part, right_part = lucky_nmb[:cntr], lucky_nmb[-cntr:]

        left_nmb_sum = sum([int(n) for n in left_part])
        right_nmb_sum = sum([int(n) for n in right_part])

        if left_nmb_sum == right_nmb_sum:
            yield num


def palindrome_prime_generator(n):
    for num in prime_numbers_generator(n):
        palindrome_nmb = str(num)
        palindrome_len = len(palindrome_nmb)
        cntr = (palindrome_len - palindrome_len % 2) // 2

        if palindrome_nmb[:cntr] == palindrome_nmb[-cntr:]:
            yield num


def armstrong_prime_generator(n):
    for num in prime_numbers_generator(n):
        armstrong_nmb = str(num)
        result = 0
        for digit in armstrong_nmb:
            result += int(digit) ** len(armstrong_nmb)
        if result == num:
            yield num


def mega_hell_generator_v666(n, functio_list=None):
    prime_numbers = []
    for num in range(2, n+1):
        if not num == 2 and num % 2 == 0:
            continue

        for prime in prime_numbers:
            if prime < sqrt(num):
                if num % prime == 0:
                    break
        else:
            prime_numbers.append(num)
            if functio_list is not None:
                all_functio_true = 0
                for functio in functio_list:
                    if functio(num):
                        all_functio_true += 1
                if all_functio_true == len(functio_list):
                    yield num
            else:
                yield num


numbers1 = prime_numbers_generator(n=10000)
numbers2 = prime_numbers_generator(n=10000)
numbers3 = prime_numbers_generator(n=10000)
print(list(filter(lucky_numbers, numbers1)))
print(list(filter(palindrome_numbers, numbers2)))
print(list(filter(armstrong_numbers, numbers3)))


functions_list = [lucky_numbers, palindrome_numbers, armstrong_numbers]

off_we_go = mega_hell_generator_v666(n=10000, functio_list=functions_list[:2])
for ultimate_number in off_we_go:
    print(ultimate_number)

off_we_go_again = mega_hell_generator_v666(n=10000, functio_list=functions_list)
for even_more_ultimate_number in off_we_go_again:
    print(even_more_ultimate_number)


number_generator = lucky_prime_numbers_generator(n=100000)
for number in number_generator:
    print(number)

palindrome_generator = palindrome_prime_generator(n=10000)
for number in palindrome_generator:
    print(number)

armstrong_generator = armstrong_prime_generator(n=10000)
for number in armstrong_generator:
    print(number)
