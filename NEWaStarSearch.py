from implementation2 import *

"""
start = tuple(map(int, input("Please enter the robots start location(x,y) :").split(',')))
goal = tuple(map(int, input("Please enter the robots goal location(x,y) :").split(',')))
"""

start1 = (2, 0)
goal1 = (2, 3)
start2 = (1, 4)
goal2 = (6, 4)

map = GridWithWeights(8, 5)
map.walls = [(0,2), (1,2), (3,2), (5,2), (6,2), (7,2)]
map.trap = [(2, 2)]
map.weights = {loc: 5 for loc in [(2,2)]}

came_from1, cost_so_far1, came_from2, cost_so_far2 = a_star_search(map, start1, goal1, start2, goal2)

path1=reconstructPath(came_from1, start1, goal1)
path2=reconstructPath(came_from2, start2, goal2)


print ("\n Key : \n R = robot location \n R2 = Second robot location \n G = Goal \n G2 = Second Goal \n T = Trap \n ### = Wall \n @ = final path to goal \n * = final path to goal 2 \n")
print("-----------------------------------")


#Prints cost graph
draw_grid(map, width=3, number1=cost_so_far1, number2=cost_so_far2, start1=start1, goal1=goal1, start2=start2, goal2=goal2)
print("-----------------------------------")


#prints final path for first robot only
draw_grid(map, width=3, start1=start1, goal1=goal1, path1=reconstructPath(came_from1, start1, goal1))
print("-----------------------------------")


#prints paths for both robots, with second robot overwriting path of first robot
draw_grid(map, width=3,  start1=start1, goal1=goal1, start2=start2, goal2=goal2, path1=path1, path2=path2)
print("-----------------------------------")


path1.reverse()    #reverse to display path from beginning
print("\nRobot1 path:\n")
for i in path1:
    print(i)


path2.reverse()    #reverse to display path from beginning
print("\nRobot2 path:\n")
for j in path2:
    print(j)
