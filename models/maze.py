from models.graph import Graph, Node
import random


class Maze:
    matrix = [[]]
    size = count = index = 0
    pos = [1, 1]
    index = 0
    graph = Graph()
    # node = Node()
    # end = Node()

    def __init__(self, size):
        if(size % 2 == 0):
            self.size = size - 1
        else:
            self.size = size
        self.count = (self.size - 1) ** 2 / 4
        self.matrix = [[0 for i in range(self.size)] for j in range(self.size)]
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
            direction = self.getDirection(self.pos)
            k = random.randint(0, len(direction) - 1)
            self.createPath(self.pos, direction[k])

        # set ending
        self.matrix[self.size - 2][self.size - 1] = 4
        n = Node(str(self.index), self.size - 1, self.size - 2)
        self.index += 1
        m = Node(str(self.index), self.size - 2, self.size - 2)
        self.graph.addNode(n)
        self.graph.addEdge(n, m)
        self.removeInvalidNode()

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
            if (self.matrix[i - 2][j] == 0):  # if not visit
                current_node = Node(str(self.index), j, i - 2)
                self.index += 1
                self.matrix[i-1][j] = 1
                self.count -= 1
                self.matrix[i-2][j] = 1
                self.graph.addNode(current_node)
                self.graph.addEdge(self.old_node, current_node)
            # if visited
            current_node = Node(str(self.index), j, i - 2)
            self.old_node = current_node
            self.pos[0] = i - 2
        elif (direction == 1):  # go right
            if (self.matrix[i][j + 2] == 0):  # if not visit
                current_node = Node(str(self.index), j + 2, i)
                self.index += 1
                self.matrix[i][j + 1] = 1
                self.count -= 1
                self.matrix[i][j + 2] = 1
                self.graph.addNode(current_node)
                self.graph.addEdge(self.old_node, current_node)
            # if visited
            current_node = Node(str(self.index), j + 2, i)
            self.old_node = current_node
            self.pos[1] = j + 2
        elif(direction == 2):  # go down
            if (self.matrix[i + 2][j] == 0):  # if not visit
                current_node = Node(str(self.index), j, i + 2)
                self.index += 1
                self.matrix[i + 1][j] = 1
                self.count -= 1
                self.matrix[i + 2][j] = 1
                self.graph.addNode(current_node)
                self.graph.addEdge(self.old_node, current_node)
            # if visited
            current_node = Node(str(self.index), j, i + 2)
            self.old_node = current_node
            self.pos[0] = i + 2
        else:  # go left
            if (self.matrix[i][j - 2] == 0):  # if not visit
                current_node = Node(str(self.index), j - 2, i)
                self.index += 1
                self.matrix[i][j - 1] = 1
                self.count -= 1
                self.matrix[i][j - 2] = 1
                self.graph.addNode(current_node)
                self.graph.addEdge(self.old_node, current_node)
            # if visited
            current_node = Node(str(self.index), j - 2, i)
            self.old_node = current_node
            self.pos[1] = j - 2

    def removeInvalidNode(self):
        i = 1
        while (i < len(self.graph.nodes)):
            current_node = self.graph.nodes[i]
            if(current_node.x == 1 and current_node.y == 1) or (current_node.x == self.size - 2 and current_node.y == self.size - 2):
                i += 1
            else:
                if(len(current_node.adjNodes) == 2):
                    pos1 = [current_node.x, current_node.y]
                    pos2 = [current_node.adjNodes[0].x,
                            current_node.adjNodes[0].y]
                    pos3 = [current_node.adjNodes[1].x,
                            current_node.adjNodes[1].y]

                    if (pos1[0] == pos2[0] and pos2[0] == pos3[0]) or (pos1[1] == pos2[1] and pos2[1] == pos3[1]):
                        self.graph.addEdge(
                            current_node.adjNode[0], current_node.adjNodes[1])
                        self.graph.remove(current_node)
                        continue
                i += 1

    def printMatrix(self):
        for i in range(self.size):
            for j in range(self.size):
                print(self.matrix[i][j], end=" ")
            print()

    def print_to_file(self):
        file = open("map.txt", "w")
        for row in range(len(self.matrix)):
            for col in range(len(self.matrix)):
                file.write(str(self.matrix[row][col]) + " ")
            file.write("\n")
