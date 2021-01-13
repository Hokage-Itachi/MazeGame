from models.graph import Graph, Node
import random
from math import *


class Maze:

    def __init__(self, size):
        if(size % 2 == 0):
            self.size = size - 1
        else:
            self.size = size
        self.count = (self.size - 1) ** 2 / 4
        self.matrix = [[0 for i in range(self.size)] for j in range(self.size)]
        self.pos = [1, 1]
        self.index = 0
        self.graph = Graph()
        # print(self.matrix)

    def create(self):
        # set beginning
        self.matrix[0][1] = 4
        self.old_node = Node(str(self.index), 1, 0)
        self.index += 1
        # add first node to graph
        self.matrix[self.pos[0]][self.pos[1]] = 1
        self.count -= 1
        current_node = Node(str(self.index), 1, 1)
        self.graph.addNode(self.old_node)
        self.graph.addNode(current_node)
        self.graph.addEdge(self.old_node, current_node)
        self.old_node = current_node

        while (self.count > 0):
            self.index += 1
            direction = self.getDirection(self.pos)
            k = random.randint(0, len(direction) - 1)
            self.createPath(self.pos, direction[k])
            

        # set ending
        self.matrix[self.size - 2][self.size - 1] = 4
        n = Node(str(self.index), self.size - 1, self.size - 2)
        self.index += 1
        m = self.graph.get_node_from_position([self.size - 2, self.size - 2])
        self.graph.addNode(n)
        self.graph.addEdge(n, m)
        self.print_to_file()

    def getDirection(self, pos):
        directions = []
        i = pos[0]
        j = pos[1]
        if (i - 2 > 0):
            directions.append(0)
        if (j + 2 < len(self.matrix)):
            directions.append(1)
        if (i + 2 < len(self.matrix)):
            directions.append(2)
        if (j - 2 > 0):
            directions.append(3)

        return directions

    def createPath(self, pos, direction):
        i, j = pos[0], pos[1]
        if (direction == 0):  # go up
            current_node = self.graph.get_node_from_position([j, (i - 2)])
            if (self.matrix[i - 2][j] == 0):  # if not visit
                current_node.label = str(self.index)
                self.matrix[i-1][j] = 1
                self.count -= 1
                self.matrix[i-2][j] = 1
                self.graph.addNode(current_node)
                self.graph.addEdge(self.old_node, current_node)
            # if visited
            self.old_node = current_node
            self.pos[0] = i - 2
        elif (direction == 1):  # go right
            current_node = self.graph.get_node_from_position([j + 2, (i)])
            if (self.matrix[i][j + 2] == 0):  # if not visit
                current_node.label = str(self.index)
                self.matrix[i][j + 1] = 1
                self.count -= 1
                self.matrix[i][j + 2] = 1
                self.graph.addNode(current_node)
                self.graph.addEdge(self.old_node, current_node)
            # if visited
            self.old_node = current_node
            self.pos[1] = j + 2
        elif(direction == 2):  # go down
            current_node = self.graph.get_node_from_position([j, (i + 2)])
            if (self.matrix[i + 2][j] == 0):  # if not visit
                current_node.label = str(self.index)
                self.matrix[i + 1][j] = 1
                self.count -= 1
                self.matrix[i + 2][j] = 1
                self.graph.addNode(current_node)
                self.graph.addEdge(self.old_node, current_node)
            # if visited
            self.old_node = current_node
            self.pos[0] = i + 2
        else:  # go left
            current_node = self.graph.get_node_from_position([j - 2, (i)])
            if (self.matrix[i][j - 2] == 0):  # if not visit
                current_node.label = str(self.index)
                self.matrix[i][j - 1] = 1
                self.count -= 1
                self.matrix[i][j - 2] = 1
                self.graph.addNode(current_node)
                self.graph.addEdge(self.old_node, current_node)
            # if visited
            self.old_node = current_node
            self.pos[1] = j - 2

    
    def printMatrix(self):
        for i in range(self.size):
            for j in range(self.size):
                print(self.matrix[i][j], end=" ")
            print()

    def print_to_file(self):
        file = open("map.txt", "w")
        for row in range(len(self.matrix)):
            for col in range(len(self.matrix)):
                if(col == len(self.matrix) - 1):
                    file.write(str(self.matrix[row][col]))
                else:
                    file.write(str(self.matrix[row][col]) + " ")
                # print("Here")
                
            file.write("\n")
            # TODO: set parent to node
    def findPath(self, start, end):
        # Create lists for open nodes and closed nodes
        start_node = self.graph.get_node_from_position(start)
        end_node = self.graph.get_node_from_position(end)
        # print(start_node.__repr__())
        # print(end_node.__repr__())
        open_list = []
        close_list = []
        sum_g = 0
        g = self.graph
        # Add the start node
        open_list.append(start_node)
        
        while (len(open_list) > 0):
            # Sort to get lowest cost node
            open_list.sort()
            
            # Get node with lowest cost
            curr_node = open_list.pop(0)
            
            # Calculate sum of g from start to current node
            sum_g += curr_node.g
            # Add current node to closed list
            close_list.append(curr_node)
            
            # If reach the goal, return the path
            if curr_node == end_node:
                path = []
                while curr_node != start_node:
                    path.append(curr_node)
                    curr_node = curr_node.parent
                # Return reverse path
                return path[::-1]
            
            # Get neighbors of current node
            
            neighbors = curr_node.adjNodes
            for next_node in neighbors:
                # If next node has been visited
                if next_node in close_list:
                    continue
                
                # Calculate heuristics (Eculid distance)
                next_node.g = self.getEculidDistance(curr_node, next_node) + sum_g
                next_node.h = self.getEculidDistance(next_node, end_node)
                next_node.f = next_node.g + next_node.h
                
                # If neighbor is in open list and it has lower f value
                if(self.can_add_to_open(open_list, next_node)):
                    # Add neighbor to open
                    open_list.append(next_node)
                    next_node.parent = curr_node
        return None
    
    def add_path_to_matrix(self, path):
        old_node = path[0]
        
        next_node = path[1]
        if(next_node.x == old_node.x):
            if(next_node.y < old_node.y):
                self.matrix[old_node.y][old_node.x] = "w"
            else:
                self.matrix[old_node.y][old_node.x] = "s"
        else:
            if(next_node.x < old_node.x):
                self.matrix[old_node.y][old_node.x] = "a"
            else:
                self.matrix[old_node.y][old_node.x] = "d"
        for i in range(1, len(path) - 1):
            node = path[i]
            if(node.x == old_node.x):
                col = node.x
                
                if (node.y < old_node.y): # move up
                    row = node.y + 1
                    self.matrix[row][col] = "w"
                    self.matrix[node.y][node.x] = "w"
                    
                else: # move down
                    row = node.y - 1
                    self.matrix[row][col] = "s"
                    self.matrix[node.y][node.x] = "s"
                    
            else:
                row = node.y
                if(node.x < old_node.x):  # move left
                    col = node.x + 1 
                    self.matrix[row][col] = "a"
                    self.matrix[node.y][node.x] = "a"

                else: # move right
                    col = node.x - 1 
                    self.matrix[row][col] = "d"
                    self.matrix[node.y][node.x] = "d"

            old_node = node
 
    def getEculidDistance(self, start, end):
        return sqrt((start.x - end.x) ** 2 + (start.y - end.y) ** 2)
    
    def can_add_to_open(self, open_list, node):
        # print("List Length: " + str(len(open_list)))
        for element in open_list:
            # print("Node: "+ node.__repr__())
            # print("Elem:" + element.__repr__())
            if(node == element and node.f > element.f):
                return False
        return True

