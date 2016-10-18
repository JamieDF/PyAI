from implementation import *
came_from, cost_so_far = a_star_search(diagram4, (0, 0), (5, 2))
draw_grid(diagram4, width=3, point_to=came_from, start=(0, 0), goal=(5, 2))
print()
draw_grid(diagram4, width=3, number=cost_so_far, start=(0, 0), goal=(5, 2))
print()
draw_grid(diagram4, width=3, path=reconstruct_path(came_from, start=(0, 0), goal=(5, 2)))
