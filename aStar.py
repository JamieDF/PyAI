from implementation import GridWithWeights
#TODO Multiple Robots


start = tuple(map(int, input("Please enter the robots start location(x,y) :").split(',')))
goal = tuple(map(int, input("Please enter the robots goal location(x,y) :").split(',')))

"""readWalls = open('GridFiles/gridWalls.txt', 'r')
gridWalls = readWalls.read()
print(gridWalls)
print(type(gridWalls))"""

map = GridWithWeights(12, 12)
map.walls = [(0, 2), (2, 4), (3, 4), (3, 3), (3, 1), (4, 1), (5, 3), (7, 3)]
map.trap = [(3, 2), (8, 8), (7, 7), (2, 7), (11, 11)]
map.weights = {loc: 5 for loc in [(3, 2), (8, 8), (7, 7), (2, 7), (11, 11)]}

print ("\n Key : \n R = robot location \n G = Goal \n T = Trap \n ### = Wall \n @ = final path to goal \n")
print("-----------------------------------")
from implementation import *
came_from, cost_so_far = a_star_search(map, start, goal)
draw_grid(map, width=3, point_to=came_from, start=start, goal=goal)
print("-----------------------------------")
draw_grid(map, width=3, number=cost_so_far, start=start, goal=goal)
print("-----------------------------------")
draw_grid(map, width=3, path=reconstruct_path(came_from, start=start, goal=goal))
