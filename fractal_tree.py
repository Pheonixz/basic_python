# A tree drawn using SimpleDraw module using a recursion function

import simple_draw as sd

sd.resolution = 1200, 1000


def plant_a_tree(initial_point, angle, branch_length):
    if branch_length < 8:
        return
    v1 = sd.get_vector(start_point=initial_point, angle=angle + 75, length=branch_length, width=7)
    v2 = sd.get_vector(start_point=initial_point, angle=angle - 75, length=branch_length, width=7)
    v1.draw(sd.COLOR_DARK_GREEN)
    v2.draw(sd.COLOR_DARK_GREEN)
    new_start_v1 = v1.end_point
    new_start_v2 = v2.end_point
    new_branch_length = branch_length * 0.83
    new_angle_1 = angle + 40
    new_angle_2 = angle - 40
    plant_a_tree(new_start_v1, new_angle_1, new_branch_length)
    plant_a_tree(new_start_v2, new_angle_2, new_branch_length)


root_point = sd.get_point(600, 1)
stem_point = sd.get_point(600, 400)
sd.line(root_point, stem_point, width=60, color=sd.COLOR_DARK_ORANGE)
plant_a_tree(stem_point, 90, 100)

sd.pause()
