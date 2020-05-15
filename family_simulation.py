# A simple model of a family life written in object oriented style. Using different arguments in the signature of
# simulation function we can check whether all the members of the family will survive during one year period or not.
# The results are printed to console.

# The signature of simulation function has arguments as follows:
# - salary (how much money would the husband earn each time he goes to work
# - number of cats (how many cats do spouses own)
# - sum for shopping (how much money do the wife spends each time she goes for food)
# - number of food incidents (how many times during the year the whole food in the house is halved - by default 6)
# - number of money incidents (how many times during the year the whole money in the house is halved - by default 6)

import random
from itertools import product
from random import randint
from termcolor import cprint


class Human:
    total_eaten_food = 0

    def __init__(self, name, gender, home, cat_owned):
        self.name = name
        self.gender = gender
        self.house = home
        self.is_alive = True
        self.fullness = 30
        self.happiness = 100
        self.cat_owned = cat_owned

    def __str__(self):
        return f"Я человек. Имя - {self.name}. Пол - {self.gender}. " \
               f"Уровень счастья - {self.happiness}. Сытость - {self.fullness}."

    def to_act(self, other):
        if self.fullness < 0:
            cprint(f"Человек {self.name} в эпоху экономического роста и процветания умер от голода.", "blue")
            self.fullness = 0
            self.happiness = 0
            self.is_alive = False
        elif self.happiness < 10:
            cprint(f"Человек {self.name} был рождён для счастья, но умер от грусти.", "blue")
            self.fullness = 0
            self.happiness = 0
            self.is_alive = False
        elif self.fullness < 10:
            self.to_eat()

    def to_eat(self):
        if self.house.human_food > 0:
            maximum_food_to_eat = 30
            while self.house.human_food > 0 and maximum_food_to_eat > 0:
                Human.total_eaten_food += 1
                self.house.human_food -= 1
                self.fullness += 1
                maximum_food_to_eat -= 1

    def to_pat_a_cat(self):
        self.happiness += 5
        self.fullness -= 10


class Cat:

    def __init__(self, name, home):
        self.name = name
        self.house = home
        self.fullness = 30
        self.is_alive = True

    def __str__(self):
        return f"Я - кот. Имя - {self.name}. Моя сытость - {self.fullness}."

    def to_eat(self):
        if self.house.cat_food > 0:
            maximum_food_to_eat = 10
            while self.house.human_food > 0 and maximum_food_to_eat > 0:
                self.house.cat_food -= 1
                self.fullness += 2
                maximum_food_to_eat -= 1
        else:
            self.fullness -= 10

    def to_sleep(self):
        self.fullness -= 10

    def to_rip_n_tear_wallpapers(self):
        self.fullness -= 10
        self.house.dirt += 5

    def to_act(self):
        random_action = randint(0, 1)
        if self.fullness < 0:
            cprint(f"Кот {self.name} безответственно заморен голодом.", "blue")
            self.is_alive = False
        elif self.fullness < 20:
            self.to_eat()
        elif random_action == 0:
            self.to_sleep()
        else:
            self.to_rip_n_tear_wallpapers()


class House:

    def __init__(self):
        self.dirt = 0
        self.money = 100
        self.human_food = 50
        self.cat_food = 30

    def __str__(self):
        return f"Я дом. Во мне {self.human_food} человечьей еды, {self.cat_food} кошачьей еды," \
               f" {self.money} денег и {self.dirt} грязи "


class Husband(Human):
    total_money_earned = 0

    def __init__(self, name, gender, home, cat_owned, partner):
        super().__init__(name, gender, home, cat_owned)
        self.married_to = partner

    def __str__(self):
        return super().__str__() + f" Моя жена - {self.married_to.name}."

    def to_act(self, salary):
        super().to_act(None)
        if self.is_alive:
            random_action = randint(1, 3)
            if self.house.money < 500:
                self.to_work(salary)
            elif self.happiness < 30:
                self.gaming()
            elif random_action == 1:
                self.to_work(salary)
            elif random_action == 2:
                self.to_pat_a_cat()
            else:
                self.gaming()

    def to_work(self, salary):
        self.fullness -= 10
        self.house.money += salary
        Husband.total_money_earned += salary

    def gaming(self):
        self.fullness -= 10
        self.happiness += 20


class Child(Human):

    def __init__(self, name, gender, home, father, mother):
        super().__init__(name, gender, home, None)
        self.father = father
        self.mother = mother

    def __str__(self):
        return super().__str__() + f" Я ребёнок {self.father.name} и {self.mother.name}."

    def to_eat(self):
        if self.house.human_food > 0:
            maximum_food_to_eat = 10
            while self.house.human_food > 0 and maximum_food_to_eat > 0:
                Human.total_eaten_food += 1
                self.house.human_food -= 1
                self.fullness += 1
                maximum_food_to_eat -= 1
        else:
            self.fullness -= 10

    def to_sleep(self):
        self.fullness -= 10

    def to_act(self, other):
        if self.fullness < 0:
            cprint(f"Ребенок {self.name} умер.", "blue")
            self.is_alive = False
        elif self.fullness < 20:
            self.to_eat()
        else:
            self.to_sleep()


