from implementation2 import GridWithWeights
#TODO Multiple Robots

"""
start = tuple(map(int, input("Please enter the robots start location(x,y) :").split(',')))
goal = tuple(map(int, input("Please enter the robots goal location(x,y) :").split(',')))
"""

start1 = (0, 0)
goal1 = (10, 10)
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

came_from1, cost_so_far1, came_from2, cost_so_far2 = a_star_search(map, start1, goal1, start2, goal2)


#Prints cost graph
draw_grid(map, width=3, number1=cost_so_far1, number2=cost_so_far2, start1=start1, goal1=goal1, start2=start2, goal2=goal2)
print("-----------------------------------")

#prints final path for first robot only
draw_grid(map, width=3, start1=start1, goal1=goal1, path1=reconstruct_path1(came_from1=came_from1, start1=start1, goal1=goal1))
print("-----------------------------------")

#prints paths for both robots, with second robot overwriting path of first robot
draw_grid(map, width=3,  start1=start1, goal1=goal1, start2=start2, goal2=goal2, path1=reconstruct_path1(came_from1=came_from1, start1=start1, goal1=goal1), path2=reconstruct_path2(came_from2=came_from2, start2=start2, goal2=goal2))
print("-----------------------------------")
