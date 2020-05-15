# A simple factory function which draws different geometric shapes
# depending on the given angle value.

import simple_draw as sd


def get_polygon(n):
    def draw_a_figure(point, angle, length, number_of_sides=n):
        vector_point = point
        angle_iteration = 360 / number_of_sides
        iteration = angle_iteration
        for side in range(number_of_sides - 1):
            side = sd.get_vector(start_point=vector_point, angle=angle + iteration, length=length)
            side.draw()
            vector_point = side.end_point
            iteration += angle_iteration
        sd.line(vector_point, point)

    return draw_a_figure
