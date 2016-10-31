import math


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
        results = filter(self.in_bounds, results)
        results = filter(self.passable, results)
        return results


class GridWithWeights(SquareGrid):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.weights = {}

    def cost(self, from_node, to_node):
        return self.weights.get(to_node, 1)

import heapq


class PriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]


def reconstruct_path1(came_from1, start1, goal1):

    current1 = goal1
    path1 = [current1]
    while current1 != start1:
        current1 = came_from1[current1]
        path1.append(current1)
    return path1

def reconstruct_path2(came_from2, start2, goal2):

    current2 = goal2
    path2 = [current2]
    while current2 != start2:
        current2 = came_from2[current2]
        path2.append(current2)

    return path2

#First heuristic function finds city block distance
def manhattanHeuristic(a, b):
    (x1, y1) = a
    (x2, y2) = b
    return abs(x1 - x2) + abs(y1 - y2)

#Second heuristic finds straight line distance to goal
def euclidianHeuristic(a, b):
    (x1, y1) = a
    (x2, y2) = b
    return abs(math.sqrt((abs(x1 - x2)) ** 2 + (abs(y1 - y2)) ** 2))


def a_star_search(graph, start1, goal1, start2, goal2):
    heur = int(input("Type '1' to execute with Manhattan heuristic OR '2' to for Euclidian\n->"))
    while (heur != 1) and (heur != 2):
        heur = int(input("Type '1' to execute with Manhattan heuristic OR '2' to for Euclidian\n->"))

    frontier1 = PriorityQueue()
    frontier2 = PriorityQueue()
    frontier1.put(start1, 0)
    frontier2.put(start2, 0)
    came_from1 = {}
    came_from2 = {}
    cost_so_far1 = {}
    cost_so_far2 = {}
    came_from1[start1] = None
    came_from2[start2] = None
    cost_so_far1[start1] = 0
    cost_so_far2[start2] = 0
    route = []

    if (heur == 1):
        #For first robot
        while not frontier1.empty():
            current1 = frontier1.get()
            route.append(current1)
            
            
            if current1 == goal1:
                break
            
            #Find next vertex in path and add to priority queue 
            for next in graph.neighbors(current1):
                new_cost1 = cost_so_far1[current1] + graph.cost(current1, next)
                if next not in cost_so_far1 or new_cost1 < cost_so_far1[next]:
                    cost_so_far1[next] = new_cost1
                    priority1 = new_cost1 + manhattanHeuristic(goal1, next)
                    frontier1.put(next, priority1)
                    came_from1[next] = current1
        
        
        #For second robot    
        while not frontier2.empty():
            current2 = frontier2.get()
            
            if current2 == goal2:
                break

            #Check if any neighbours equal the last added vertex to Robot1's priority queue
            counter=0
            for i in graph.neighbors(current2):
                if (i == route[counter + 1]):
                    #If so, remove that vertex from the list of possible neighbours
                    del graph.neighbors(current2)[i]
                else:
                    counter += 1
                
            #Find next vertex in path and add to priority queue 
            for next in graph.neighbors(current2):
                new_cost2 = cost_so_far2[current2] + graph.cost(current2, next)
                if next not in cost_so_far2 or new_cost2 < cost_so_far2[next]:
                    cost_so_far2[next] = new_cost2
                    priority2 = new_cost2 + manhattanHeuristic(goal2, next)
                    frontier2.put(next, priority2)
                    came_from2[next] = current2
            

    else:
        #For first robot
        while not frontier1.empty():
            current1 = frontier1.get()
            route.append(current1)
            
            
            if current1 == goal:
                break
            
            #Find next vertex in path and add to priority queue 
            for next in graph.neighbors(current1):
                new_cost1 = cost_so_far1[current1] + graph.cost(current1, next)
                if next not in cost_so_far1 or new_cost1 < cost_so_far1[next]:
                    cost_so_far1[next] = new_cost1
                    priority1 = new_cost1 + euclidianHeuristic(goal1, next)
                    frontier1.put(next, priority1)
                    came_from1[next] = current1
        
        
        #For second robot    
        while not frontier2.empty():
            current2 = frontier2.get()
            
            if current2 == goal:
                break

            #Check if any neighbours equal the last added vertex to Robot1's priority queue
            counter = 0
            for i in graph.neighbors(current2):
                if i == route1[counter + 1]:
                    #If so, remove that vertex from the list of possible neighbours
                    del graph.neighbors(current2)[i]
                else:
                    counter += 1

            #Find next vertex in path and add to priority queue 
            for next in graph.neighbors(current2):
                new_cost2 = cost_so_far2[current2] + graph.cost(current2, next)
                if next not in cost_so_far2 or new_cost2 < cost_so_far2[next]:
                    cost_so_far2[next] = new_cost2
                    priority2 = new_cost2 + euclidianHeuristic(goal2, next)
                    frontier2.put(next, priority2)
                    came_from2[next] = current2
    print("Total cost for Robot ones path")
    print(cost_so_far2[next])


    # New,  Exits program if the robot could not make it to the goal
    if current1 != goal1:
        import sys
        sys.exit("Could not find Robot1 goal.")
    elif current2 != goal2:
        sys.exit("Could not find Robot1 goal.")

    #returns costs and paths for each robot
    return came_from1, cost_so_far2, came_from2, cost_so_far2
