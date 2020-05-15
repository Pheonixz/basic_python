# A snowfall animation made in object oriented style using SimpleDraw library.

import simple_draw as sd


sd.resolution = 1200, 800
snowflakes = {}
step = 0


class Snowflake:

    def __init__(self):
        self.length = sd.random_number(10, 101)
        self.x = sd.random_number(0, sd.resolution[0])
        self.y = sd.randint(sd.resolution[1] - 100, sd.resolution[1] + 100)
        self.factor_a = sd.random_number(10, 100)/100
        self.factor_b = sd.random_number(10, 100)/100
        self.factor_c = sd.random_number(10, 100)

    def draw(self, color=sd.COLOR_WHITE):
        start_point = sd.get_point(x=self.x, y=self.y)
        sd.snowflake(
            center=start_point,
            length=self.length,
            color=color,
            factor_a=self.factor_a,
            factor_b=self.factor_b,
            factor_c=self.factor_c
        )

    def clear_previous_picture(self, color=sd.background_color):
        self.draw(color)

    def move(self):
        self.x += sd.random_number(-10, 11)
        self.y -= sd.random_number(0, 15)


def run_snowfall(snowflakes_count=0):
    if len(snowflakes) != snowflakes_count:
        snowflakes[len(snowflakes)] = Snowflake()

    for num, snowflake in snowflakes.items():
        snowflake.clear_previous_picture()
        snowflake.move()
        snowflake.draw()

        if snowflake.y < 0:
            snowflakes[num] = Snowflake()


while True:
    step += 1
    sd.start_drawing()

    if step < 50:
        run_snowfall(snowflakes_count=20)
    elif step > 50:
        run_snowfall(snowflakes_count=50)

    sd.sleep(0.05)
    sd.finish_drawing()

    if sd.user_want_exit():
        break
