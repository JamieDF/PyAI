import math


def from_id_width(id, width):
    return (id % width, id // width)


def draw_tile(graph, id, style, width):
    r = " ."
    if 'number' in style and id in style['number']: r = " %d" % style['number'][id]
    if 'point_to' in style and style['point_to'].get(id, None) is not None:
        (x1, y1) = id
        (x2, y2) = style['point_to'][id]
        if x2 == x1 + 1: r = " \u2190"
        if x2 == x1 - 1: r = " \u2192"
        if y2 == y1 + 1: r = " \u2191"
        if y2 == y1 - 1: r = " \u2193"

    if 'start' in style and id == style['start']: r = " R"
    if 'goal' in style and id == style['goal']: r = " G"
    if 'path' in style and id in style['path']: r = " @"
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


# Map details and locations
'''
map = GridWithWeights(12, 12)
map.walls = [(1, 4),  (4, 2), (5, 4), (3, 4), (3, 3), (3, 1), (4, 1), (5, 3), (7, 3), (4, 2), (1, 7), (11, 4), (3, 11), (4, 10), (9, 5), (6, 6), (0, 4), (2, 4)]
map.trap = [(3, 2), (8, 8), (7, 7), (2, 7), (11, 11)]
map.weights = {loc: 5 for loc in [(3, 2), (8, 8), (7, 7), (2, 7), (11, 11)]}
'''

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


def reconstruct_path(came_from, start, goal):
    current = goal
    path = [current]
    while current != start:
        current = came_from[current]
        path.append(current)
    path.append(start)  # optional
    path.reverse()  # optional
    return path


def manhattanHeuristic(a, b):
    (x1, y1) = a
    (x2, y2) = b
    return abs(x1 - x2) + abs(y1 - y2)


def euclidianHeuristic(a, b):
    (x1, y1) = a
    (x2, y2) = b
    return abs(math.sqrt((abs(x1 - x2)) ** 2 + (abs(y1 - y2)) ** 2))


def a_star_search(graph, start, goal):
    heur = int(input("Type '1' to execute with Manhattan heuristic OR '2' to for Euclidian\n->"))
    while (heur != 1) and (heur != 2):
        heur = int(input("Type '1' to execute with Manhattan heuristic OR '2' to for Euclidian\n->"))
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0

    if (heur == 1):
        while not frontier.empty():
            current = frontier.get()

            if current == goal:
                break

            for next in graph.neighbors(current):
                new_cost = cost_so_far[current] + graph.cost(current, next)
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost + manhattanHeuristic(goal, next)
                    frontier.put(next, priority)
                    came_from[next] = current

    else:
        while not frontier.empty():
            current = frontier.get()

            if current == goal:
                break

            for next in graph.neighbors(current):
                new_cost = cost_so_far[current] + graph.cost(current, next)
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost + euclidianHeuristic(goal, next)
                    frontier.put(next, priority)
                    came_from[next] = current

    # New,  Exits program if the robot could not make it to the goal
    if current != goal:
        import sys
        sys.exit("could not find goal")

    return came_from, cost_so_far
