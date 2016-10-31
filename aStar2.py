from implementation2 import GridWithWeights
#TODO Multiple Robots

"""
start = tuple(map(int, input("Please enter the robots start location(x,y) :").split(',')))
goal = tuple(map(int, input("Please enter the robots goal location(x,y) :").split(',')))
"""

start = (0, 0)
goal = (10, 10)
start2 = (2, 2)
goal2 = (7,8)

"""readWalls = open('GridFiles/gridWalls.txt', 'r')
gridWalls = readWalls.read()
print(gridWalls)
print(type(gridWalls))"""

map = GridWithWeights(12, 12)
map.walls = [(0, 2), (2, 4), (3, 4), (3, 3), (3, 1), (4, 1), (5, 3), (7, 3)]
map.trap = [(3, 2), (8, 8), (7, 7), (2, 7), (11, 11)]
map.weights = {loc: 5 for loc in [(3, 2), (8, 8), (7, 7), (2, 7), (11, 11)]}

print ("\n Key : \n R = robot location \n R2 = Second robot location \n G = Goal \n G2 = Second Goal \n T = Trap \n ### = Wall \n @ = final path to goal \n * = final path to goal 2 \n")
print("-----------------------------------")

from implementation2 import *

came_from, cost_so_far, came_from2, cost_so_fa2 = a_star_search(map, start, goal, start2, goal2)

draw_grid(map, width=3, point_to=came_from, point_to2=came_from2, start=start, goal=goal, start2=start2, goal2=goal2)
print("-----------------------------------")
draw_grid(map, width=3, number=cost_so_far, number2=cost_so_fa2, start=start, goal=goal, start2=start2, goal2=goal2)
print("-----------------------------------")
draw_grid(map, width=3, start=start, goal=goal, path=reconstruct_path(came_from=came_from, start=start, goal=goal))
print("-----------------------------------")
draw_grid(map, width=3,  start=start, goal=goal, start2=start2, goal2=goal2, path=reconstruct_path(came_from=came_from, start=start, goal=goal), path2=reconstruct_path2(came_from2=came_from2, start2=start2, goal2=goal2))
print("-----------------------------------")
