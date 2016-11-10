from NEWimplementation import *

#takes both robots start and end locations from an input
start1 = tuple(map(int, input("Please enter the first robots start location(x,y) :").split(',')))
goal1 = tuple(map(int, input("Please enter the first robots goal location(x,y) :").split(',')))

start2 = tuple(map(int, input("Please enter the second robots start location(x,y) :").split(',')))
goal2 = tuple(map(int, input("Please enter the second robots goal location(x,y) :").split(',')))


#Imports the maps walls and trap locations from the file located in the GridFiles folder

#Note to change the map layout, change the number following the files title to 1,2,3 or for to get the correct maps
#i.e to use map 4 chagnge the open to 'GridFiles/gridWalls4.txt' and 'GridFiles/gridTraps4.txt'
with open('GridFiles/gridWalls1.txt') as f:
    list1 = [tuple(map(int, i.split(','))) for i in f]

with open('GridFiles/gridTraps1.txt') as f:
    list2 = [tuple(map(int, i.split(','))) for i in f]

map = GridWithWeights(8, 5)
map.walls = list1
map.trap = list2
map.weights = {loc: 5 for loc in list2}

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