class Wife(Human):
    total_fur_coats_bought = 0

    def __init__(self, name, gender, home, cat_owned, partner):
        super().__init__(name, gender, home, cat_owned)
        self.married_to = partner

    def __str__(self):
        return super().__str__() + f" Мой муж - {self.married_to.name}."

    def to_act(self, spending):
        super().to_act(None)
        if self.is_alive:
            random_action = randint(1, 3)
            if self.house.human_food < 60 or self.house.cat_food < 20:
                self.to_do_shopping(spending)
            elif self.house.dirt > 100:
                self.to_clean_a_house()
            elif self.happiness < 80:
                self.to_pat_a_cat()
                self.to_buy_a_fur_coat()
            elif random_action == 1:
                self.to_buy_a_fur_coat()
            elif random_action == 2:
                self.to_pat_a_cat()
            else:
                self.fullness -= 10

    def to_do_shopping(self, spending):
        if self.house.money > spending:
            self.house.human_food += spending/2
            self.house.cat_food += spending/2
            self.house.money -= spending
            self.fullness -= 10

    def to_buy_a_fur_coat(self):
        if self.house.money > 400:
            self.happiness += 60
            self.house.money -= 350
            self.fullness -= 10
            Wife.total_fur_coats_bought += 1

    def to_clean_a_house(self):
        if self.house.dirt > 100:
            self.house.dirt -= 100
        elif self.house.dirt <= 100:
            self.house.dirt = 0
        self.fullness -= 10


def simulation(salary, number_of_cats, sum_for_shopping, food_incidents=6, money_incidents=6):
    successful_simulations = 0
    failed_simulations = 0
    simulations = {"Успешные": [], "Провальные": []}
    simulation_number = 0

    for food_incident, money_incident in product(range(1, food_incidents), range(1, money_incidents)):
        sweet_home = House()
        cats = []
        failure = False
        failure_day = None
        simulation_number += 1

        for cat in range(number_of_cats):
            cat = Cat(f"Кот номер {cat}", sweet_home)
            cats.append(cat)

        eddy = Husband(name="Эдуард Владимирович", gender="Мальчик", partner=None, home=sweet_home, cat_owned=cats)
        masha = Wife(name="Мария Георгиевна", gender="Девочка", partner=None, home=sweet_home, cat_owned=cats)

        eddy.married_to, masha.married_to = masha, eddy
        genevieve = Child("Женевьева", "Девочка", sweet_home, eddy, masha)

        days_of_food_incidents = random.sample(range(365), food_incident)
        days_of_money_incidents = random.sample(range(365), money_incident)

        for day in range(366):

            if day in days_of_food_incidents:
                sweet_home.human_food /= 2
                sweet_home.cat_food /= 2

            if day in days_of_money_incidents:
                sweet_home.money /= 2

            are_cats_alive = True
            sweet_home.dirt += 5
            if sweet_home.dirt > 90:
                eddy.happiness -= 10
                masha.happiness -= 10
            eddy.to_act(salary)
            masha.to_act(sum_for_shopping)
            genevieve.to_act(None)

            for cat in cats:
                cat.to_act()
                if not cat.is_alive:
                    are_cats_alive = False

            if not masha.is_alive or not eddy.is_alive or not genevieve.is_alive or not are_cats_alive:
                failure = True
                failure_day = day
                break

        if failure:
            cprint(
                f"Член семьи не выжил. Симуляция закончена на день {failure_day}. "
            )
            failed = [
                f"Симуляция № {simulation_number:2}", f"Зарплата {salary}",
                f"Котов {number_of_cats}", f"Пищевых происшествий {food_incident}",
                f"Денежных происшествий {money_incident}", f"День остановки {failure_day}"
            ]
            simulations["Провальные"].append(failed)
            failed_simulations += 1
        else:
            cprint(
                f"Симуляция прошла успешно."
            )
            success = [
                f"Симуляция № {simulation_number:2}", f"Зарплата {salary}", f"Котов {number_of_cats}",
                f"Пищевых происшествий {food_incident}", f"Денежных происшествий {money_incident}"
            ]
            simulations["Успешные"].append(success)
            successful_simulations += 1

    cprint(
        f"При зарплате {salary}, тратах на продукты {sum_for_shopping} и {number_of_cats} котах:\n"
        f"Успешных симуляций - {successful_simulations}. Провальных симуляций - {failed_simulations}.\n"
        f"Коэффициент успешности - {round(successful_simulations/failed_simulations, 2)}",
        "green"
    )

    for key, value in simulations.items():
        cprint(key, "blue")
        for element in simulations[key]:
            print(element)


simulation(salary=400, number_of_cats=21, sum_for_shopping=400)
