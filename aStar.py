
#TODO Multiple Robots


start = tuple(map(int, input("Please enter the robots start location(x,y) :").split(',')))
goal = tuple(map(int, input("Please enter the robots goal location(x,y) :").split(',')))

print ("\n Key : \n R = robot location \n G = Goal \n T = Trap \n ### = Wall \n @ = final path to goal \n")
print("-----------------------------------")
from implementation import *
came_from, cost_so_far = a_star_search(map, start, goal)
draw_grid(map, width=3, point_to=came_from, start=start, goal=goal)
print("-----------------------------------")
draw_grid(map, width=3, number=cost_so_far, start=start, goal=goal)
print("-----------------------------------")
draw_grid(map, width=3, path=reconstruct_path(came_from, start=start, goal=goal))
