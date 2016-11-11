"""
This file contains...
-A* Search Algorithm
-cost function
-two heuristic functions (Euclidian and Manhattan)
-code to prevent the robots from colliding with each other and finding alternative paths
"""

import math
import heapq
import sys


def from_id_width(id, width):
    return (id % width, id // width)


def draw_tile(graph, id, style, width):
    r = " ."
    if 'number1' in style and id in style['number1']: r = " %d" % style['number1'][id]
    if 'number2' in style and id in style['number2']: r = " %d" % style['number2'][id]

    if 'path1' in style and id in style['path1']: r = " @"
    if 'path2' in style and id in style['path2']: r = " *"

    if 'start1' in style and id == style['start1']: r = " R"
    if 'goal1' in style and id == style['goal1']: r = " G"
    if 'start2' in style and id == style['start2']: r = " R2"
    if 'goal2' in style and id == style['goal2']: r = " G2"

    if id in graph.walls: r = "#" * width
    if id in graph.trap: r = " T"  # added trap
    return r


def draw_grid(graph, width=2, **style):
    for y in range(graph.height):
        for x in range(graph.width):
            print("%%-%ds" % width % draw_tile(graph, (x, y), style, width), end="")
        print()


class SquareGrid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.walls = []
        self.trap = []



    def in_bounds(self, id):
        (x, y) = id
        return 0 <= x < self.width and 0 <= y < self.height

    def passable(self, id):
        return id not in self.walls

    def neighbors(self, id):
        (x, y) = id
        results = [(x + 1, y), (x, y - 1), (x - 1, y), (x, y + 1)]
        if (x + y) % 2 == 0: results.reverse()  # aesthetics
        validResults = []
        for i in results: 
            if self.passable(i) and self.in_bounds(i):
                validResults.append(i)
        return validResults


class GridWithWeights(SquareGrid):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.weights = {}

    def cost(self, from_node, to_node):
        return self.weights.get(to_node, 1)


class PriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]


def reconstructPath(came_from, start, goal): #creates path of robot

    current = goal
    path = [current]
    while current != start:
        current = came_from[current]
        path.append(current)
    return path


def heuristicFunction(heuristic, a, b): #Heuristic function returns either Manhattan or Euclidian heuristic
    (x1, y1) = a    #robot start position
    (x2, y2) = b    #robot goal position
    if heuristic == 1: #Manhattan heuristic selected
        return abs(x1 - x2) + abs(y1 - y2)
    else: #Euclidian heuristic selected
        return abs(math.sqrt((abs(x1 - x2)) ** 2 + (abs(y1 - y2)) ** 2))


def a_star_search(graph, start1, goal1, start2, goal2): #Execute A* algorithm 
    #Prompt users to select Manhattan or Euclidian heuristic for execution
    heur = int(input("\n\nType '1' to execute with Manhattan heuristic OR '2' for Euclidian\n->"))
    while (heur != 1) and (heur != 2):
        heur = int(input("\n\nType '1' to execute with Manhattan heuristic OR '2' for Euclidian\n->"))

    frontier1 = PriorityQueue()
    frontier2 = PriorityQueue()
    frontier3 = PriorityQueue()
    frontier1.put(start1, 0)
    frontier2.put(start2, 0)
    frontier3.put(start2, 0)
    came_from1 = {}
    came_from2 = {}
    came_from3 = {}
    cost_so_far1 = {}
    cost_so_far2 = {}
    cost_so_far3 = {}
    came_from1[start1] = None
    came_from2[start2] = None
    came_from3[start2] = None
    cost_so_far1[start1] = 0
    cost_so_far2[start2] = 0
    cost_so_far3[start2] = 0
    robot1path = []
    robot2path = []
    robot2idealPath = []
    pathAltered = False


    while not frontier1.empty():    #For first robot
        current1 = frontier1.get()
        if current1 == goal1:    #Goal found
            break
            
        for next in graph.neighbors(current1):    #Find next vertex in path and add to priority queue 
            new_cost1 = cost_so_far1[current1] + graph.cost(current1, next)
            if next not in cost_so_far1 or new_cost1 < cost_so_far1[next]:
                cost_so_far1[next] = new_cost1
                priority1 = new_cost1 + heuristicFunction(heur, goal1, next)
                frontier1.put(next, priority1)
                came_from1[next] = current1
            
    robot1path = (reconstructPath(came_from1, start1, goal1))
    robot1path.reverse()


    counter = 0    #used to handle collisions
    while not frontier2.empty():    #For second robot
        current2 = frontier2.get()
        
        if current2 == goal2:
            break
        
        coords = graph.neighbors(current2)
        unoccupiedCoords = []
        for i in coords:
            if not (counter < len(robot1path) and i == robot1path[counter]):
                unoccupiedCoords.append(i)
                print(i)
            else:
                pathAltered = True


        print("Iteration:    %r  Pos:    %r" % (counter, current2))
        print(pathAltered)

        for next in unoccupiedCoords:    #Find next vertex in path and add to priority queue 
            new_cost2 = cost_so_far2[current2] + graph.cost(current2, next)
            if next not in cost_so_far2 or new_cost2 < cost_so_far2[next]:
                '''if counter < len(robot1path) and next == robot1path[counter]:
                    wait.append(counter)'''
                cost_so_far2[next] = new_cost2
                priority2 = new_cost2 + heuristicFunction(heur, goal2, next)
                frontier2.put(next, priority2)
                came_from2[next] = current2
        counter += 1

    while not frontier3.empty():
        current3 = frontier3.get()
        if current3 == goal2:    #Goal found
            break
            
        for next in graph.neighbors(current3):    #Find next vertex in path and add to priority queue 
            new_cost3 = cost_so_far3[current3] + graph.cost(current3, next)
            if next not in cost_so_far3 or new_cost3 < cost_so_far3[next]:
                cost_so_far3[next] = new_cost3
                priority3 = new_cost3 + heuristicFunction(heur, goal2, next)
                frontier3.put(next, priority3)
                came_from3[next] = current3
            
    robot2path = reconstructPath(came_from2, start2, goal2)
    robot2path.reverse()
    robot2idealPath = reconstructPath(came_from3, start2, goal2)
    robot2idealPath.reverse()
    
    if (pathAltered == True):
        if (robot2idealPath == robot2path):
            print("Robot 2 waits once to avoid collision with Robot 1.")
        else:
            print("Robot 2 diverts its course to avoid collision with Robot 1.")


    #Exits program if either robot could not make it to their goal
    if current1 != goal1:
        sys.exit("Could not find Robot1 goal.")
    elif current2 != goal2:
        sys.exit("Could not find Robot2 goal.")

    #Returns costs and paths for each robot
    return came_from1, cost_so_far1, came_from2, cost_so_far2
