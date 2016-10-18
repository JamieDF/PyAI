
print ("\n Key : \n R = robot location \n G = Goal \n T = Trap \n ### = Wall \n @ = final path to goal \n")
print("_________________________")
from implementation import *
came_from, cost_so_far = a_star_search(map, (0, 0), (10, 9))
draw_grid(map, width=3, point_to=came_from, start=(0, 0), goal=(10, 9))
print("_________________________")
draw_grid(map, width=3, number=cost_so_far, start=(0, 0), goal=(10, 9))
print("_________________________")
draw_grid(map, width=3, path=reconstruct_path(came_from, start=(0, 0), goal=(10, 9)))
